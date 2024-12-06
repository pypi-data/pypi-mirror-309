# pyColorKit

**pyColorKit** is a Python package designed to simplify color format conversions. It provides easy-to-use methods to convert between RGB, HEX, and HSL formats, with a focus on clean and modular design.

## Features
- Convert **HEX to RGB**
- Convert **RGB to HSL**
- Convert **HSL to RGB**
- Convert **RGB to HEX**
- Generate sequential colors
- Generate complimentary colors

---

## Installation

Install the package using pip:

```bash
pip install color-converter
```

---

## Usage

### Importing the Package
```python
from pycolorkit import ColorConverter, ColorGenerator
```

### Examples

#### RGB to HEX Conversion
```python
result = ColorConverter.rgb_to_hex(255, 0, 0)
print(result)  # Output: "#ff0000"
```

#### Generate a complimentary color
```python
result = ColorGenerator.compliment((0, 100, 50))
print(result)  # Output: (180, 100, 50)
```

---

## Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.