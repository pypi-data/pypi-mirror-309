from __future__ import annotations

import msgspec


class ConstContainer(msgspec.Struct, kw_only=True, frozen=True):  # type: ignore[call-arg]
    """
    A fast and memory-efficient immutable container class using BaseModel.

    This class provides a base for creating constant containers with the following features:
    - Immutability (frozen=True)
    - Fast serialization and deserialization
    - Memory efficiency
    - Type checking support
    """
