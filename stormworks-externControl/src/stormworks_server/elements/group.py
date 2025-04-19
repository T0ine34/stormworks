from typing import List, Tuple
from uuid import uuid4 as uuid
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .factory import ElementFactory
from .component import Component
from .utils import Position

class Group(Component):
    def __init__(self, elements : List[BaseElement]):
        super().__init__()
        self.elements = elements
        
        self._position = self.__calculatePosition()
        
    def __calculatePosition(self) -> Position:
        x1 = min([e.position.x for e in self.elements])
        y1 = min([e.position.y for e in self.elements])
        x2 = max([e.position.x + e.position.width for e in self.elements])
        y2 = max([e.position.y + e.position.height for e in self.elements])
        
        return Position(x1, y1, x2 - x1, y2 - y1)
        
    def html(self) -> Tuple[Element, str]:
        styleSheetList = []
        
        container = Element("div")
        container.set("class", "group container")
        container.set("id", self.cssId)

        for e in self.elements:
            htmlElement, css = e.html()
            styleSheetList.append(css)
            container.append(htmlElement)
            
        
        css =  "#" + self.cssId + "{\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += f"   grid-template-columns: repeat({self._position.width}, 1fr);\n"
        css += f"   grid-template-rows: repeat({self._position.height}, 1fr);\n"
        css += "}\n"
        
        css += "\n".join(styleSheetList)
        
        return container, css
    
    @staticmethod
    def fromXml(xml : Element):
        elements = []
        for e in xml:
            elements.append(ElementFactory.fromXml(e))
        return Group(elements)
    
    def __str__(self):
        return f"Group {len(self.elements)} elements"
    

    @property
    def position(self):
        return self._position

    @property
    def hasChildren(self):
        return True
    
    @property
    def children(self):
        return self.elements