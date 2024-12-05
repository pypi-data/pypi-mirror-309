from __future__ import annotations

from ._models import DataModel, Kind


class ComponentNode(DataModel):
    handle: str
    name: str
    kind: Kind
    provider: ProviderNode
    depends: list[ComponentNode] = []


class ProviderNode(DataModel):
    name: str
    kind: str
    depends: list[ComponentNode] = []
