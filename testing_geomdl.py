
import csv
import geomdl
import geomdl.fitting
from geomdl import exchange
from geomdl import construct
#approx = geomdl.fitting.approximate_curve()
#exchange.export_stl(approx, "approximation.stl")

from geomdl import fitting
from geomdl.visualization import VisVTK

import csv
import random
import math
import numpy as np

def generate_point_cloud_csv(file_path, num_points_u=10, num_points_v=10):
    """
    Generates a CSV file with 3D points forming a regular grid surface.
    
    :param file_path: Path to save the CSV file.
    :param num_points_u: Number of points along the U direction.
    :param num_points_v: Number of points along the V direction.
    """
    u_values = np.linspace(0, 1, num_points_u)
    v_values = np.linspace(0, 1, num_points_v)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for u in u_values:
            for v in v_values:
                x = u  # Spread in X direction
                y = v  # Spread in Y direction
                z = math.sin(u * v)  # Curved surface
                writer.writerow([x, y, z])

def read_csv_as_tuples(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [tuple(map(float, row)) for row in reader]

generate_point_cloud_csv("point_cloud.csv", num_points_u=20,num_points_v=20)
print("Point cloud CSV generated successfully.")

file_path = 'point_cloud.csv'  # Change this to your actual file path
points = read_csv_as_tuples(file_path)

size_u = 2
size_v = 2
degree_u = 2
degree_v = 2

# Do global curve approximation
#surf = fitting.approximate_surface(points, size_u, size_v, degree_u, degree_v)

surf = fitting.approximate_surface(points, size_u, size_v, degree_u, degree_v, ctrlpts_size_u=5, ctrlpts_size_v=5)

surf_curves = construct.extract_curves(surf)
plot_extras = [
    dict(
        points=surf_curves['u'][0].evalpts,
        name="u",
        color="cyan",
        size=5
    ),
    dict(
        points=surf_curves['v'][0].evalpts,
        name="v",
        color="magenta",
        size=5
    )
]

# Plot the interpolated curve
surf.delta = 0.05
surf.vis = VisVTK.VisSurface()
surf.render(extras = plot_extras)

# # Visualize data and evaluated points together
import numpy as np
import matplotlib.pyplot as plt
evalpts = np.array(surf.evalpts)
pts = np.array(points)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(evalpts[:, 0], evalpts[:, 1], evalpts[:, 2])
ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color="red")
plt.show()

