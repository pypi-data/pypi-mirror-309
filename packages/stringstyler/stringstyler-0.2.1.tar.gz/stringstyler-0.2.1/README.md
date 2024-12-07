
# stringstyler

**Add color and change the format of your strings !**

[![PyPI Version](https://img.shields.io/pypi/v/stringstyler?color=%2334D058&label=pypi%20package)](https://pypi.org/project/stringstyler/)
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://github.com/numgrade/stringstyler/blob/main/LICENSE)
![Python 3](https://img.shields.io/badge/Python%20version-3.9%2B-blue)

---

## Installation

Create and activate a virtual environment and then install stringstyler:

```console
$ pip install stringstyler

---> 100%
```

## Usage

### The print_color_text() function

```python
from stringstyler import print_styler


print_styler('Hello, World!', 'red')
print_styler('Hello, World!', 'red', style='bold')
print_styler('Hello, World!', 'green', style='underline')
print_styler('Hello, World!', 'blue', style='reverse')
print_styler('Hello, World!', 'magenta', style='invisible')
print_styler('Hello, World!', 'cyan', style='strikethrough')
```

### The text_styler decorator

```python
from stringstyler import text_styler

@text_styler(color="yellow", style="bold")
def greet(name: str):
    """Greets a person by name."""
    return f"Hello, {name}!"
```

## License

This project is licensed under the terms of the MIT license.