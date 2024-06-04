import open3d as o3d
import numpy as np
import os

def filter_points(point_cloud, x_range, y_range):

    """
    Function to filter point cloud data to a provided coordinate range x and y.

    Args:
        point_cloud (object): open3d point cloud object
        x_range (list): List format of x_min and x_max, [min_x, max_x]
        y_range (list): List format of y_min and y_max, [min_y, max_y]

    """

    # Empty list to append points to
    filtered_points = []

    # Extracting point from point cloud
    points = np.asarray(point_cloud.points)

    # Cylcing through point cloud document and reading the coordinates of points
    for point in points:
        x, y, z = point
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            filtered_points.append([x, y, z])

    # Returning an open3d point cloud object        
    return o3d.geometry.PointCloud(o3d.utility.Vector3dVector(np.array(filtered_points)))

def crop_geometry(point_cloud_input_path: str = "example", \
                  cropped_point_cloud_output_file_path: str = "example", \
                  min_x: float = 1.0, max_x: float = 1.0, \
                  min_y: float = 1.0, max_y: float = 1.0):
    
    """
    Function to crop geometry after user input on the range of the plate field.

    Args:
        point_cloud_input_path (str): Input path to the original point cloud
        cropped_point_cloud_output_file_path (str): Output file path of the cropped
                                                    point cloud
        min_x, max_x (float): coordinates for the min/max x range of the region of
                              interest
        min_y, max_y (float): coordinates for the min/max y range of the region of
                              interest
    
    """

    # Creating np array of the provided boundary points
    boundary_points = np.array([[min_x, min_y, 2],[min_x, max_y, 2],\
                       [max_x, max_y, 2],[max_x, min_y, 2]])

    # Create a LineSet object for displaying the ROI
    lines = [[0, 1], [1, 2], [2, 3], [3, 0]]
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(boundary_points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(np.array([[1, 0, 0] for _ in lines]))

    # Loading the point cloud file
    pcd = o3d.io.read_point_cloud(point_cloud_input_path) 
    
    # Visualize the LineSet with the point cloud
    print("Cornfirm through pressing: 'Q'")
    o3d.visualization.draw_geometries([line_set, pcd])

    # filtering the input file, to only include points from the previously defined range
    filtered_points = filter_points(pcd, [min_x, max_x], [min_y, max_y])

    # Save the cropped point cloud
    o3d.io.write_point_cloud(f"{cropped_point_cloud_output_file_path}\\cropped_{os.path.basename(point_cloud_input_path)}",\
                              filtered_points)
