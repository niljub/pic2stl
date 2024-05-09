# pic2stl Image Converter

## Overview
`pic2stl` is a Python package that converts images to 3D STL models. It reads an image, translates it into a 3D mesh, and exports the mesh in STL format. This package is ideal for creating 3D printable models from logos, silhouettes, and other high-contrast images.

## Features
- Convert images to 3D STL meshes
- Set extrusion height for 3D models
- Optionally add a base plane for enhanced model adhesion
- Compatible with any mainstream image format

## Installation
To use this package, ensure that you have the required dependencies installed:
```bash
pip install numpy Pillow numpy-stl scipy
```

## Usage
### Function
```python
def image_to_stl(image_path, output_path, extrusion_height, add_base=False, base_thickness=0)
```
#### Parameters
- **`image_path`**: Path to the input image.
- **`output_path`**: Path to save the generated STL file.
- **`extrusion_height`**: Height of the 3D model extrusion.
- **`add_base`** (Optional, default `False`): Adds a base plane if set to `True`.
- **`base_thickness`** (Optional, default `1`): Thickness of the base plane.

### Example
```python
# Convert an image to STL
image_to_stl('path/to/input_image.png', 'output.stl', extrusion_height=3, add_base=True, base_thickness=2)
```

### How It Works
1. **Load Image**: The function reads the input image and converts it to grayscale if needed.
2. **Binary Conversion**: Pixels above a specific threshold are considered "on," and those below are "off."
3. **Mesh Creation**: A 3D mesh is generated based on the "on" pixels, extruding vertically.
4. **Optional Base**: Adds an optional base to the bottom of the model for stability.
5. **Export to STL**: The mesh is then exported to STL format.

## License
This package is distributed under the MIT License.

## Contribution
Contributions are welcome. Please submit issues or pull requests to help improve this package!

