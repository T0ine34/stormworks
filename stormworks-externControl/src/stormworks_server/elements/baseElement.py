from .utils import Channel, Position
from .component import Component
class BaseElement(Component):
    def __init__(self, channel : Channel, position : Position):
        super().__init__()
        self._channel = channel
        self._position = position
    
    @property
    def channel(self):
        return self._channel
    
    @property
    def position(self):
        return self._position
