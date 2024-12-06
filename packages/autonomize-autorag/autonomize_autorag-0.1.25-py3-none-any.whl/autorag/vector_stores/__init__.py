# pylint: disable=missing-module-docstring

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from autorag.vector_stores.azure_ai_search import AzureAISearchVectorStore
    from autorag.vector_stores.base import VectorStore
    from autorag.vector_stores.qdrant import QdrantVectorStore

__all__ = [
    "VectorStore",
    "AzureAISearchVectorStore",
    "QdrantVectorStore",
]

_module_lookup = {
    "VectorStore": "autorag.vector_stores.base",
    "AzureAISearchVectorStore": "autorag.vector_stores.azure_ai_search",
    "QdrantVectorStore": "autorag.vector_stores.qdrant",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
