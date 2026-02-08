import numpy as np
from PIL import Image
import trimesh
import cairosvg
import os
import tempfile
import argparse

def svg_to_png(svg_path, png_path):
    """Converts an SVG file to a PNG file."""
    cairosvg.svg2png(url=svg_path, write_to=png_path)

def image_to_stl(image_path, output_path, extrusion_height, add_base=False, base_thickness=1.0, invert_image=False, threshold=128):
    """
    Converts an image to a 3D STL model.
    
    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the generated STL file.
        extrusion_height (float): Height of the 3D model extrusion.
        add_base (bool): Whether to add a base plane.
        base_thickness (float): Thickness of the base plane.
        invert_image (bool): Whether to invert the binary image.
        threshold (int): Grayscale threshold for binary conversion (0-255).
    """
    temp_png = None
    # Handle SVG files by converting to a temporary PNG
    if str(image_path).lower().endswith('.svg'):
        temp_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        svg_to_png(image_path, temp_png)
        actual_image_path = temp_png
    else:
        actual_image_path = image_path

    try:
        # Load the image and convert to grayscale
        img = Image.open(actual_image_path).convert('L')

        # Convert to a binary image based on threshold
        img = img.point(lambda p: 1 if p > threshold else 0, mode='1')

        # Convert the image to a numpy array
        if invert_image:
            array = 1 - np.array(img)
        else:
            array = np.array(img)

        # Get dimensions
        height, width = array.shape
        
        vertices = []
        faces = []
        vert_map = {}

        def get_vert(x, y, z):
            # Round to avoid floating point issues with dictionary keys
            key = (round(float(x), 6), round(float(y), 6), round(float(z), 6))
            if key not in vert_map:
                vert_map[key] = len(vertices)
                vertices.append([float(x), float(y), float(z)])
            return vert_map[key]

        # Determine Z levels
        z0 = float(base_thickness) if add_base else 0.0
        z1 = z0 + float(extrusion_height)
        
        # Optimization: Only create faces for "on" pixels and avoid internal walls
        for y in range(height):
            for x in range(width):
                if array[y, x] == 1:
                    # Top vertices (Z = z1)
                    v1t = get_vert(x, y, z1)
                    v2t = get_vert(x + 1, y, z1)
                    v3t = get_vert(x + 1, y + 1, z1)
                    v4t = get_vert(x, y + 1, z1)

                    # Bottom vertices (Z = z0)
                    v1b = get_vert(x, y, z0)
                    v2b = get_vert(x + 1, y, z0)
                    v3b = get_vert(x + 1, y + 1, z0)
                    v4b = get_vert(x, y + 1, z0)

                    # Top face
                    faces.append([v1t, v2t, v3t])
                    faces.append([v1t, v3t, v4t])

                    # Bottom face
                    faces.append([v1b, v3b, v2b])
                    faces.append([v1b, v4b, v3b])

                    # Side faces: only create if there's no adjacent "on" pixel
                    # Left (x-1)
                    if x == 0 or array[y, x-1] == 0:
                        faces.append([v1t, v4t, v4b])
                        faces.append([v1t, v4b, v1b])
                    # Right (x+1)
                    if x == width - 1 or array[y, x+1] == 0:
                        faces.append([v2t, v2b, v3b])
                        faces.append([v2t, v3b, v3t])
                    # Top (y-1)
                    if y == 0 or array[y-1, x] == 0:
                        faces.append([v1t, v1b, v2b])
                        faces.append([v1t, v2b, v2t])
                    # Bottom (y+1)
                    if y == height - 1 or array[y+1, x] == 0:
                        faces.append([v4t, v3t, v3b])
                        faces.append([v4t, v3b, v4b])

        # Add base plate if requested
        if add_base:
            # Base plate from z=0 to z=base_thickness covering the whole image area
            b1b = get_vert(0, 0, 0)
            b2b = get_vert(width, 0, 0)
            b3b = get_vert(width, height, 0)
            b4b = get_vert(0, height, 0)

            b1t = get_vert(0, 0, base_thickness)
            b2t = get_vert(width, 0, base_thickness)
            b3t = get_vert(width, height, base_thickness)
            b4t = get_vert(0, height, base_thickness)

            # Base bottom face
            faces.append([b1b, b3b, b2b])
            faces.append([b1b, b4b, b3b])
            # Base top face
            faces.append([b1t, b2t, b3t])
            faces.append([b1t, b3t, b4t])
            # Base side faces
            # Left
            faces.append([b1t, b4t, b4b])
            faces.append([b1t, b4b, b1b])
            # Right
            faces.append([b2t, b2b, b3b])
            faces.append([b2t, b3b, b3t])
            # Top
            faces.append([b1t, b1b, b2b])
            faces.append([b1t, b2b, b2t])
            # Bottom
            faces.append([b4t, b3t, b3b])
            faces.append([b4t, b3b, b4b])

        # Create the mesh using trimesh
        if not vertices or not faces:
            # Handle empty mesh case
            mesh_obj = trimesh.Trimesh()
        else:
            mesh_obj = trimesh.Trimesh(vertices=vertices, faces=faces)
            # Basic cleanup
            mesh_obj.update_faces(mesh_obj.unique_faces())

        # Export the mesh to STL format
        mesh_obj.export(output_path)
        
    finally:
        # Clean up temporary PNG file if it was created
        if temp_png and os.path.exists(temp_png):
            os.remove(temp_png)

def main():
    parser = argparse.ArgumentParser(description='Convert an image to a 3D STL model.')
    parser.add_argument('image_path', help='Path to the input image (PNG, JPG, SVG, etc.)')
    parser.add_argument('output_path', help='Path to save the generated STL file')
    parser.add_argument('extrusion_height', type=float, help='Height of the 3D model extrusion')
    parser.add_argument('--add-base', action='store_true', help='Add a base plane to the model')
    parser.add_argument('--base-thickness', type=float, default=1.0, help='Thickness of the base plane (default: 1.0)')
    parser.add_argument('--invert-image', action='store_true', help='Invert the image (extrude dark pixels instead of bright ones)')
    parser.add_argument('--threshold', type=int, default=128, help='Grayscale threshold for binary conversion (0-255, default: 128)')
    
    args = parser.parse_args()
    
    image_to_stl(
        args.image_path,
        args.output_path,
        args.extrusion_height,
        add_base=args.add_base,
        base_thickness=args.base_thickness,
        invert_image=args.invert_image,
        threshold=args.threshold
    )

if __name__ == '__main__':
    main()
