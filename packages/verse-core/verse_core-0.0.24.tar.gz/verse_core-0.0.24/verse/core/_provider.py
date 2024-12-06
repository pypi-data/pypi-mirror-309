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
        if operation is not None and operation.name is not None:
            func_name = operation.name
            func = getattr(self, func_name, None)
            if func is not None and callable(func):
                self.init()
                result = func(**operation.args or {})
                if not isinstance(result, Response):
                    return Response(result=result)
                return result

        raise NotSupportedError(
            operation.to_json() if operation is not None else None
        )

    async def arun(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Response[Any]:
        if operation is not None and operation.name is not None:
            func_name = f"a{operation.name}"
            func = getattr(self, func_name, None)
            if func is not None and callable(func):
                await self.ainit()
                result = await func(**operation.args or {})
                if not isinstance(result, Response):
                    return Response(result=result)
                return result

        return await AsyncHelper.to_async(
            func=self.run, operation=operation, context=context
        )
