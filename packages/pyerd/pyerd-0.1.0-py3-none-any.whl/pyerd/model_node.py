from dataclasses import dataclass


@dataclass
class ModelNode:
    name: str
    fields: dict
    parents: list[str]