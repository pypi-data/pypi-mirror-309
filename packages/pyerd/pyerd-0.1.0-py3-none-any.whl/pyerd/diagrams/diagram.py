
import enum
from pyerd.diagrams.mermaid import nodes_to_mermaid
from pyerd.model_node import ModelNode


class DiagramType(enum.Enum):
  MERMAID = "mermaid"

class Diagram:
  def __init__(self, type: DiagramType):
    self.type = type

  def generate_diagram(self, nodes: list[ModelNode]) -> str:
    match self.type:
      case DiagramType.MERMAID:
        return nodes_to_mermaid(nodes)
    raise ValueError("Diagram type unknown")