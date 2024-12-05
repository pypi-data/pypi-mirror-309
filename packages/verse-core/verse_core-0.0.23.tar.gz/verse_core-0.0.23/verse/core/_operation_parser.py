from __future__ import annotations

from typing import Any

from ._models import DataModel, Operation


class OperationParser:
    operation: Operation | None

    def __init__(self, operation: Operation | None):
        self.operation = operation

    def op_equals(self, name: str | None) -> bool:
        operation_name = self.get_name()
        if operation_name is not None:
            operation_name = operation_name.lower()
        arg_name = name
        if arg_name is not None:
            arg_name = arg_name.lower()
        return operation_name == arg_name

    def get_args(self) -> dict:
        if self.operation is not None and self.operation.args is not None:
            return self.operation.args
        return {}

    def get_nargs(self) -> dict | None:
        return self.get_arg("nargs")

    def get_arg(self, arg: str, convert_dict: bool = False) -> Any:
        if (
            self.operation is not None
            and self.operation.args is not None
            and arg in self.operation.args
        ):
            arg_val = self.operation.args[arg]
            if convert_dict and isinstance(arg_val, DataModel):
                return arg_val.to_dict()
            return arg_val
        return None

    def set_arg(self, arg: str, value: Any) -> None:
        if self.operation is not None:
            if self.operation.args is None:
                self.operation.args = dict()
            self.operation.args[arg] = value

    def get_name(self) -> str | None:
        if self.operation is not None:
            return self.operation.name
        return None

    def get_statement(self) -> str | None:
        return self.get_arg("statement")
