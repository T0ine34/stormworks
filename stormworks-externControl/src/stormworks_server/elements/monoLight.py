from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Color, Types, Mode
from .utils import getColorVariants, getIcon, isCustomIcon


class MonoLight(BaseElement):
    def __init__(self, channel : Channel, color : Color, position : Position, iconName = "circle"):
        super().__init__(channel, position)
        self._iconName = iconName
        self._color = color
        
    def html(self) -> Tuple[Element, str]:
        colors = getColorVariants(self._color)
        onColor = self._color.hex()
        offColor = Color(0, 0, 64).hex()
        
        container = Element("div")
        container.set("class", "mono-color light")
        container.set("data-channel", self.channel.str('b'))
        container.set("id", self.cssId)
        
        if isCustomIcon(self._iconName):
            svg = getIcon(self._iconName)
            svg.set("class", "icon svg")
            container.append(svg)
        else:
            img = Element("i")
            img.set("class", f"fas fa-{self._iconName} icon")
            container.append(img)
        
        css =  "#" + self.cssId + "{\n"
        css += f"   color: {offColor};\n"
        css += f"   stroke: {offColor};\n"
        css += f"   fill: {offColor};\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        css += "#" + self.cssId + ".active{\n"
        css += f"   color: {onColor};\n"
        css += f"   stroke: {onColor};\n"
        css += f"   fill: {onColor};\n"
        css += "}\n"
        css += "#" + self.cssId + ".active > .glow{\n"
        css += f"   box-shadow: 0 0 30px 15px {onColor};\n"
        css += "}\n"
                
        return container, css
    
    
    @staticmethod
    def fromXml(xml : Element): # <MonoLight channel="1" color="#FFFF00" col="3" row="3" width="1" height="1" icon = "hands-holding-circle"></MonoLight>
        
        elements =  {
            "channel" : xml.get("channel"),
            "color" : xml.get("color"),
            "x" : xml.get("col"),
            "y" : xml.get("row"),
            "width" : xml.get("width"),
            "height" : xml.get("height"),
            "icon" : xml.get("icon")
        }
        
        for k, v in elements.items():
            if v is None:
                raise ValueError(f"Missing {k} in light")
        
        try:
            return MonoLight(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.SIMPLE), #type: ignore
                Color.fromAuto(elements['color']), #type: ignore
                Position(
                    int(elements['x']), #type: ignore
                    int(elements['y']), #type: ignore
                    int(elements['width']), #type: ignore
                    int(elements['height']) #type: ignore
                ),
                elements['icon'] #type: ignore
            )
        except Exception as e:
            raise ValueError(f"Invalid light: {e}")
        
    def __str__(self):
        return f"Light {self._channel} {repr(self._color)} {self._position.x} {self._position.y} {self._position.width} {self._position.height} {self._iconName}"
        
    
    @property
    def type(self):
        return Types.BOOLEAN
    
    @property
    def mode(self):
        return Mode.READ