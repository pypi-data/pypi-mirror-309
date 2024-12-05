from __future__ import annotations

from typing import Any

from ._models import DataModel, Kind
from ._yaml_loader import YamlLoader

__all__ = [
    "ComponentInstance",
    "Manifest",
    "ProviderInstance",
]


class ProviderInstance(DataModel):
    name: str
    kind: Kind = Kind.BASE
    parameters: dict[str, Any] = dict()


class ComponentInstance(DataModel):
    handle: str
    name: str
    kind: Kind = Kind.BASE
    parameters: dict[str, Any] = dict()
    provider: ProviderInstance


class Manifest(DataModel):
    components: list[ComponentInstance] = []
    root: str | None = None

    @staticmethod
    def parse(path: str) -> Manifest:
        obj = YamlLoader.load(path=path)
        manifest = Manifest.from_dict(obj)
        return manifest
