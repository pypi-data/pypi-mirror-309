__all__ = ["DataModel", "DataModelField"]

from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field


class DataModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="ignore")

    def to_dict(self):
        return self.model_dump()

    def to_json(self):
        return self.model_dump_json()

    def copy(self, deep: bool = False, **kwargs):
        return self.model_copy(deep=deep, **kwargs)

    @classmethod
    def from_dict(cls, obj: dict | None) -> Self:
        return cls.model_validate(obj)

    @classmethod
    def from_json(cls, json: str) -> Self:
        return cls.model_validate_json(json)


def DataModelField(
    alias: str | None = None,
    exclude: bool | None = None,
    **kwargs,
) -> Any:
    return Field(alias=alias, exclude=exclude, **kwargs)
