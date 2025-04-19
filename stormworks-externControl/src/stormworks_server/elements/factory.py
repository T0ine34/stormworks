from xml.etree.ElementTree import Element
from .component import Component


def getClasses(_class : type):
    classes = _class.__subclasses__()
    for cls in classes:
        classes += getClasses(cls)
    return classes
    


class ElementFactory:
    @staticmethod
    def fromXml(xml : Element):
        classes = getClasses(Component)
        for cls in classes:
            if cls.__name__ == xml.tag:
                return cls.fromXml(xml)
        raise ValueError(f"Invalid element: {xml.tag}; available elements: {', '.join([cls.__name__ for cls in classes])}")
