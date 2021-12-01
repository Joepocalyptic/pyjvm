from dataclasses import dataclass
from objects import ElementValue, Annotation


@dataclass
class AnnotationElementValue(ElementValue):
    annotation_value: Annotation
