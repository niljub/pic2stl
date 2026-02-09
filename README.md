# pic2stl Image Converter

## Overview
`pic2stl` is a Python package that converts images (including PNG, JPG, and SVG) to 3D STL models. It reads an image, translates it into an optimized 3D mesh, and exports the mesh in STL format. This package is ideal for creating 3D printable models from logos, silhouettes, and other high-contrast images.

## Features
- Convert images (PNG, JPG, SVG, etc.) to 3D STL meshes.
- Optimized mesh generation (no internal faces).
- Set extrusion height for 3D models.
- Set binary threshold for image conversion.
- Optionally add a base plane.
- CLI support for easy use from the terminal.

## Installation
To use this package, ensure that you have the required dependencies installed:
```bash
pip install .
```
Dependencies include: `numpy`, `Pillow`, `trimesh`, `cairosvg`, and `scipy`. Note: `cairosvg` requires system-level `cairo` libraries to be installed.

## Usage

### Command Line Interface (CLI)
After installation, you can use the `pic2stl` command directly:
```bash
pic2stl input.png output.stl 5 --add-base --base-thickness 2
```

### Python API
```python
from pic2stl import image_to_stl

# Convert an image to STL
image_to_stl(
    image_path='input.png',
    output_path='output.stl',
    extrusion_height=3,
    add_base=True,
    base_thickness=2,
    threshold=128
)
```

#### Parameters
- **`image_path`**: Path to the input image.
- **`output_path`**: Path to save the generated STL file.
- **`extrusion_height`**: Height of the 3D model extrusion.
- **`add_base`** (Optional, default `False`): Adds a base plane if set to `True`.
- **`base_thickness`** (Optional, default `1.0`): Thickness of the base plane.
- **`invert_image`** (Optional, default `False`): Inverts the binary conversion.
- **`threshold`** (Optional, default `128`): Grayscale threshold for binary conversion (0-255).

### How It Works
1. **Load Image**: The function reads the input image. SVG files are automatically converted to temporary PNGs.
2. **Binary Conversion**: Pixels above the threshold are considered "on," and those below are "off."
3. **Mesh Creation**: A 3D mesh is generated from "on" pixels. The mesh is optimized to remove all internal walls between adjacent pixels.
4. **Optional Base**: Adds an optional base plate at the bottom. If added, the image extrusion sits on top of the base (total height = base_thickness + extrusion_height).
5. **Export to STL**: The mesh is exported to STL format using `trimesh`.

## License
This package is distributed under the MIT License.

## Contribution
Contributions are welcome. Please submit issues or pull requests to help improve this package!
