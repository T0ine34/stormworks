from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Types, Mode
from .utils import getIcon, isCustomIcon


class RGBLight(BaseElement):
    def __init__(self, channel : Channel, position : Position, iconName = "circle"):
        super().__init__(channel, position)
        self._iconName = iconName

    def html(self) -> Tuple[Element, str]:
        
        container = Element("div")
        container.set("class", "rgb-color light")
        container.set("data-channel", self.channel.str('n'))
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
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        
        return container, css
    
    
    @staticmethod
    def fromXml(xml : Element): # <RGBLight channel="1" col="3" row="3" width="1" height="1" icon = "hands-holding-circle"></RGBLight>
        
        elements =  {
            "channel" : xml.get("channel"),
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
            return RGBLight(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.RGB), #type: ignore
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
        

    @property
    def type(self) -> Types:
        return Types.NUMBER

    @property
    def mode(self) -> Mode:
        return Mode.READ
    
    def __str__(self):
        return f"RGBLight {self.channel} {self._position} {self._iconName}"