from typing import Dict, Any, List
from sqlalchemy import text

from llama_index.core.schema import BaseNode, MetadataMode, TextNode
from llama_index.core.vector_stores.utils import metadata_dict_to_node, node_to_metadata_dict


class SimilarityFunction:
    """Custom similarity function for vector comparisons."""
    
    def __init__(self, sql_template: str):
        """Initialize with SQL template.
        
        Args:
            sql_template: SQL template string that will be formatted with 
                {embedding_col} and :query_embedding
        """
        self.sql_template = sql_template

    def __call__(self, embedding_col: str, query_embedding: List[float]) -> text:
        """Generate SQL text with parameters."""
        sql = self.sql_template.format(embedding_col=embedding_col)
        return text(sql).bindparams(query_embedding)


DEFAULT_SIMILARITY_FUNCTIONS = {
    "postgresql": {
        "cosine": SimilarityFunction("1 - ({embedding_col} <=> $1)"),
        "euclidean": SimilarityFunction("1 / (1 + ({embedding_col} <-> :query_embedding))"),
    },
}

DEFAULT_JSON_EXTRACTORS = {
    "postgresql": lambda col, key: f"{col}->>{key}",
    "mysql": lambda col, key: f"JSON_EXTRACT({col}, $.{key})",
    "sqlite": lambda col, key: f"json_extract({col}, $.{key})",
}

class FieldMapper:
    """Maps between node fields and database columns."""
    
    def to_db(self, node: BaseNode) -> Dict[str, Any]:
        """Convert node to database fields."""
        raise NotImplementedError
        
    def to_node(self, row: Any) -> BaseNode:
        """Convert database row to node."""
        raise NotImplementedError

class DefaultFieldMapper(FieldMapper):
    """Default implementation that uses JSON metadata column."""
    
    def __init__(
        self,
        id_col: str = "id",
        text_col: str = "text",
        embedding_col: str = "embedding",
        metadata_col: str = "metadata",
        flat_metadata: bool = True
    ):
        self.id_col = id_col
        self.text_col = text_col
        self.embedding_col = embedding_col
        self.metadata_col = metadata_col
        self.flat_metadata = flat_metadata
    
    def to_db(self, node: BaseNode) -> Dict[str, Any]:
        """Store metadata as JSON."""
        return {
            self.id_col: node.node_id,
            self.text_col: node.get_content(metadata_mode=MetadataMode.NONE),
            self.embedding_col: node.get_embedding(),
            self.metadata_col: node_to_metadata_dict(
                node, remove_text=True, flat_metadata=self.flat_metadata
            )
        }
        
    def to_node(self, row: Any) -> BaseNode:
        """Reconstruct node from JSON metadata."""
        try:
            metadata = getattr(row, self.metadata_col)
            node = metadata_dict_to_node(metadata)
            node.set_content(str(getattr(row, self.text_col)))
        except Exception:
            # Fallback to basic node
            node = TextNode(
                text=getattr(row, self.text_col),
                id_=getattr(row, self.id_col),
                metadata=metadata,
            )
        return node

class ColumnFieldMapper(FieldMapper):
    """Maps node fields to individual table columns."""
    
    def __init__(
        self,
        id_col: str = "id",
        text_col: str = "text", 
        embedding_col: str = "embedding",
        metadata_column_map: Dict[str, str] = None
    ):
        """Initialize with column mappings.
        
        Args:
            id_col: Column name for node ID
            text_col: Column name for text content
            embedding_col: Column name for embedding
            metadata_column_map: Mapping of metadata keys to column names
                e.g. {"doc_id": "document_id", "source": "doc_source"}
        """
        self.id_col = id_col
        self.text_col = text_col
        self.embedding_col = embedding_col
        self.metadata_column_map = metadata_column_map or {}
        
    def to_db(self, node: BaseNode) -> Dict[str, Any]:
        """Map node fields to columns."""
        values = {
            self.id_col: node.node_id,
            self.text_col: node.get_content(metadata_mode=MetadataMode.NONE),
            self.embedding_col: node.get_embedding(),
        }
        
        # Map metadata fields to columns
        for meta_key, col_name in self.metadata_column_map.items():
            values[col_name] = node.metadata.get(meta_key)
            
        return values
        
    def to_node(self, row: Any) -> BaseNode:
        """Reconstruct node from columns."""
        metadata = {}
        for meta_key, col_name in self.metadata_column_map.items():
            metadata[meta_key] = getattr(row, col_name)
            
        return TextNode(
            text=getattr(row, self.text_col),
            id_=getattr(row, self.id_col),
            metadata=metadata,
        )
