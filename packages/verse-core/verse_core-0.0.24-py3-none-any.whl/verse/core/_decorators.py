import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, cast, get_origin, get_type_hints

from ._models import Operation, Response

T = TypeVar("T", bound=Callable[..., Any])


def operation() -> Callable[[T], T]:
    def decorator(func: T) -> T:
        if not inspect.iscoroutinefunction(func):

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                self = args[0]
                context = kwargs.pop("context", None)

                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                locals = dict(bound_args.arguments)
                locals.pop("self", None)

                operation = Operation.normalize(
                    name=func.__name__,
                    args=locals,
                )
                response = self.run(operation, context)
                return_type = get_type_hints(func).get("return", None)
                if return_type is None:
                    return response
                elif get_origin(return_type) is Response:
                    return response
                else:
                    return response.result

            return cast(T, wrapper)
        else:

            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                self = args[0]
                context = kwargs.pop("context", None)

                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                locals = dict(bound_args.arguments)
                locals.pop("self", None)

                operation = Operation.normalize(
                    name=func.__name__[1:],
                    args=locals,
                )
                response = await self.arun(operation, context)
                return_type = get_type_hints(func).get("return", None)
                if return_type is None:
                    return response
                elif get_origin(return_type) is Response:
                    return response
                else:
                    return response.result

            return cast(T, wrapper)

    return decorator
