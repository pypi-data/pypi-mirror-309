from __future__ import annotations

import asyncio
from typing import Protocol, runtime_checkable, TypeVar, ParamSpec, Callable, Union

T_co = TypeVar("T_co", covariant=True)
P = ParamSpec("P")


@runtime_checkable
class Executable(Protocol[T_co]):
    """Protocol for synchronous services within the application."""

    def execute(self) -> T_co:
        """Performs the service's main operations."""
        ...


@runtime_checkable
class AsyncExecutable(Protocol[T_co]):
    """Protocol for asynchronous services within the application."""

    async def execute(self) -> T_co:
        """Performs the service's main operations asynchronously."""
        ...


class Executor:
    """Executor for services, handling both synchronous and asynchronous services."""

    async def execute(
        self,
        service_class: Callable[P, Union[Executable[T_co], AsyncExecutable[T_co]]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T_co:
        """Executes a given service class with provided arguments."""
        service_instance = service_class(*args, **kwargs)

        match service_instance:
            case AsyncExecutable():
                result: T_co = await service_instance.execute()
            case Executable():
                loop: asyncio.events.AbstractEventLoop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, service_instance.execute)
            case _:
                raise ValueError(
                    "Invalid service type. Must be either Executable or AsyncExecutable."
                )

        return result
