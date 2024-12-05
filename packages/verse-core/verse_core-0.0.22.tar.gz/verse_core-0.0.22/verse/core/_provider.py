from typing import Any

from ._async_helper import AsyncHelper
from ._models import Context, Operation, Response
from .exceptions import NotSupportedError


class Provider:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def init(self, context: Context | None = None) -> None:
        pass

    async def ainit(self, context: Context | None = None) -> None:
        await AsyncHelper.to_async(func=self.init, context=context)

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Response[Any]:
        raise NotSupportedError(
            operation.to_json() if operation is not None else None
        )

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Response[Any]:
        return await AsyncHelper.to_async(
            func=self.run, operation=operation, context=context
        )
