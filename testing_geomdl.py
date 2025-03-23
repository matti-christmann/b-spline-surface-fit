
import csv
import open3d as o3d
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

def generate_point_cloud_csv(file_path, num_points_u = 50, num_points_v = 50):
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
    
def read_pc_from_ply(file_path):  
    # Read pc from .ply file, store in numpy array and convert to tuple
      # Change this to your actual file path
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    print("LENGTH OF POINTS " + str(len(points)))
    point_tuples = [tuple(point) for point in points]

    return point_tuples

generate_point_cloud_csv("point_cloud.csv", num_points_u=10,num_points_v=10)
print("Point cloud CSV generated successfully.")


file_path = "point_cloud.csv"
points = read_csv_as_tuples(file_path)



# Load PLY file
file_path = 'cropped_P1_original_data.ply'

# Loading the point cloud
pcd = o3d.io.read_point_cloud(file_path)

# Perform voxel grid downsampling with Open3D
downsampled_pcd = pcd.voxel_down_sample(5)
points = np.asarray(downsampled_pcd.points)
point_tuples = [tuple(point) for point in points]

print("LENGTH OF POINTS: " + str(len(points)))
size_u = 10  # Adjust according to your needs
size_v = len(points) // size_u
degree_u = 2
degree_v = 2
ctrlpts_size_u = 5
ctrlpts_size_v = 5


surf = fitting.approximate_surface(point_tuples, size_u, size_v, degree_u, degree_v,\
                                   ctrlpts_size_u = ctrlpts_size_u, ctrlpts_size_v = ctrlpts_size_v,
                                   centripetal = False)

surf_curves = construct.extract_curves(surf)
plot_extras = [ # adding extras to the surface plot
    dict(points=surf_curves['u'][0].evalpts, name="u", color="cyan", size=5),
    dict(points=surf_curves['v'][0].evalpts, name="v", color="magenta", size=5),
    dict(points=points, name="input points", color="red", size=8)  # Add input points
]

# Plot the interpolated curve
surf.delta = 0.08
surf.vis = VisVTK.VisSurface()
surf.render(extras = plot_extras)

filename = "fitted_surface.stl"
geomdl.exchange.export_obj(surf, filename)

# # Visualize data and evaluated points together
import numpy as np
import matplotlib.pyplot as plt
evalpts = np.array(surf.ctrlpts)
pts = np.array(points)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(evalpts[:, 0], evalpts[:, 1], evalpts[:, 2], color = "green")
ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color="red")
plt.show()

