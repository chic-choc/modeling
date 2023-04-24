
'''
import numpy as np
import open3d as o3d

def load_obj_file(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def add_random_noise(mesh, noise_strength=0.02):
    vertices = np.asarray(mesh.vertices)
    noise = np.random.normal(0, noise_strength, size=vertices.shape)
    vertices += noise

    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    return mesh

def save_obj_file(mesh, output_file_path):
    o3d.io.write_triangle_mesh(output_file_path, mesh)

input_file = 'model.obj'
output_file = 'noisy_model.obj'

mesh = load_obj_file(input_file)
mesh_with_noise = add_random_noise(mesh)
save_obj_file(mesh_with_noise, output_file)

'''

import numpy as np
import open3d as o3d

def load_obj_file(file_path):
    mesh = o3d.io.read_triangle_mesh(file_path)
    return mesh

def add_random_noise(mesh, noise_strength=0.02, selection_mask=None):
    vertices = np.asarray(mesh.vertices)
    noise = np.zeros_like(vertices)

    if selection_mask is None:
        # Add noise to all vertices if no selection mask is provided
        noise = np.random.normal(0, noise_strength, size=vertices.shape)
    else:
        # Add noise only to selected vertices
        noise[selection_mask] = np.random.normal(0, noise_strength, size=noise[selection_mask].shape)

    vertices += noise
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    return mesh

def save_obj_file(mesh, output_file_path):
    o3d.io.write_triangle_mesh(output_file_path, mesh)

input_file = 'model.obj'
output_file = 'noisy_model.obj'

mesh = load_obj_file(input_file)

# Convert vertices to a NumPy array and access the y-coordinates
vertices = np.asarray(mesh.vertices)
selection_mask = (vertices[:, 1] > np.mean(vertices[:, 1]))

# Add noise only to the selected vertices
mesh_with_noise = add_random_noise(mesh, selection_mask=selection_mask)

save_obj_file(mesh_with_noise, output_file)