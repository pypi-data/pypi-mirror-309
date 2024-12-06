from pyerd.diagrams.diagram import DiagramType, Diagram
from pyerd.utils import get_classes, get_nodes_for_classes


def draw(python_module, output: str | None = None):
    classes = get_classes(python_module)
    nodes = get_nodes_for_classes(classes)

    generator = Diagram(DiagramType.MERMAID)
    mermaid_diagram = generator.generate_diagram(nodes)
    if output is None:
        print(mermaid_diagram)
    else:
        with open(output, 'w') as file:
            file.write("```mermaid")
            file.write(mermaid_diagram)
            file.write("```")
