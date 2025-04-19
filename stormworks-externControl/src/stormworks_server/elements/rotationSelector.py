from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .component import Component
from .factory import ElementFactory
from .utils import Channel, Position, Direction, Input, Types, Mode


class RotationSelector(BaseElement):    
    def __init__(self, channel : Channel, position : Position, insideElement : Component, min : int = 0, max : int = 1, innerRotation : int = 0, neutral : Direction = Direction.UP, input : Input = None):
        super().__init__(channel, position)
        self._negative = min is not None and float(min) < 0
        self._insideElement = insideElement
        self._min = min
        self._max = max
        self._innerRotation = innerRotation
        self._neutral = neutral
        self._input = input
        
    def html(self) -> Tuple[Element, str]:
        
        container = Element("div")
        container.set("id", self.cssId)
        container.set("data-channel", self.channel.str('n'))
        container.set("data-input", self._input.str('n'))
        container.set("class", "rotation-selector")
        container.set("data-min", str(self._min))
        container.set("data-max", str(self._max))
        container.set("data-neutral", self._neutral.value)
        
        bounds_inner = Element("div")
        bounds_inner.set("class", "bounds-inner")
        container.append(bounds_inner)
        
        
        a = Element("div")
        a.set("class", "a")
        bounds_inner.append(a)
        
        rotator = Element("div")
        rotator.set("class", "rotator")
        a.append(rotator)
        
        htmlElement, css = self._insideElement.html()
        rotator.append(htmlElement)

        css += f"#{self.cssId}" + "{\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        
        css += f"#{self._insideElement.cssId}" + "{\n"
        css += f"   grid-column: 1 / 2;\n"
        css += f"   grid-row: 1 / 2;\n"
        css += f"   transform: rotate({self._innerRotation}deg);\n"
        css += "}\n"
        
        return container, css
    

    @staticmethod
    def fromXml(xml : Element): # <Keypad channel="3" color="#FF0000" col="4" row="1" width="2" height="3" decimal="false" max="32" min = "1"></Keypad>
        
        elements =  {
            "channel" : xml.get("channel"),
            "x" : xml.get("col"),
            "y" : xml.get("row"),
            "width" : xml.get("width"),
            "height" : xml.get("height"),
            "min" : xml.get("min"),
            "max" : xml.get("max"),
            "innerRotation" : xml.get("innerRotation"),
            "neutral" : xml.get("neutral"),
            "input" : xml.get("input")
        }
        
        insideElement = None
        if len(xml) == 1:
            insideElement = ElementFactory.fromXml(xml[0])
        else:
            raise ValueError("Invalid XML; RotationSelector must have exactly one child")
        
        try:
            return RotationSelector(
                Channel.fromString(elements["channel"]),
                Position(
                    int(elements["x"]),
                    int(elements["y"]),
                    int(elements["width"]),
                    int(elements["height"])
                ),
                insideElement,
                int(elements["min"]) if elements["min"] is not None else 0,
                int(elements["max"]) if elements["max"] is not None else 1,
                int(elements["innerRotation"]) if elements["innerRotation"] is not None else 0,
                Direction(elements["neutral"]) if elements["neutral"] is not None else Direction.UP,
                Input.fromString(elements["input"] if elements["input"] is not None else "none")
            )
        except ValueError as e:
            raise ValueError(f"Error in RotationSelector: {e}") from None
        
    @property
    def type(self) -> Types:
        return Types.NUMBER
    
    @property
    def value(self):
        return 0
        
    @property
    def mode(self) -> Mode:
        return Mode.WRITE
    
    @property
    def hasChildren(self):
        return True
    
    @property
    def children(self):
        return [self._insideElement]
    
    def __str__(self):
        return f"RotationSelector {self.channel} {self._position} {self._min} {self._max} {self._innerRotation} {self._neutral} {self._input}"