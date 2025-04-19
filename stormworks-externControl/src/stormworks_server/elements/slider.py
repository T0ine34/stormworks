from typing import Tuple
from xml.etree.ElementTree import Element
from .baseElement import BaseElement
from .utils import Channel, Position, Color, Direction, Input, Types, Mode
from .utils import getColorVariants


class Slider(BaseElement):
    def __init__(self, channel : Channel, color : Color, position : Position, min : int, max : int, step : int, value : int = 0, direction : Direction = Direction.RIGHT, button : bool = False, input : Input = Input(None)):
        super().__init__(channel, position)
        self._min = min
        self._max = max
        self._step = step
        self._value = value
        self._vertical = direction == Direction.UP or direction == Direction.DOWN
        self._reverse = direction == Direction.LEFT or direction == Direction.UP
        self._color = color
        self._button = button
        self._input = input
        
    def html(self) -> Tuple[Element, str]:
        # a slider is a range input, with 2 buttons, one to increase and one to decrease the value
        colors = getColorVariants(self._color)
        textColor = colors["oppositeBW"].hex()
        bgColor = self._color.hex()
        
        container = Element("div")
        
        slider = Element("input")
        slider.set("type", "range")
        slider.set("min", str(self._min))
        slider.set("max", str(self._max))
        slider.set("step", str(self._step))
        slider.set("value", str(self._value))
        
        if self._button:
            increaseBtn = Element("button")
            increaseBtn.set("id", "increase-btn")
            increaseBtn.set("class", "slider-button")
            increaseBtn.text = " "

            decreaseBtn = Element("button")
            decreaseBtn.set("id", "decrease-btn")
            decreaseBtn.set("class", "slider-button")
            decreaseBtn.text = " "
    
    
        container.set("id", self.cssId)
        container.set("data-channel", self.channel.str('n'))
        container.set("data-input", self._input.str('n'))
        if self._vertical:
            container.set("class", "vertical slider")
            if self._button:
                container.append(increaseBtn)
            container.append(slider)
            if self._button:
                container.append(decreaseBtn)
        else:
            container.set("class", "horizontal slider")
            if self._button:
                container.append(decreaseBtn)
            container.append(slider)
            if self._button:
                container.append(increaseBtn)
        
        css =  "#" + self.cssId + "{\n"
        css += f"   color: {textColor};\n"
        css += f"   grid-column: {self._position.x} / {self._position.x + self._position.width};\n"
        css += f"   grid-row: {self._position.y} / {self._position.y + self._position.height};\n"
        css += "}\n"
        css += "#" + self.cssId + " > input{\n"
        css += f"   background-color: {textColor};\n"
        css += f"   color: {bgColor};\n"
        if self._vertical:
            css += f"   writing-mode: vertical-lr;\n"
        if self._reverse:
            css += f"   direction: rtl;\n"
        css += "}\n"
        css += "#" + self.cssId + " > input::-webkit-slider-thumb{\n"
        css += f"   background-color: {bgColor};\n"
        css += "}\n"
        css += "#" + self.cssId + " > input::-moz-range-thumb{\n"
        css += f"   background-color: {bgColor};\n"
        css += "}\n"
        
        return container, css
    
    @staticmethod
    def fromXml(xml : Element):
        
        elements =  {
            "channel" : xml.get("channel"),
            "color" : xml.get("color"),
            "x" : xml.get("col"),
            "y" : xml.get("row"),
            "width" : xml.get("width"),
            "height" : xml.get("height"),
            "min" : xml.get("min"),
            "max" : xml.get("max"),
            "step" : xml.get("step"),
            "value" : xml.get("value"),
            "direction" : xml.get("direction") or "right",
            "button" : xml.get("button") or "false",
            "input" : Input.fromString(xml.get("input")) if xml.get("input") else Input(None)
        }
        
        for k, v in elements.items():
            if v is None:
                raise ValueError(f"Missing {k} in slider")
            
        try:
            return Slider(
                Channel.fromString(elements['channel']).mustBe(Channel.TYPE.SIMPLE), #type: ignore
                Color.fromAuto(elements['color']), #type: ignore
                Position(
                    int(elements['x']), #type: ignore
                    int(elements['y']), #type: ignore
                    int(elements['width']), #type: ignore
                    int(elements['height']) #type: ignore
                ),
                float(elements['min']), #type: ignore
                float(elements['max']), #type: ignore
                float(elements['step']), #type: ignore
                float(elements['value']), #type: ignore
                Direction(elements['direction']), #type: ignore
                elements['button'] == "true",
                elements['input'] #type: ignore
            )
        except Exception as e:
            raise ValueError(f"Invalid slider: {e}")
        
    def __str__(self):
        return f"Slider {self._channel} {repr(self._color)} {self._position.x} {self._position.y} {self._position.width} {self._position.height} {self._min} {self._max} {self._step} {self._value} {self._vertical}"

    @property
    def value(self):
        return self._value
    
    @property
    def type(self):
        return Types.NUMBER
    
    @property
    def mode(self):
        return Mode.WRITE
