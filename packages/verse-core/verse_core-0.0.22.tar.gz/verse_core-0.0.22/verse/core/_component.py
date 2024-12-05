import time
import uuid
from typing import Any

from ._models import BaseContext, Context, Operation, Response
from ._provider import Provider


class Component:
    provider: Provider
    _debug: bool
    _unpack_result: bool
    _handle: str | None

    def __init__(
        self,
        **kwargs,
    ):
        self._debug = kwargs.pop("_debug", False)
        self._unpack_result = kwargs.pop("_unpack_result", False)
        self._handle = None
        self.provider = None
        provider = kwargs.pop("provider", "default")
        self.attach(provider=provider)

    def attach(
        self,
        provider: Provider | dict | str,
    ) -> None:
        if isinstance(provider, Provider):
            self.provider = provider
        else:
            if isinstance(provider, dict):
                name = provider.pop("name")
                parameters = provider.pop("parameters", dict())
            elif isinstance(provider, str):
                name = provider
                parameters = dict()
            from ._loader import Loader

            module_name = self.__class__.__module__.rsplit(".", 1)[0]
            provider_path = f"{module_name}.providers.{name}"
            provider_instance = Loader.load_provider_instance(
                path=provider_path,
                parameters=parameters,
            )
            self.attach(provider=provider_instance)
        self._attach_component_parameters()

    def init(self, context: Context | None = None) -> None:
        self.provider.init(context=context)

    async def ainit(self, context: Context | None = None) -> None:
        await self.provider.ainit(context=context)

    def run(
        self,
        operation: dict | str | Operation | None = None,
        context: dict | Context | None = None,
        **kwargs,
    ) -> Any:
        parent_context = self._convert_context(context)
        current_context = self._init_context(
            parent_context, kwargs.pop("context_info", None)
        )
        response = self.provider.run(
            operation=self._convert_operation(operation),
            context=current_context,
        )
        if isinstance(response, Response):
            if response.context is not None:
                current_context = response.context
        else:
            response = Response(result=response)
        self._finalize_context(parent_context, current_context)
        response.context = parent_context
        if not self._debug:
            response.native = None
        if self._unpack_result:
            return response.result
        return response

    async def arun(
        self,
        operation: dict | str | Operation | None = None,
        context: dict | Context | None = None,
        **kwargs,
    ) -> Any:
        parent_context = self._convert_context(context)
        current_context = self._init_context(
            parent_context, kwargs.pop("context_info", None)
        )
        response = await self.provider.arun(
            operation=self._convert_operation(operation),
            context=current_context,
        )
        if isinstance(response, Response):
            if response.context is not None:
                current_context = response.context
        else:
            response = Response(result=response)
        self._finalize_context(parent_context, current_context)
        response.context = parent_context
        if not self._debug:
            response.native = None
        if self._unpack_result:
            return response.result
        return response

    def execute(
        self,
        statement: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        operation = Operation(
            name="EXECUTE",
            args=dict(statement=statement, params=params),
        )
        return self.run(operation)

    async def aexecute(
        self,
        statement: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        operation = Operation(
            name="EXECUTE",
            args=dict(statement=statement, params=params),
        )
        return await self.arun(operation)

    def _attach_component_parameters(self):
        pass

    def _run_internal(
        self,
        op: str | None,
        args: dict,
        unpack_result: bool = False,
    ) -> Any:
        context = None
        unpack = False
        if "kwargs" in args:
            context = args["kwargs"].pop("context", None)
            unpack = args["kwargs"].pop("_unpack_result", False)
        res = self.run(
            operation=Operation.normalize(name=op, args=args), context=context
        )
        unpack = unpack or unpack_result
        if unpack:
            return res.result
        return res

    async def _arun_internal(
        self,
        op: str | None,
        args: dict,
        unpack_result: bool = False,
    ) -> Any:
        context = None
        unpack = False
        if "kwargs" in args:
            context = args["kwargs"].pop("context", None)
            unpack = args["kwargs"].pop("_unpack_result", False)
        res = await self.arun(
            operation=Operation.normalize(name=op, args=args), context=context
        )
        unpack = unpack or unpack_result
        if unpack:
            return res.result
        return res

    def _convert_operation(
        self,
        operation: dict | str | Operation | None,
    ) -> Operation | None:
        if isinstance(operation, dict):
            return Operation.from_dict(operation)
        elif isinstance(operation, str):
            return Operation(name=operation)
        return operation

    def _convert_context(
        self,
        context: dict | Context | None,
    ) -> Context | None:
        if isinstance(context, dict):
            return Context.from_dict(context)
        if context is None:
            return None
        return context

    def _init_context(
        self,
        parent_context: Context | None,
        context_info: dict | None,
    ) -> Context:
        provider_name = self.provider.__module__.split(".")[-1]
        component_name = self.__module__.split(".")[-2]
        if parent_context is not None:
            run_id = parent_context.run_id
        else:
            run_id = str(uuid.uuid4())
        ctx = Context(
            run_id=run_id,
            component=component_name,
            provider=provider_name,
            handle=self._handle,
            start_time=time.time(),
            parent=parent_context,
        )
        if parent_context is not None and parent_context.info is not None:
            ctx.info = parent_context.info
        if context_info is not None and ctx.info is None:
            ctx.info = context_info
        elif context_info is not None and ctx.info is not None:
            ctx.info = ctx.info.__dict__ | context_info
        return ctx

    def _finalize_context(
        self,
        parent_context: Context | None,
        current_context: Context,
    ):
        end_time = time.time()
        if current_context.start_time:
            current_context.latency = end_time - current_context.start_time
        if parent_context is not None:
            parent_context.children.append(
                BaseContext(
                    component=current_context.component,
                    provider=current_context.provider,
                    handle=current_context.handle,
                    info=current_context.info,
                    start_time=current_context.start_time,
                    latency=current_context.latency,
                    children=current_context.children,
                )
            )
