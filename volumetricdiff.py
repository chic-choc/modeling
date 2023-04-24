import numpy as np
from mayavi import mlab

obj_file_1 = "model.obj"
obj_file_2 = "modelcopy.obj"

vertices = []
faces = []

for file_path in [obj_file_1, obj_file_2]:
    with open(file_path, 'r') as f:
        for line in f.readlines():
            split_line = line.strip().split()
            if len(split_line) > 0:
                if split_line[0] == 'v':
                    vertices.append([float(x) for x in split_line[1:]])
                elif split_line[0] == 'f':
                    faces.append([int(x.split('/')[0]) - 1 for x in split_line[1:]])

    if file_path == obj_file_1:
        vertices1, faces1 = np.array(vertices), np.array(faces)
    else:
        vertices2, faces2 = np.array(vertices), np.array(faces)

    vertices = []
    faces = []

# Calculate the volumetric difference between the two objects
volume1 = 0
volume2 = 0
for i, (vertices, faces) in enumerate([(vertices1, faces1), (vertices2, faces2)]):
    for face in faces:
        for j in range(1, len(face) - 1):
            a, b, c, d = vertices[face[0]], vertices[face[j]], vertices[face[j + 1]], np.zeros(3)
            volume = np.abs(np.dot(a - d, np.cross(b - d, c - d))) / 6

            if i == 0:
                volume1 += volume
            else:
                volume2 += volume

volumetric_difference = abs(volume1 - volume2)
print(f"The volumetric difference between the two .obj files is {volumetric_difference} cubic units.")

# Create the figure and axis objects
fig = mlab.figure()

# Plot the first object
mlab.triangular_mesh(vertices1[:, 0], vertices1[:, 1], vertices1[:, 2], faces1, color=(1, 0, 0), opacity=0.7)

# Plot the second object
mlab.triangular_mesh(vertices2[:, 0], vertices2[:, 1], vertices2[:, 2], faces2, color=(0, 1, 0), opacity=0.7)

# Show the volumetric difference between the two objects as a scalar field
vol_diff_scalar = np.zeros(len(vertices1))
vol_diff_scalar.fill(volumetric_difference)
mlab.triangular_mesh(vertices1[:, 0], vertices1[:, 1], vertices1[:, 2], faces1, scalars=vol_diff_scalar, colormap='cool')

# Add a colorbar to the figure
mlab.colorbar(orientation='vertical')




# Show the figure
mlab.show()