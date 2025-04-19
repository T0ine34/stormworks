from ..colors import Color
from ..globals import CONFIG
from xml.etree.ElementTree import Element, fromstring
from enum import Enum, StrEnum
from typing import Dict
import os

def getColorVariants(color : Color) -> Dict[str, Color]:
    return {
        "oppositeBW": color.opposite().blackOrWhite(),
        "dark": color - Color(32, 32, 32, 0),
        "darkOppositeBW": (color - Color(32, 32, 32, 0)).opposite().blackOrWhite(),
    }
    
    

def getIcon(icon : str) -> Element:
    with open(CONFIG["app.path"] + "/icons/" + icon + ".svg", "r") as f:
        return fromstring(f.read())

def isCustomIcon(icon : str) -> bool:
    iconPath = CONFIG["app.path"] + "/icons/" + icon + ".svg" # type: ignore
    return os.path.exists(iconPath)

class Position:
    def __init__(self, x : int, y : int, width : int, height : int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def __str__(self):
        return f"Position({self.x}, {self.y}, {self.width}, {self.height})"


class Channel:
    class TYPE(Enum):
        SIMPLE = 0
        RGB = 1
    def __init__(self, channel1 : int, channel2 : int = -1, channel3 : int = -1):
        if channel2 != -1 and channel3 == -1 or channel2 == -1 and channel3 != -1:
            raise ValueError("Invalid channel configuration")
        self._channels = [channel1, channel2, channel3]
        self._type = Channel.TYPE.SIMPLE if channel2 == -1 else Channel.TYPE.RGB

    def __str__(self):
        match self._type:
            case Channel.TYPE.SIMPLE:
                return f"{self._channels[0]}"
            case Channel.TYPE.RGB:
                return f"{self._channels[0]}, {self._channels[1]}, {self._channels[2]}"
        
    @staticmethod
    def fromString(channel : str):
        channels = channel.split(",")
        if len(channels) == 1:
            return Channel(int(channels[0]))
        elif len(channels) == 3:
            return Channel(int(channels[0]), int(channels[1]), int(channels[2]))
        else:
            raise ValueError("Invalid channel configuration")
        
    def mustBe(self, type : TYPE):
        if self._type != type:
            raise ValueError(f"Channel must be of type {type}")
        return self
    
    def str(self, prefix : str):
        match self._type:
            case Channel.TYPE.SIMPLE:
                return f"{prefix}{self._channels[0]}"
            case Channel.TYPE.RGB:
                return f"{prefix}{self._channels[0]}, {prefix}{self._channels[1]}, {prefix}{self._channels[2]}"
                
                

class Direction(StrEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    
class Input:
    class Origin(Enum):
        INPUT = 0
        OUTPUT = 1
    
        @staticmethod
        def fromString(input : str):
            return Input.Origin[input.upper()]
        
    def __init__(self, origin : Origin|None, channel : Channel = Channel(0)):
        self._origin = origin
        self._channel = channel
        
    def str(self, prefix : str):
        if self._origin is None:
            return "none"
        return f"{self._origin.name.lower()}:{self._channel.str(prefix)}"
    
    def __str__(self):
        if self._origin is None:
            return "none"
        return f"{self._origin.name} {self._channel}"
    
    @staticmethod
    def fromString(input : str):
        if input == "none":
            return Input(None)
        parts = input.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid input string")
        return Input(Input.Origin.fromString(parts[0]), Channel.fromString(parts[1]))
    

class Types(StrEnum):
    UNDEFINED = "/"
    BOOLEAN = "b"
    NUMBER = "n"
    # below is not used
    COMPOSITE = "c"
    SOUND = "s"
    IMAGE = "i"
    TEXT = "t"
    
class Mode(Enum):
    UNDEFINED = 0
    WRITE = 1
    READ = 2