from enum import Enum
import colorsys
from pryttier.math import Vector3

class RGB:
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
        self.r = r
        self.g = g
        self.b = b
        self._normalized = False

    def __repr__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def normalize(self) -> None:
        self._normalized = True
        self.r /= 255
        self.g /= 255
        self.b /= 255
        self.rgb = (self.r, self.g, self.b)

    def denormalize(self) -> None:
        self._normalized = False
        self.r *= 255
        self.g *= 255
        self.b *= 255
        self.rgb = (self.r, self.g, self.b)

    def complement(self):
        if self._normalized:
            return RGB(1 - self.r, 1 - self.g, 1 - self.b)
        else:
            return RGB(255 - self.r, 255 - self.g, 255 - self.b)

    def toVector(self):
        return Vector3(self.r, self.g, self.b)


class AnsiColor:
    def __init__(self, colorCode: int):
        self.code = f"\033[{colorCode}m"

    @property
    def value(self):
        return self.code


class AnsiRGB:
    def __init__(self, rgb: RGB | tuple[int, int, int]):
        if isinstance(rgb, RGB):
            self.code = f"\u001b[38;2;{rgb.r};{rgb.g};{rgb.b}m"
        elif isinstance(rgb, tuple):
            self.code = f"\u001b[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @property
    def value(self):
        return self.code


class AnsiRGB_BG:
    def __init__(self, rgb: RGB | tuple[int, int, int]):
        if isinstance(rgb, RGB):
            self.code = f"\u001b[48;2;{rgb.r};{rgb.g};{rgb.b}m"
        elif isinstance(rgb, tuple):
            self.code = f"\u001b[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    @property
    def value(self):
        return self.code


class AnsiColors(Enum):
    BLACK = AnsiColor(30)
    RED = AnsiColor(31).value
    GREEN = AnsiColor(32).value
    YELLOW = AnsiColor(33).value  # orange on some systems
    BLUE = AnsiColor(34).value
    MAGENTA = AnsiColor(35).value
    CYAN = AnsiColor(36).value
    LIGHT_GRAY = AnsiColor(37).value
    DARK_GRAY = AnsiColor(90).value
    BRIGHT_RED = AnsiColor(91).value
    BRIGHT_GREEN = AnsiColor(92).value
    BRIGHT_YELLOW = AnsiColor(93).value
    BRIGHT_BLUE = AnsiColor(94).value
    BRIGHT_MAGENTA = AnsiColor(95).value
    BRIGHT_CYAN = AnsiColor(96).value
    WHITE = AnsiColor(97).value

    RESET = '\033[0m'  # called to return to standard terminal text color


def coloredText(text: str, color: AnsiColors | AnsiColor | AnsiRGB | AnsiRGB_BG, reset: bool = True) -> str:
    if reset:
        text = color.value + text + AnsiColors.RESET.value
    elif not reset:
        text = color.value + text

    return text
