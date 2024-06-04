import open3d as o3d
import os

#TO DO Implement dependency check

def voxel_downsampling(point_cloud_input_path: str = "example",
                       voxel_size: float = 3.0,
                       downsampled_point_cloud_output_path: str = "example_downsampled.ply"):
    """
    Perform voxel downsampling on a point cloud using Open3D library.

    Args:
        point_cloud_input_path (str): Input path to the point cloud to be downsampled.
        voxel_size (float): Size of voxel to be used for averaging the points.
        downsampled_point_cloud_output_path (str): Output path to save the downsampled point cloud.
    """

    try:
        # Loading the point cloud
        pcd = o3d.io.read_point_cloud(point_cloud_input_path)

        # Perform voxel grid downsampling with Open3D
        downsampled_pcd = pcd.voxel_down_sample(voxel_size)

        # Save the downsampled point cloud to a new file
        output_file_path = os.path.join(downsampled_point_cloud_output_path,
                                        f"downsampled_{os.path.basename(point_cloud_input_path)}")
        o3d.io.write_point_cloud(output_file_path, downsampled_pcd)
        print(f"Downsampled point cloud saved at: {output_file_path}")

    except FileNotFoundError:
        print(f"File not found: {point_cloud_input_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage:
# voxel_downsampling("input_point_cloud.ply", 3.0, "output_folder")
