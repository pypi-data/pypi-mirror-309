from __future__ import annotations

import importlib
import importlib.util
import inspect
import os
import re
import sys
from enum import Enum
from typing import Any

from ._component import Component, Provider
from ._models import Operation
from .constants import ROOT_PACKAGE_NAME
from .dependency import ComponentNode, ProviderNode
from .exceptions import LoadError
from .manifest import ComponentInstance, Manifest
from .spec import Kind


class Loader:
    MANIFEST_FILE = "manifest.yaml"
    dir: str
    manifest_path: str

    manifest: Manifest
    root: str

    _init = False
    _dependencies: dict[str, ComponentDependency] = dict()

    def __init__(
        self,
        dir: str = ".",
        manifest: str = MANIFEST_FILE,
        root: str | None = None,
    ):
        self.dir = dir
        self.manifest_path = os.path.join(
            dir,
            manifest,
        )
        self.manifest = Manifest.parse(path=self.manifest_path)
        if root is not None:
            self.root = root
        elif self.manifest.root is not None:
            self.root = self.manifest.root
        abs_project_folder = os.path.abspath(dir)
        if abs_project_folder not in sys.path:
            sys.path.append(abs_project_folder)
        self._prepare_unresolved()

    def load_root(self) -> Component:
        if self.root is None:
            raise LoadError("Root handle must be specified")
        return self._resolve_component(self.root).component

    def load_component(self, handle: str) -> Component:
        return self._resolve_component(handle).component

    def get_dependency_graph(self) -> ComponentNode:
        def _get_node(component: ComponentDependency) -> ComponentNode:
            node = ComponentNode(
                handle=component.handle,
                name=component.name,
                kind=component.kind,
                provider=ProviderNode(
                    name=component.provider.name, kind=component.provider.kind
                ),
            )
            dependencies = self._get_dependencies_from_param(
                component.parameters
            )
            for dependency in dependencies:
                node.depends.append(_get_node(dependency))

            dependencies = self._get_dependencies_from_param(
                component.provider.parameters
            )
            for dependency in dependencies:
                node.provider.depends.append(_get_node(dependency))
            return node

        return _get_node(self._dependencies[self.root])

    def _resolve_component(
        self,
        handle: str,
    ) -> ComponentDependency:
        if handle in self._dependencies:
            if self._dependencies[handle].resolved:
                return self._dependencies[handle]
            cdep = self._dependencies[handle]
        else:
            raise LoadError(f"Unresolved component {handle}")
        cdep.parameters = self._resolve_param(
            cdep.parameters,
        )
        pdep = self._resolve_provider(handle)
        cdep.component = self._init_component(cdep, pdep.provider)
        cdep.component._handle = handle
        cdep.resolved = True
        return cdep

    def _resolve_provider(
        self,
        component_handle: str,
    ) -> ProviderDependency:
        cdep = self._dependencies[component_handle]
        pdep = cdep.provider
        pdep.parameters = self._resolve_param(
            pdep.parameters,
        )
        pdep.provider = self._init_provider(pdep)
        pdep.resolved = True
        return pdep

    def _resolve_param(self, value: Any) -> Any:
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = self._resolve_param(v)
            return value
        elif isinstance(value, list):
            for i, item in enumerate(value):
                value[i] = self._resolve_param(item)
            return value
        elif isinstance(value, str) and self._is_ref(value):
            ref_info = self._get_ref_info(value)
            if ref_info.type == RefType.COMPONENT:
                return self._resolve_component(
                    ref_info.component_handle,
                ).component
            elif ref_info.type == RefType.COMPONENT_GET:
                return self._resolve_component_get(
                    self._resolve_component(
                        ref_info.component_handle,
                    ).component,
                    ref_info.get_args,
                )
        return value

    def _get_dependencies_from_param(
        self, value: Any
    ) -> list[ComponentDependency]:
        dependencies: list = []
        if isinstance(value, dict):
            for k, v in value.items():
                dependencies.extend(self._get_dependencies_from_param(v))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                dependencies.extend(self._get_dependencies_from_param(item))
        elif isinstance(value, str) and self._is_ref(value):
            ref_info = self._get_ref_info(value)
            if ref_info.component_handle in self._dependencies:
                dependencies.append(
                    self._dependencies[ref_info.component_handle]
                )
            else:
                raise LoadError(
                    f"Unresolved component {ref_info.component_handle}"
                )
        return dependencies

    def _init_component(
        self,
        cdep: ComponentDependency,
        provider: Provider,
    ) -> Component:
        path = cdep.py_path
        if cdep.py_path is not None and cdep.py_path.startswith("."):
            path = os.path.join(
                self.dir,
                cdep.name,
                cdep.py_path,
            )
        component = Loader.load_component_instance(
            path=path,
            parameters=cdep.parameters,
            provider=provider,
        )
        return component

    def _init_provider(self, pdep: ProviderDependency) -> Provider:
        path = pdep.py_path
        if pdep.py_path is not None and pdep.py_path.startswith("."):
            path = os.path.join(
                self.dir,
                pdep.component_name,
                pdep.py_path,
            )
        provider = Loader.load_provider_instance(
            path=path,
            parameters=pdep.parameters,
        )
        return provider

    def _prepare_unresolved(self):
        for component in self.manifest.components:
            self._prepare_component_dependency(component)

    def _prepare_component_dependency(self, component: ComponentInstance):
        cdep = ComponentDependency()
        cdep.handle = component.handle
        cdep.name = component.name
        cdep.parameters = component.parameters
        cdep.kind = component.kind
        namespace, package = component.name.split("_", 1)
        if component.kind == Kind.CUSTOM:
            cdep.py_path = f"{component.name}.component"
        else:
            cdep.py_path = (
                f"{ROOT_PACKAGE_NAME}.{namespace}.{package}.component"
            )
        pdep = ProviderDependency()
        pdep.component_name = component.name
        pdep.name = component.provider.name
        pdep.parameters = component.provider.parameters
        pdep.kind = component.provider.kind
        if (
            component.kind == Kind.CUSTOM
            or component.provider.kind == Kind.CUSTOM
        ):
            pdep.py_path = (
                f"{component.name}.providers.{component.provider.name}"
            )
        else:
            namespace = f"{ROOT_PACKAGE_NAME}.{namespace}.{package}"
            pdep.py_path = f"{namespace}.providers.{component.provider.name}"
        pdep.resolved = False
        cdep.provider = pdep
        cdep.resolved = False
        self._dependencies[component.handle] = cdep

    def _resolve_component_get(self, component: Component, get_args: dict):
        res = component.run(operation=Operation(name="get", args=get_args))
        return res.result.value

    def _resolve_provider_get(self, provider: Provider, get_args: dict):
        res = provider.run(operation=Operation(name="get", args=get_args))
        return res.result.value

    def _get_ref_info(self, str: str):
        pattern = r"^\{\{(.+)\}\}$"
        match = re.match(pattern, str)
        if not match:
            raise LoadError(f"{str} not a ref")
        value = match.group(1)
        splits = value.split(".")
        ref_info = RefInfo()
        ref_info.component_handle = splits[0]
        if len(splits) == 1:
            ref_info.type = RefType.COMPONENT
        elif len(splits) == 2:
            ref_info.type = RefType.COMPONENT_GET
            ref_info.get_args = dict(key=dict(id=splits[1]))
        elif len(splits) == 3:
            ref_info.type = RefType.COMPONENT_GET
            ref_info.get_args = dict(key=dict(label=splits[1], id=splits[2]))
        return ref_info

    def _is_ref(self, str: str) -> bool:
        pattern = r"^\{\{.+\}\}$"
        return bool(re.match(pattern, str))

    def _get_path(self, base_dir: str, manifest_path: str):
        return os.path.join(base_dir, manifest_path)

    @staticmethod
    def load_provider_instance(
        path: str | None = None,
        parameters: dict[str, Any] = dict(),
    ) -> Provider:
        if path is None:
            return Provider(**parameters)
        provider = Loader.load_class(path, Provider)
        return provider(**parameters)

    @staticmethod
    def load_component_instance(
        path: str | None,
        parameters: dict,
        provider: Provider,
    ) -> Component:
        if path is None:
            return Component(provider=provider, **parameters)
        component = Loader.load_class(path, Component)
        return component(provider=provider, **parameters)

    @staticmethod
    def load_class(path: str, type: Any) -> Any:
        class_name = None
        if ":" in path:
            splits = path.split(":")
            module_name = splits[0]
            class_name = splits[-1]
        else:
            module_name = path
        if module_name.endswith(".py"):
            import sys

            normalized_module_name = (
                os.path.normpath(module_name)
                .replace("\\", "/")
                .split(".py")[0]
                .replace("/", ".")
                .lstrip(".")
            )
            spec = importlib.util.spec_from_file_location(
                normalized_module_name, os.path.abspath(path)
            )
            if spec is not None:
                module = importlib.util.module_from_spec(spec)
                sys.modules[normalized_module_name] = module
                if spec.loader is not None:
                    spec.loader.exec_module(module)
            module_name = normalized_module_name
        else:
            module = importlib.import_module(module_name)
        if class_name is not None:
            return getattr(module, class_name)
        else:
            for name, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, type) and cls.__module__ == module_name:
                    return cls
        raise LoadError(f"{type.__name__} not found at {module}")


class RefInfo:
    type: RefType
    component_handle: str
    get_args: dict


class RefType(int, Enum):
    COMPONENT = 0
    COMPONENT_GET = 1


class ComponentDependency:
    handle: str
    name: str
    kind: Kind
    parameters: dict[str, Any]
    py_path: str | None
    provider: ProviderDependency
    component: Component
    resolved: bool = False


class ProviderDependency:
    component_name: str
    name: str
    kind: Kind
    parameters: dict[str, Any]
    py_path: str | None
    provider: Provider
    resolved: bool = False
