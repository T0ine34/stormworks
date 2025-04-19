from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Types, Mode
from ..colors import Color


class Keypad(BaseElement):
    def __init__(self, channel : Channel, position : Position, color : Color, decimal : bool, value : str = "0", min : int|None = None, max : int|None = None):
        super().__init__(channel, position)
        self._negative = min is not None and float(min) < 0
        self._decimal = decimal
        self._value = value
        self._color = color
        self._min = min
        self._max = max


    def __createButton(self, value : str, id : str|None = None) -> Element:
        button = Element("button")
        button.set("class", "keypad-button")
        if id is not None:
            button.set("id", id)
        button.set("data-value", value)
        
        icon = Element("i")
        icon.set("class", "fas fa-" + value)
        button.append(icon)
                
        return button
    
    
        
    def html(self) -> Tuple[Element, str]:
        
        # ___ <
        # 7 8 9
        # 4 5 6
        # 1 2 3
        # - 0 .
        
        container = Element("div")
        container.set("id", self.cssId)
        container.set("data-channel", self.channel.str('n'))
        container.set("class", "keypad")
        container.set("data-min", str(self._min))
        container.set("data-max", str(self._max))
        
        # create the number display
        display = Element("div")
        display.set("class", "keypad-display")
        display.text = self._value
        container.append(display)
        
        container.append(self.__createButton("backspace"))
        container.append(self.__createButton("7"))
        container.append(self.__createButton("8"))
        container.append(self.__createButton("9"))
        container.append(self.__createButton("4"))
        container.append(self.__createButton("5"))
        container.append(self.__createButton("6"))
        container.append(self.__createButton("1"))
        container.append(self.__createButton("2"))
        container.append(self.__createButton("3"))
        if self._negative:
            container.append(self.__createButton("minus"))
        container.append(self.__createButton("0", "zero"))
        if self._decimal:
            container.append(self.__createButton("circle", "decimal"))

        css =  "#" + self.cssId + "{\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        css += "#" + self.cssId + " .keypad-display{\n"
        css += f"   color: {self._color.hex()};\n"
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
            "color" : xml.get("color"),
            "decimal" : xml.get("decimal"),
            "max" : xml.get("max", None),
            "min" : xml.get("min", None),
            "value" : xml.get("value", "0")
        }
        
        if elements['max'] is not None and elements['min'] is not None and float(elements['max']) < float(elements['min']):
            raise ValueError("Max value must be greater than min value")
        
        elements['value'] = max(elements['min'], min(elements['max'], elements['value']))
        
        for k, v in elements.items():
            if v is None:
                raise ValueError(f"Missing {k} in keypad")
        
        try:
            return Keypad(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.SIMPLE), #type: ignore
                Position(
                    int(elements['x']), #type: ignore
                    int(elements['y']), #type: ignore,
                    int(elements['width']), #type: ignore
                    int(elements['height']) #type: ignore
                ),
                Color.fromAuto(elements['color']), #type: ignore
                elements['decimal'].lower() == "true", #type: ignore
                elements['value'], #type: ignore
                elements['min'], #type: ignore
                elements['max'] #type: ignore
            )
        except ValueError as e:
            raise ValueError(f"Error in keypad: {e}") from None
        
    @property
    def type(self) -> Types:
        return Types.NUMBER
        
    @property
    def value(self):
        return self._value
        
    @property
    def mode(self):
        return Mode.WRITE
        
    def __str__(self):
        return f"Keypad {self._channel} {repr(self._color)} {self._position.x} {self._position.y} {self._position.width} {self._position.height} {self._decimal} {self._value} {self._min} {self._max}"