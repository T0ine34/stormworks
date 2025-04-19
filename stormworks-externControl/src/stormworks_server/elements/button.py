from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Color, Input, Types, Mode
from .utils import getIcon, isCustomIcon


class Button(BaseElement):
    def __init__(self, channel : Channel, color : Color, position : Position, icon : str, toggle : bool = False, input : Input = Input(None)):
        super().__init__(channel, position)
        self._toggle = toggle
        self._color = color
        self._icon = icon
        self._input = input
        
    def html(self) -> Tuple[Element, str]:
        
        onColor = self._color.hex()
        offColor = Color(0, 0, 64).hex()
        
        button = Element("button")
        button.set("class", "button")
        button.set("data-toggle", str(self._toggle).lower())
        button.set("data-channel", self.channel.str('b'))
        button.set("data-input", self._input.str('b'))
        button.set("id", self.cssId)

        if isCustomIcon(self._icon):
            svg = getIcon(self._icon)
            svg.set("class", "icon svg")
            button.append(svg)
        else:
            img = Element("i")
            img.set("class", f"fas fa-{self._icon} icon")
            button.append(img)
        
        css =  "#" + self.cssId + "{\n"
        css += f"   color: {offColor};\n"
        css += f"   fill: {offColor};\n"
        css += f"   stroke: {offColor};\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        css += "#" + self.cssId + ".active{\n"
        css += f"   color: {onColor};\n"
        css += f"   fill: {onColor};\n"
        css += f"   stroke: {onColor};\n"
        css += "}\n"
        
        return button, css
    
    @staticmethod
    def fromXml(xml : Element):
        
        elements =  {
            "channel" : xml.get("channel"),
            "icon" : xml.get("icon"),
            "color" : xml.get("color"),
            "x" : xml.get("col"),
            "y" : xml.get("row"),
            "width" : xml.get("width"),
            "height" : xml.get("height"),
            "toggle" : xml.get("toggle"),
            "input" : xml.get("input") or None
        }
        
        for k, v in elements.items():
            if v is None:
                raise ValueError(f"Missing {k} in button")

        try:            
            return Button(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.SIMPLE),
                Color.fromAuto(elements['color']),
                Position(
                    int(elements['x']),
                    int(elements['y']),
                    int(elements['width']),
                    int(elements['height'])
                ),
                elements['icon'],
                elements['toggle'] == "true",
                Input.fromString(elements['input'] if elements["input"] is not None else "none")
            )
        except Exception as e:
            raise ValueError(f"Invalid button: {e}")
        
    def __str__(self):
        return f"Button {self._channel} {repr(self._color)} {self._position.x} {self._position.y} {self._position.width} {self._position.height} {self._icon} {self._toggle}"

    @property
    def type(self):
        return Types.BOOLEAN
    
    @property
    def mode(self):
        return Mode.WRITE