def error_estimation(reconstructed_surface_path: str="examples", \
                     point_cloud_path: str="examples", \
                     error_plot: bool = False):
    
    """
    This is a function that takes the reconstructed surface and the original
    point cloud and calculates the distance of the point to the reconstructed
    surface. The distance is then obtained for each point cloud point and
    the average reconstruction error is calculated.

    Args:
        reconstructed_surface_path (str): Input path to the surface
        point_cloud_path (str): Input path to the point cloud
        error_plot (bool): Boolean value if color plot of the error should 
                           be shown
    
    Created by: Matti Christmann

    """

    # importing meshlab
    import pymeshlab as ml

    # Creating meshset
    mesh = ml.MeshSet()

    # Loading reference mesh. In the case of the surface reconstruction we set
    # this as the reconstructed surface.
    mesh.load_new_mesh(reconstructed_surface_path)

    # Loading measure mesh. Im porting the point cloud to measure the distance
    # of points to the reconstructed surface.
    mesh.load_new_mesh(point_cloud_path)
    
    # Mesuring distance between point cloud and surface. This is done for every
    # point of the point cloud. Result is stored in a scalar array.
    mesh.apply_filter("compute_scalar_by_distance_from_another_mesh_per_vertex",\
                    measuremesh = 1,\
                    refmesh = 0, \
                    signeddist = False )
    
    # Obtaining the scalar array, that holds the distances for each point of the
    # point cloud
    distance_array = mesh.mesh(1).vertex_scalar_array()

    # Calculating the mean average error
    mae = sum(distance_array) / len(distance_array)
    print("max distance:"+ str(max(distance_array)),"min distance:" + str(min(distance_array)))
    print("mean average error:" + str(mae))
    # Checking if the user added the  rendering option:
    # Coloring the point cloud according to the distance from the reconstructed
    # surface
    if True:
         mesh.apply_filter("compute_color_from_scalar_per_vertex", \
                            minval = max(distance_array), \
                            maxval = min(distance_array), \
                            zerosym = False)
                
         mesh.save_current_mesh(point_cloud_path)
    # Clearing the meshlab data
    mesh.clear()    
    mesh = None

    if error_plot == True:

        import open3d as o3d        
        # Load PLY file
        point_cloud = o3d.io.read_point_cloud(point_cloud_path)
        surface = o3d.io.read_triangle_mesh(reconstructed_surface_path)
        print("press Q to exit.")
        o3d.visualization.draw_geometries([point_cloud, surface])

    return mae

