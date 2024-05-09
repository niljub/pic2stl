import numpy as np
from PIL import Image
from stl import mesh
from scipy.spatial import cKDTree


def image_to_stl(image_path, output_path, extrusion_height, add_base=False, base_thickness=1):
    # Load the image and convert to grayscale
    img = Image.open(image_path).convert('L')
    
    # Convert to a binary image
    threshold = 128
    img = img.point(lambda p: 1 if p > threshold else 0, mode='1')
    
    # Convert the image to a numpy array
    array = np.array(img)

    
    # Get dimensions
    height, width = array.shape
    
    # List to hold the mesh vertices and faces
    vertices = []
    faces = []
    
    # Create the mesh
    for y in range(height):
        for x in range(width):
            if array[y, x] == 1:
                # Create vertices for the current block
                start_x = x
                start_y = y
                end_x = x + 1
                end_y = y + 1
                z_top = extrusion_height
                z_bottom = 0
                
                # Vertices of the prism
                current_vertices = [
                    [start_x, start_y, z_bottom], [end_x, start_y, z_bottom], [end_x, end_y, z_bottom], [start_x, end_y, z_bottom],  # Bottom vertices
                    [start_x, start_y, z_top], [end_x, start_y, z_top], [end_x, end_y, z_top], [start_x, end_y, z_top]  # Top vertices
                ]
                
                v_offset = len(vertices)
                vertices.extend(current_vertices)
                
                # Faces of the prism (each face consists of two triangles)
                current_faces = [
                    [v_offset, v_offset + 1, v_offset + 2], [v_offset, v_offset + 2, v_offset + 3],  # Bottom face
                    [v_offset + 4, v_offset + 5, v_offset + 6], [v_offset + 4, v_offset + 6, v_offset + 7],  # Top face
                    [v_offset, v_offset + 1, v_offset + 5], [v_offset, v_offset + 5, v_offset + 4],  # Side faces
                    [v_offset + 1, v_offset + 2, v_offset + 6], [v_offset + 1, v_offset + 6, v_offset + 5],
                    [v_offset + 2, v_offset + 3, v_offset + 7], [v_offset + 2, v_offset + 7, v_offset + 6],
                    [v_offset + 3, v_offset, v_offset + 4], [v_offset + 3, v_offset + 4, v_offset + 7]
                ]
                faces.extend(current_faces)

    # Optionally add a base plane for better adhesion
    if add_base:
        base_vertices = [
            [0, 0, 0], [width, 0, 0], [width, height, 0], [0, height, 0],
            [0, 0, base_thickness], [width, 0, base_thickness], [width, height, base_thickness], [0, height, base_thickness]
        ]
        
        base_offset = len(vertices)
        vertices.extend(base_vertices)
        
        base_faces = [
            [base_offset, base_offset + 1, base_offset + 2], [base_offset, base_offset + 2, base_offset + 3],  # Bottom face
            [base_offset + 4, base_offset + 5, base_offset + 6], [base_offset + 4, base_offset + 6, base_offset + 7],  # Top face
            [base_offset, base_offset + 1, base_offset + 5], [base_offset, base_offset + 5, base_offset + 4],  # Side faces
            [base_offset + 1, base_offset + 2, base_offset + 6], [base_offset + 1, base_offset + 6, base_offset + 5],
            [base_offset + 2, base_offset + 3, base_offset + 7], [base_offset + 2, base_offset + 7, base_offset + 6],
            [base_offset + 3, base_offset, base_offset + 4], [base_offset + 3, base_offset + 4, base_offset + 7]
        ]
        faces.extend(base_faces)
    
    # Create the mesh
    vertices = np.array(vertices)
    faces = np.array(faces)
    output_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            output_mesh.vectors[i][j] = vertices[f[j]]
    
    # Write to file
    output_mesh.save(output_path)

# Example usage
image_to_stl('transparent.webp', 'output.stl', extrusion_height=3, add_base=False, base_thickness=1)


