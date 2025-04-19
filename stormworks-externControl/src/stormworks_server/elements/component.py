from uuid import uuid4 as uuid
from xml.etree.ElementTree import Element
from typing import Tuple
from abc import ABC, abstractmethod
from .utils import Types, Mode

class Component(ABC):
    """
    Base class for all components, including groups and elements.
    """
    def __init__(self):
        self._uid = uuid()
        
    @property
    def uid(self):
        return self._uid
    
    @property
    def cssId(self) -> str:
        return f"{self.__class__.__name__.lower()}-{self.uid}"
    
    @property
    def type(self) -> Types:
        return Types.UNDEFINED
    
    @property
    def mode(self) -> Mode:
        return Mode.UNDEFINED
    
    @property
    def hasChildren(self) -> bool:
        return False
    
    @abstractmethod
    def html(self) -> Tuple[Element, str]:
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod
    def fromXml(xml : Element):
        raise NotImplementedError()
    