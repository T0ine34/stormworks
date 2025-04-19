import re
class Color:
    def __init__(self, r : int, g : int, b : int, a : int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
    @staticmethod
    def fromHex(hex : str):
        if hex[0] == "#":
            hex = hex[1:]
        
        r, g, b, a = 0, 0, 0, 255    
        
        if len(hex) == 3: #RGB
            r = int(hex[0] * 2, 16)
            g = int(hex[1] * 2, 16)
            b = int(hex[2] * 2, 16)
        elif len(hex) == 4: #RGBA
            r = int(hex[0] * 2, 16)
            g = int(hex[1] * 2, 16)
            b = int(hex[2] * 2, 16)
            a = int(hex[3] * 2, 16)
        elif len(hex) == 6: #RRGGBB
            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
        elif len(hex) == 8: #RRGGBBAA
            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
            a = int(hex[6:8], 16)
        else:
            raise ValueError(f"Invalid hex color: {hex}")
        return Color(r, g, b, a)
    
    @staticmethod
    def fromRgb(rgb : str): # r,g,b,a or r,g,b
        return Color(*[int(x) for x in rgb.split(",")])

    
    @staticmethod
    def fromAuto(color : str) -> "Color":
        """Converts a color string to a Color object, support hex, rgb and hsl formats (with or without alpha channel)

        Args:
            color (str): The color string

        Raises:
            ValueError: If the color string is invalid

        Returns:
            Color: The Color object
        """
        if re.match(r"^#[0-9a-fA-F]{3,8}$", color):
            return Color.fromHex(color)
        if color.startswith("rgba") or color.startswith("RGBA"):
            return Color.fromRgb(color[5:-1])
        if color.startswith("rgb") or color.startswith("RGB"):
            return Color.fromRgb(color[4:-1])
        if re.match(r"^\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*\d+\s*)?$", color):
            return Color.fromRgb(color)
        raise ValueError(f"Invalid color: {color}")
    
    
    def __str__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"
    
    def opposite(self):
        return Color(255 - self.r, 255 - self.g, 255 - self.b, self.a)
    
    def grayshade(self):
        gray = round(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
        return Color(gray, gray, gray, self.a)
    
    def blackOrWhite(self):
        if self.r < 200 \
        or self.g < 200 \
        or self.b < 55:
            return Color(0, 0, 0, self.a)
        return Color(255, 255, 255, self.a)
    
    def hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"
    
    def rgb(self):
        return f"rgb({self.r}, {self.g}, {self.b})"
    
    def rgba(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"
        
    
    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __add__(self, other):
        r = max(0, min(255, self.r + other.r))
        g = max(0, min(255, self.g + other.g))
        b = max(0, min(255, self.b + other.b))
        a = max(0, min(255, self.a + other.a))
        return Color(r, g, b, a)
    
    def __sub__(self, other):
        r = max(0, min(255, self.r - other.r))
        g = max(0, min(255, self.g - other.g))
        b = max(0, min(255, self.b - other.b))
        a = max(0, min(255, self.a - other.a))
        return Color(r, g, b, a)
    
    def __repr__(self):
        return f"\033[38;2;{self.r};{self.g};{self.b}mColor({self.r} {self.g} {self.b} {self.a})\033[0m"
    
    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))