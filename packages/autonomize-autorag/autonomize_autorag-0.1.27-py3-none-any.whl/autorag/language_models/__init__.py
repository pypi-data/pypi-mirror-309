# pylint: disable=missing-module-docstring

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from autorag.language_models.base import LanguageModel
    from autorag.language_models.modelhub import ModelhubLanguageModel
    from autorag.language_models.ollama import OllamaLanguageModel
    from autorag.language_models.openai import (
        AzureOpenAILanguageModel,
        OpenAILanguageModel,
    )

__all__ = [
    "ModelhubLanguageModel",
    "LanguageModel",
    "OllamaLanguageModel",
    "OpenAILanguageModel",
    "AzureOpenAILanguageModel",
]

_module_lookup = {
    "ModelhubLanguageModel": "autorag.language_models.modelhub",
    "LanguageModel": "autorag.language_models.base",
    "OllamaLanguageModel": "autorag.language_models.ollama",
    "OpenAILanguageModel": "autorag.language_models.openai",
    "AzureOpenAILanguageModel": "autorag.language_models.openai",
}


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module = importlib.import_module(_module_lookup[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")
