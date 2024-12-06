
import inspect

from pyerd.constants import MODULE_EXCLUDES, PARENT_EXCLUDES
from pyerd.model_node import ModelNode


def get_classes(module):
    """Get classes in the given module

    Args:
        module: Python Module

    Returns:
        list: List of classes in module
    """
    classes = []
    for name, obj in inspect.getmembers(module):
        if name not in MODULE_EXCLUDES and inspect.isclass(obj):
            classes.append(obj)
    return classes


def get_nodes_for_classes(classes):
    nodes = []

    for cls in classes:
        # Either get __annotations__ or model_fields
        members = inspect.getmembers(cls)
        fields = {}
        for member in members:
            if member[0] == '__annotations__':
                fields = member[1]
        parents = [parent for parent in cls.__bases__ if parent.__name__ not in PARENT_EXCLUDES]
        nodes.append(ModelNode(name=cls.__name__, parents=parents, fields=fields))
    return nodes