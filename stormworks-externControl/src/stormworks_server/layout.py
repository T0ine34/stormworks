from xml.etree.ElementTree import Element, tostring, fromstring
from xml.etree import ElementTree as ET
from typing import List
import os
from gamuLogger import Logger

from .elements import Component, ElementFactory

PATH = os.path.dirname(os.path.abspath(__file__))


# register namespaces for html and svg
ET.register_namespace("", "http://www.w3.org/1999/xhtml")
ET.register_namespace("", "http://www.w3.org/2000/svg")


class Layout:
    def __init__(self, elements : List[Component], name : str):
        self.elements = elements
        self._width = 0
        self._height = 0
        self._name  = name
        self._calculateSize()
        
    def _calculateSize(self):
        for e in self.elements:
            self._width = max(self._width, e.position.x + e.position.width - 1)
            self._height = max(self._height, e.position.y + e.position.height - 1)
    
    def html(self, template_path : str) -> str:
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        elementsAsString = []
        
        styleSheetList = []
        
        css = ".container {\n"
        css += f"   grid-template-columns: repeat({self._width}, 1fr);\n"
        css += f"   grid-template-rows: repeat({self._height}, 1fr);\n"
        css += "}\n"
        
        styleSheetList.append(css)
        
        for e in self.elements:
            htmlElement, css = e.html()
            elementsAsString.append(tostring(htmlElement, method="html").decode("utf-8"))
            styleSheetList.append(css)
        
        with open(template_path, "r") as template:
            dom = template.read()
            dom = dom.replace("{{name}}", self._name)
            dom = dom.replace("{{buttons}}", "\n".join(elementsAsString))
            dom = dom.replace("{{style}}", "\n".join(styleSheetList))
            
        return dom
    
    @staticmethod
    def fromXml(xml_path : str):
        Logger.info(f"Loading layout from {xml_path}")
        with open(xml_path, "r") as f:
            xml = fromstring(f.read())
        
        if xml is None:
            raise ValueError("Invalid XML file")
        
        elements = []
        for e in xml:
            elements.append(ElementFactory.fromXml(e))
            
            name = '.'.join(os.path.basename(xml_path).split(".")[:-1])
        
        Logger.info(f"Loaded {len(elements)} elements")
        return Layout(elements, name)
