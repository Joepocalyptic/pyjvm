from dataclasses import dataclass
from objects.attributes import ElementValue, Annotation


@dataclass
class AnnotationElementValue(ElementValue):
    annotation_value: Annotation
