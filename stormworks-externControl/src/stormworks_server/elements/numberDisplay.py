from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Types, Mode
from ..colors import Color

class NumberDisplay(BaseElement):
    def __init__(self, channel : Channel, position : Position, color : Color, decimal : bool):
        super().__init__(channel, position)
        self._color = color
        self._decimal = decimal

    def html(self) -> Tuple[Element, str]:
        container = Element('div')
        container.set('class', 'number-display')
        container.set('data-channel', self.channel.str('n'))
        container.set('id', self.cssId)
        container.set('data-decimal', 'true' if self._decimal else 'false')

        display = Element('div')
        display.set('class', 'display')
        container.append(display)
        
        css =  f"#{self.cssId}" + "{\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        # css += f"#number-display-{self.uid} .display" + "{\n"
        css += "#" + self.cssId + " .display{\n"
        css += f"   color: {self._color.hex()};\n"
        css += "}\n"
        
        return container, css
    
    @staticmethod
    def fromXml(xml : Element) -> 'NumberDisplay': # <NumberDisplay channel="1" col="3" row="3" width="1" height="1" decimal="false" color="#ff0000"></NumberDisplay>
        elements =  {
            "channel" : xml.get("channel"),
            "x" : xml.get("col"),
            "y" : xml.get("row"),
            "width" : xml.get("width"),
            "height" : xml.get("height"),
            "color" : xml.get("color"),
            "decimal" : xml.get("decimal"),
        }
        
        for k, v in elements.items():
            if v is None:
                raise ValueError(f"Missing {k} in numberDisplay")
        
        try:
            return NumberDisplay(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.SIMPLE), #type: ignore
                Position(
                    int(elements['x']), #type: ignore
                    int(elements['y']), #type: ignore,
                    int(elements['width']), #type: ignore
                    int(elements['height']) #type: ignore
                ),
                Color.fromAuto(elements['color']), #type: ignore
                elements['decimal'] == 'true' #type: ignore
            )
        except ValueError as e:
            raise ValueError(f"Error in numberDisplay: {e}") from None

    @property
    def type(self) -> Types:
        return Types.NUMBER
    
    @property
    def mode(self) -> Mode:
        return Mode.READ
    
    def __str__(self):
        return f"NumberDisplay {self._channel} {repr(self._color)} {self._position.x} {self._position.y} {self._position.width} {self._position.height} {self._decimal}"