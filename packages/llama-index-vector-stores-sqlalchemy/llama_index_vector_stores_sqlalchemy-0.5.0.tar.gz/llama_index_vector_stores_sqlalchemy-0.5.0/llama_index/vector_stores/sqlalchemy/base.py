"""SQLAlchemy vector store."""

import logging
from typing import Any, Dict, List, Optional, Type, Union, cast, Callable

from sqlalchemy import Column, MetaData, Table, create_engine, text, String, Text, JSON
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import select

from llama_index.core.bridge.pydantic import Field, PrivateAttr
from llama_index.core.schema import BaseNode, MetadataMode, TextNode
from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
    FilterCondition,
    FilterOperator,
    MetadataFilter,
    MetadataFilters,
    VectorStoreQuery,
    VectorStoreQueryResult,
)
from llama_index.vector_stores.sqlalchemy.utils import (
    ColumnFieldMapper,
    DefaultFieldMapper,
    FieldMapper,
    SimilarityFunction,
    DEFAULT_SIMILARITY_FUNCTIONS,
    DEFAULT_JSON_EXTRACTORS,
)


class SQLAlchemyVectorStore(BasePydanticVectorStore):
    """SQLAlchemy vector store.
    
    Can work with any SQLAlchemy-supported database.
    
    Args:
        connection_string: SQLAlchemy connection string
        table_name: Name of table to store vectors
        schema_name: Database schema name
        table_schema: Optional custom table schema
        embed_dim: Embedding dimension
        hybrid_search: Whether to enable hybrid search
        distance_strategy: Distance calculation strategy (cosine, euclidean, etc)
        similarity_functions: Optional custom similarity functions per dialect
        json_extractor: Optional custom JSON extraction function
    """

    stores_text: bool = True
    flat_metadata: bool = True

    connection_string: str
    async_connection_string: str
    table_name: str 
    schema_name: str
    embed_dim: int
    hybrid_search: bool
    distance_strategy: str
    table_schema: Dict[str, Column] = Field(default_factory=dict)
    similarity_functions: Dict[str, Dict[str, SimilarityFunction]] = Field(default_factory=dict)
    json_extractors: Dict[str, Callable] = Field(default_factory=dict)
    field_mapper: FieldMapper = Field(default_factory=lambda: DefaultFieldMapper())
    insert_batch_size: int = 100

    _engine: Any = PrivateAttr()
    _async_engine: Any = PrivateAttr()
    _table: Any = PrivateAttr()
    _base: Any = PrivateAttr()
    _is_initialized: bool = PrivateAttr(default=False)
    _dialect_name: str = PrivateAttr()

    def __init__(
        self,
        connection_string: str,
        async_connection_string: str,
        table_name: str,
        field_mapper: Optional[FieldMapper] = None,
        schema_name: str = "public",
        table_schema: Optional[Dict[str, Column]] = None,
        embed_dim: int = 1536,
        hybrid_search: bool = False,
        distance_strategy: str = "cosine",
        similarity_functions: Optional[Dict[str, Dict[str, SimilarityFunction]]] = None,
        json_extractors: Optional[Dict[str, Callable]] = None,
        insert_batch_size: int = 100,
        **kwargs: Any,
    ) -> None:
        """Initialize params."""
        # Merge custom similarity functions with defaults
        all_similarity_functions = DEFAULT_SIMILARITY_FUNCTIONS.copy()
        if similarity_functions:
            for dialect, funcs in similarity_functions.items():
                if dialect not in all_similarity_functions:
                    all_similarity_functions[dialect] = {}
                all_similarity_functions[dialect].update(funcs)

        # Merge custom JSON extractors with defaults
        all_json_extractors = DEFAULT_JSON_EXTRACTORS.copy()
        if json_extractors:
            all_json_extractors.update(json_extractors)

        super().__init__(
            connection_string=connection_string,
            async_connection_string=async_connection_string,
            table_name=table_name,
            field_mapper=field_mapper or DefaultFieldMapper(),
            schema_name=schema_name,
            table_schema=table_schema or {},
            embed_dim=embed_dim,
            hybrid_search=hybrid_search,
            distance_strategy=distance_strategy,
            similarity_functions=all_similarity_functions,
            json_extractors=all_json_extractors,
            insert_batch_size=insert_batch_size,
        )

    def _initialize(self) -> None:
        """Initialize the vector store."""
        if not self._is_initialized:
            # Create SQLAlchemy engine and session
            self._engine = create_engine(self.connection_string)
            self._async_engine = create_async_engine(self.async_connection_string)
            self._dialect_name = self._engine.dialect.name
            
            # Create base class for declarative models
            self._base = declarative_base()
            
            # Create table if it doesn't exist
            metadata = MetaData(schema=self.schema_name)
            self._table = Table(
                self.table_name,
                metadata,
                *self.table_schema.values(),
                schema=self.schema_name
            )
            metadata.create_all(self._engine)
            
            self._is_initialized = True

    def _calculate_similarity(
        self, 
        embedding_col: Any,
        query_embedding: List[float],
        strategy: str = "cosine"
    ) -> Any:
        """Calculate similarity between embeddings based on strategy and dialect."""
        from sqlalchemy import literal_column

        if not query_embedding:
            raise ValueError("Query embedding cannot be None")

        dialect_funcs = self.similarity_functions.get(self._dialect_name, {})
        if not dialect_funcs:
            raise ValueError(
                f"No similarity functions defined for dialect: {self._dialect_name}"
            )
        
        similarity_func = dialect_funcs.get(strategy)
        if not similarity_func:
            raise ValueError(
                f"Strategy '{strategy}' not supported for dialect '{self._dialect_name}'. "
                f"Available strategies: {list(dialect_funcs.keys())}"
            )

        return literal_column(
            similarity_func(str(embedding_col), query_embedding).text
        )

    @classmethod
    def from_params(
        cls,
        dialect: str,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        table_name: str,
        **kwargs: Any
    ) -> "SQLAlchemyVectorStore":
        """Create store from connection parameters."""
        if dialect == "postgresql":
            connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            async_connection_string = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        elif dialect == "mysql":
            connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            async_connection_string = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        elif dialect == "sqlite":
            connection_string = f"sqlite:///{database}"
            async_connection_string = f"sqlite+aiosqlite:///{database}"
        else:
            raise ValueError(f"Unsupported dialect: {dialect}")

        return cls(
            connection_string=connection_string,
            async_connection_string=async_connection_string,
            table_name=table_name,
            **kwargs
        )

    @classmethod
    def from_existing_table(
        cls,
        connection_string: str,
        async_connection_string: str,
        table_name: str,
        id_column: str,
        text_column: str,
        embedding_column: str,
        metadata_columns: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ) -> "SQLAlchemyVectorStore":
        """Create store from existing table schema."""
        # Create table schema based on existing columns
        table_schema = {
            id_column: Column(id_column, String, primary_key=True),
            text_column: Column(text_column, Text),
            embedding_column: Column(embedding_column, Text),  # or appropriate type for your embeddings
        }
        
        # Add metadata columns to schema
        if metadata_columns:
            for _, col_name in metadata_columns.items():
                table_schema[col_name] = Column(col_name, Text)  # adjust type as needed
        
        field_mapper = ColumnFieldMapper(
            id_col=id_column,
            text_col=text_column,
            embedding_col=embedding_column,
            metadata_column_map=metadata_columns
        )
        
        return cls(
            connection_string=connection_string,
            async_connection_string=async_connection_string,
            table_name=table_name,
            field_mapper=field_mapper,
            table_schema=table_schema,  # Add the table schema
            **kwargs
        )
    
    @property
    def client(self) -> Any:
        """Get underlying database client."""
        if not self._is_initialized:
            return None
        return self._engine

    @classmethod
    def class_name(cls) -> str:
        return "SQLAlchemyVectorStore"

    def add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        """Add nodes to vector store.
        
        Args:
            nodes: List of nodes with embeddings to add
            
        Returns:
            List of node IDs added
        """
        self._initialize()
        
        ids = []
        with Session(self._engine) as session:
            # Process nodes in batches
            for i in range(0, len(nodes), self.insert_batch_size):
                batch = nodes[i:i + self.insert_batch_size]
                
                with session.begin():
                    for node in batch:
                        values = self.field_mapper.to_db(node)
                        session.execute(
                            self._table.insert().values(**values)
                        )
                        ids.append(node.node_id)
                    
        return ids
    
    async def async_add(self, nodes: List[BaseNode], **add_kwargs: Any) -> List[str]:
        """Add nodes to vector store asynchronously."""
        self._initialize()
        
        ids = []
        async with AsyncSession(self._async_engine) as session:
            # Process nodes in batches
            for i in range(0, len(nodes), self.insert_batch_size):
                batch = nodes[i:i + self.insert_batch_size]
                
                async with session.begin():
                    for node in batch:
                        values = self.field_mapper.to_db(node)
                        await session.execute(
                            self._table.insert().values(**values)
                        )
                        ids.append(node.node_id)
                    
        return ids
    
    def delete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        """Delete nodes with given ref_doc_id in metadata."""
        self._initialize()
        
        with Session(self._engine) as session:
            with session.begin():
                json_extractor = self.json_extractors.get(self._dialect_name)
                if not json_extractor:
                    raise ValueError(f"JSON operations not implemented for dialect: {self._dialect_name}")
                
                where_clause = text(
                    f"{json_extractor('metadata', 'doc_id')} = :ref_doc_id"
                )
                session.execute(
                    self._table.delete().where(where_clause),
                    {"ref_doc_id": ref_doc_id}
                )
    
    async def adelete(self, ref_doc_id: str, **delete_kwargs: Any) -> None:
        """Delete nodes with given ref_doc_id in metadata."""
        self._initialize()

        async with AsyncSession(self._async_engine) as session:
            async with session.begin():
                json_extractor = self.json_extractors.get(self._dialect_name)
                if not json_extractor:
                    raise ValueError(f"JSON operations not implemented for dialect: {self._dialect_name}")
                
                where_clause = text(
                    f"{json_extractor('metadata', 'doc_id')} = :ref_doc_id"
                )
                await session.execute(
                    self._table.delete().where(where_clause),
                    {"ref_doc_id": ref_doc_id}
                )

    def query(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        """Query vector store."""
        self._initialize()

        # Build query using field mapper's column names
        similarity_expr = self._calculate_similarity(
            getattr(self._table.c, self.field_mapper.embedding_col),
            query.query_embedding,
            self.distance_strategy
        )

        # Build base query
        stmt = select(
            self._table,
            similarity_expr.label("similarity")
        )

        # Add WHERE clause if there are filters
        if query.filters:
            where_clause = self._build_filter_clause(query.filters)
            stmt = stmt.where(where_clause)

        # Add ORDER BY and LIMIT
        stmt = stmt.order_by(text("similarity DESC")).limit(query.similarity_top_k)

        # Execute query
        with Session(self._engine) as session:
            results = session.execute(stmt).fetchall()

        # Convert results to nodes using field mapper
        nodes = []
        similarities = []
        ids = []

        for result in results:
            node = self.field_mapper.to_node(result)
            nodes.append(node)
            similarities.append(float(result.similarity))
            ids.append(node.node_id)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities, 
            ids=ids
        )
    
    async def aquery(self, query: VectorStoreQuery, **kwargs: Any) -> VectorStoreQueryResult:
        """Query vector store asynchronously."""
        self._initialize()

        # Build query using field mapper's column names
        stmt = select(
            self._table,
            self._calculate_similarity(
                getattr(self._table.c, self.field_mapper.embedding_col),
                query.query_embedding,
                self.distance_strategy
            ).label("similarity")
        )

        if query.filters:
            stmt = stmt.where(self._build_filter_clause(query.filters))

        stmt = stmt.order_by(text("similarity DESC")).limit(query.similarity_top_k)

        # Execute query
        async with AsyncSession(self._async_engine) as session:
            results = await session.execute(stmt)
            results = results.fetchall()

        # Convert results to nodes using field mapper
        nodes = []
        similarities = []
        ids = []

        for result in results:
            node = self.field_mapper.to_node(result)
            nodes.append(node)
            similarities.append(float(result.similarity))
            ids.append(node.node_id)

        return VectorStoreQueryResult(
            nodes=nodes,
            similarities=similarities, 
            ids=ids
        )

    def _build_filter_clause(self, filters: MetadataFilters) -> Any:
        """Convert metadata filters to SQL WHERE clause."""
        from sqlalchemy import text

        # Handle nested filters recursively
        if isinstance(filters, MetadataFilters):
            from sqlalchemy import and_, or_
            
            conditions = []
            for filter_ in filters.filters:
                if isinstance(filter_, MetadataFilters):
                    conditions.append(self._build_filter_clause(filter_))
                else:
                    conditions.append(self._build_single_filter(filter_))
                    
            if filters.condition == "and":
                return and_(*conditions)
            elif filters.condition == "or":
                return or_(*conditions)
            else:
                raise ValueError(f"Invalid condition: {filters.condition}")
        else:
            return _build_single_filter(filters)

    def _build_single_filter(self, filter_: MetadataFilter) -> Any:
        json_extractor = self.json_extractors.get(self._dialect_name)
        if not json_extractor:
            raise ValueError(f"JSON operations not implemented for dialect: {self._dialect_name}")

        if filter_.operator in [FilterOperator.IN, FilterOperator.NIN]:
            # For IN/NIN operators, format list of values
            filter_value = ", ".join(f"'{e}'" for e in filter_.value)
            return text(
                f"{json_extractor('metadata_', filter_.key)} "
                f"{self._to_sql_operator(filter_.operator)} "
                f"({filter_value})"
            )
        elif filter_.operator == FilterOperator.CONTAINS:
            if self._dialect_name == "postgresql":
                # Postgres-specific JSON array containment
                return text(
                    f"metadata_::jsonb->'{filter_.key}' @> '[\"{filter_.value}\"]'"
                )
            else:
                # Generic JSON array contains implementation
                # Note: This is a simplified version and may need to be adapted per dialect
                # Should work for now
                return text(
                    f"JSON_CONTAINS({json_extractor('metadata_', filter_.key)}, "
                    f"'[\"{filter_.value}\"]')"
                )
        elif filter_.operator == FilterOperator.TEXT_MATCH:
            # Standard SQL LIKE operator
            return text(
                f"{json_extractor('metadata_', filter_.key)} "
                f"{self._to_sql_operator(filter_.operator)} "
                f"'%{filter_.value}%'"
            )
        else:
            # Try to handle numeric values by casting
            try:
                float(filter_.value)
                cast_expr = {
                    "postgresql": "CAST({} AS FLOAT)",
                    "mysql": "CAST({} AS DECIMAL)",
                    "sqlite": "CAST({} AS REAL)",
                }.get(self._dialect_name, "CAST({} AS FLOAT)")
                
                return text(
                    f"{cast_expr.format(json_extractor('metadata_', filter_.key))} "
                    f"{self._to_sql_operator(filter_.operator)} "
                    f"{float(filter_.value)}"
                )
            except (ValueError, TypeError):
                # Fall back to string comparison
                return text(
                    f"{json_extractor('metadata_', filter_.key)} "
                    f"{self._to_sql_operator(filter_.operator)} "
                    f"'{filter_.value}'"
                )

    def _to_sql_operator(self, operator: FilterOperator) -> str:
        """Convert filter operator to SQL operator."""
        operator_map = {
            FilterOperator.EQ: "=",
            FilterOperator.GT: ">",
            FilterOperator.LT: "<",
            FilterOperator.GTE: ">=",
            FilterOperator.LTE: "<=",
            FilterOperator.NE: "!=",
            FilterOperator.IN: "IN",
            FilterOperator.NIN: "NOT IN",
            FilterOperator.TEXT_MATCH: "LIKE"
        }
        if operator not in operator_map:
            raise ValueError(f"Unsupported filter operator: {operator}")
        return operator_map[operator]