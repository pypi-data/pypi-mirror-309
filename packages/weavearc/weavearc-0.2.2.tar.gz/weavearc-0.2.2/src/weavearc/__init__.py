"""
cortex.base is a module that provides the core
functionality any API needs to run.
"""

from msgspec import Meta, field

from .data import (
    AsyncRepository,
    ConstContainer,
    CreateResult,
    DeleteResult,
    Entity,
    BaseModel,
    ReadAllResult,
    ReadResult,
    Repository,
    UpdateResult,
    ValueObject,
)
from .contracts import AsyncExecutable, Executor, Executable
from .utils.builders import DynamicDict

__all__: list[str] = [
    "ConstContainer",
    "BaseModel",
    "field",
    "Meta",
    "Meta",
    "field",
    "AsyncRepository",
    "Repository",
    "ReadAllResult",
    "ReadResult",
    "CreateResult",
    "UpdateResult",
    "DeleteResult",
    "Executor",
    "Entity",
    "ValueObject",
    "AsyncExecutable",
    "DynamicDict",
    "Executable",
]
