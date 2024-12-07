"""This module provides:

- a function to print colored text to the console.
- a decorator to print colored text to the console.
"""

from functools import wraps
import string
from typing import Callable, Optional


TEMPLATE = string.Template("\033[${code}m")
RESET = TEMPLATE.substitute(code="0")


style_codes = {
    "bold": "01",
    "disable": "02",
    "underline": "04",
    "reverse": "07",
    "invisible": "08",
    "strikethrough": "09",
}

color_codes_fg = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}


def print_styler(
    text: str, color: str = "white", style: Optional[str] = None, **kwargs
) -> None:
    """Prints colored text to the console.

    Args:
        text: A string to be printed.
        color: A string specifying the color of the text. The color can be one
            of the following: 'black', 'red', 'green', 'yellow', 'blue',
            'magenta', 'cyan', 'white'.
        style: A string specifying the style of the text. The style can be one
            of the following: 'bold', 'disable', 'underline', 'reverse',
            'invisible', 'strikethrough'.
        kwargs: Additional keyword arguments to be passed to the print function.
    """
    color_code = color_codes_fg.get(color, color_codes_fg[color])
    end = RESET
    if style:
        style_code = style_codes.get(style, style_codes[style])
        # We can merge the style and color codes by separating them with a semicolon.
        start = TEMPLATE.substitute(code=f"{style_code};{color_code}")
    else:
        start = TEMPLATE.substitute(code=color_code)
    print(f"{start}{text}{end}", **kwargs)


def text_styler(color: str = "white", style: Optional[str] = None) -> Callable:
    """Decorator to return colored text.

    Args:
        color: A string specifying the color of the text. The color can be one
            of the following: 'black', 'red', 'green', 'yellow', 'blue',
            'magenta', 'cyan', 'white'.
        style: A string specifying the style of the text. The style can be one
            of the following: 'bold', 'disable', 'underline', 'reverse',
            'invisible', 'strikethrough'.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            color_code = color_codes_fg.get(color, color_codes_fg[color])
            end = RESET
            if style:
                style_code = style_codes.get(style, style_codes[style])
                # We can merge the style and color codes by separating them with a semicolon.
                start = TEMPLATE.substitute(code=f"{style_code};{color_code}")
            else:
                start = TEMPLATE.substitute(code=color_code)
            return f"{start}{text}{end}"

        return wrapper

    return decorator


if __name__ == "__main__":
    print_styler("Hello, World!", "red")
    print_styler("Hello, World!", "red", style="bold")
    print_styler("Hello, World!", "green", style="underline")
    print_styler("Hello, World!", "blue", style="reverse")
    print_styler("Hello, World!", "magenta", style="invisible")
    print_styler("Hello, World!", "cyan", style="strikethrough")

    # Using the decorator
    @text_styler(color="yellow", style="bold")
    def greet(name: str):
        """Greets a person by name."""
        return f"Hello, {name}!"

    print(greet("Alice"))
    # help(greet)
    # classic print
    print("\033[31m  text \033[0m")
