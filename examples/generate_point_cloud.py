import numpy as np
import open3d as o3d

def generate_random_point_cloud(num_points=1000, scale=1.0):
    """
    Generate a random point cloud of specified number of points.
    
    :param num_points: Number of points in the point cloud
    :param scale: The scale of the point cloud in all directions
    :return: open3d.geometry.PointCloud object
    """
    # Generate random 3D points within a unit cube, scaled by the given scale
    points = np.random.rand(num_points, 3) * scale
    
    # Create an Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    return pcd

def save_point_cloud_to_ply(pcd, filename="random_point_cloud.xyz"):
    """
    Save the generated point cloud to a .ply file.
    
    :param pcd: open3d.geometry.PointCloud object
    :param filename: File name for the saved point cloud
    """
    o3d.io.write_point_cloud(filename, pcd)
    print(f"Point cloud saved as {filename}")

def main():
    # Set the number of points and scale for the point cloud
    num_points = 1000  # You can adjust this for more/less density
    scale = 1.0  # Adjust the scale as necessary
    
    # Generate the random point cloud
    point_cloud = generate_random_point_cloud(num_points, scale)
    
    # Save the point cloud to a .ply file
    save_point_cloud_to_ply(point_cloud)

if __name__ == "__main__":
    main()
