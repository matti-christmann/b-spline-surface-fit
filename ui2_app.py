import tkinter as tk
from tkinter import filedialog
from threading import Thread
from crop_geometry import crop_geometry
from surface_fitting import surface_fitting
from voxel_downsampling import voxel_downsampling
from error_estimation import error_estimation

import os

class PointCloudProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point Cloud Processor v1.0")

        self.input_file_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.output_file_name = tk.StringVar()
        self.processing_status = tk.StringVar()

        # Input file selection
        self.file_label = tk.Label(root, text="Select Point Cloud File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_entry = tk.Entry(root, textvariable=self.input_file_path, state="disabled")
        self.input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Output folder selection
        self.output_label = tk.Label(root, text="Select Output Folder:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(root, textvariable=self.output_folder_path, state="disabled")
        self.output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.output_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.output_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Output file name
        self.output_file_label = tk.Label(root, text="Output File Name:")
        self.output_file_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.output_file_entry = tk.Entry(root, textvariable=self.output_file_name)
        self.output_file_entry.grid(row=2, column=1, padx=10, pady=10, sticky="we")

        # Region of Interest header
        self.roi_header_label = tk.Label(root, text="Region of Interest:")
        self.roi_header_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # x_max and x_min
        self.x_max_label = tk.Label(root, text="x_max:")
        self.x_max_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.x_max_entry = tk.Entry(root)
        self.x_max_entry.grid(row=4, column=3, padx=10, pady=10, sticky="we")

        self.x_min_label = tk.Label(root, text="x_min:")
        self.x_min_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.x_min_entry = tk.Entry(root)
        self.x_min_entry.grid(row=4, column=1, padx=10, pady=10, sticky="we")

        # y_max and y_min
        self.y_max_label = tk.Label(root, text="y_max:")
        self.y_max_label.grid(row=6, column=2, padx=10, pady=10, sticky="w")
        self.y_max_entry = tk.Entry(root)
        self.y_max_entry.grid(row=6, column=3, padx=10, pady=10, sticky="we")

        self.y_min_label = tk.Label(root, text="y_min:")
        self.y_min_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.y_min_entry = tk.Entry(root)
        self.y_min_entry.grid(row=6, column=1, padx=10, pady=10, sticky="we")

        # Voxel size
        self.voxel_label = tk.Label(root, text="Voxel Size:")
        self.voxel_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.voxel_entry = tk.Entry(root)
        self.voxel_entry.grid(row=8, column=1, padx=10, pady=10, sticky="we")

        # UDegree
        self.udegree_label = tk.Label(root, text="UDegree:")
        self.udegree_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.udegree_entry = tk.Entry(root)
        self.udegree_entry.grid(row=9, column=1, padx=10, pady=10, sticky="we")

        # VDegree
        self.vdegree_label = tk.Label(root, text="VDegree:")
        self.vdegree_label.grid(row=10, column=0, padx=10, pady=10, sticky="w")
        self.vdegree_entry = tk.Entry(root)
        self.vdegree_entry.grid(row=10, column=1, padx=10, pady=10, sticky="we")

        # NbUPoles
        self.nbupoles_label = tk.Label(root, text="NbUPoles:")
        self.nbupoles_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")
        self.nbupoles_entry = tk.Entry(root)
        self.nbupoles_entry.grid(row=11, column=1, padx=10, pady=10, sticky="we")

        # NbVPoles
        self.nbvpoles_label = tk.Label(root, text="NbVPoles:")
        self.nbvpoles_label.grid(row=12, column=0, padx=10, pady=10, sticky="w")
        self.nbvpoles_entry = tk.Entry(root)
        self.nbvpoles_entry.grid(row=12, column=1, padx=10, pady=10, sticky="we")

        # Iterations
        self.iterations_label = tk.Label(root, text="Iterations:")
        self.iterations_label.grid(row=13, column=0, padx=10, pady=10, sticky="w")
        self.iterations_entry = tk.Entry(root)
        self.iterations_entry.grid(row=13, column=1, padx=10, pady=10, sticky="we")

        # Color plot
        self.error_plot_var = tk.BooleanVar()
        self.error_plot_checkbox = tk.Checkbutton(root, text="Error Estimate Color Plot", variable=self.error_plot_var)
        self.error_plot_checkbox.grid(row=14, column=0, columnspan=2, pady=10)

        # Processing button
        self.process_button = tk.Button(root, text="Process Point Cloud", command=self.process_point_cloud)
        self.process_button.grid(row=15, column=0, columnspan=3, pady=20)

        # Processing status
        self.status_label = tk.Label(root, textvariable=self.processing_status)
        self.status_label.grid(row=16, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # Close button (hidden initially)
        self.close_button = tk.Button(root, text="Close", command=self.close_app, state="disabled")
        self.close_button.grid(row=17, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Point Cloud Files", "*.ply;*.xyz")])
        self.input_file_path.set(file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_path.set(folder_path)

    def process_point_cloud(self):
        input_path = self.input_file_path.get()
        output_folder = self.output_folder_path.get()
        output_file_name = self.output_file_name.get()
        x_max = float(self.x_max_entry.get())
        x_min = float(self.x_min_entry.get())
        y_max = float(self.y_max_entry.get())
        y_min = float(self.y_min_entry.get())
        voxel_size = float(self.voxel_entry.get())
        udegree = int(self.udegree_entry.get())
        vdegree = int(self.vdegree_entry.get())
        nbupoles = int(self.nbupoles_entry.get())
        nbvpoles = int(self.nbvpoles_entry.get())
        iterations = int(self.iterations_entry.get())
        color_plot = self.error_plot_var.get()

        if input_path and output_folder and output_file_name:
            output_path = os.path.join(output_folder, f"{output_file_name}.ply")
            self.processing_status.set("Processing... Please wait.")
            self.process_button["state"] = "disabled"

            # Run the processing in a separate thread to avoid freezing the GUI
            processing_thread = Thread(target=self.process_and_update_status,
                               args=(input_path, output_folder, output_file_name, voxel_size, \
                                     udegree, vdegree, nbupoles, nbvpoles, iterations, color_plot,\
                                        x_max, x_min, y_max, y_min))
            processing_thread.start()

    def process_and_update_status(self, input_path, output_folder,
                                    output_file_name, voxel_size,
                                    udegree, vdegree, nbupoles,
                                    nbvpoles, iterations, color_plot, \
                                    x_max, x_min, y_max, y_min):
        
        # Crop geometry and get cropped_points_output_folder
        # here we take the provided input path of the pc and load it!
        # we crop the provided point cloud and have a cropped pc as output
        # we should save the cropped point cloud and that is the one that should be
        # downsmapled
        # maybe we can do the loading of the point clouds also in the function,that
        # way there are no mistakes and user does not have to worry about PC format
        print(output_folder) 
        crop_geometry(point_cloud_input_path = input_path, \
                         cropped_point_cloud_output_file_path = output_folder, \
                         min_x = x_min, max_x = x_max, \
                         min_y = y_min, max_y = y_max)
   
       
        # Downsampling the point cloud
        path_cropped = f"{output_folder}\\cropped_{os.path.basename(input_path)}"
        voxel_downsampling(point_cloud_input_path = path_cropped, \
                              voxel_size = voxel_size, \
                              downsampled_point_cloud_output_path = output_folder)

        # Performing the surface reconstruction
        path_downsampled = f"{output_folder}\\downsampled_cropped_{os.path.basename(input_path)}"
        
        surface_fitting(
                            input_file_name=path_downsampled, \
                            output_path=output_folder,\
                            save_file_name=output_file_name,\
                            UDegree=udegree, VDegree=vdegree,\
                            NbUPoles=nbupoles, NbVPoles=nbvpoles,\
                            iterations=iterations,\
                            x_min = x_min, x_max = x_max, \
                            y_min = y_min, y_max = y_max)

        path_fitted_surface = f"{output_folder}\\{output_file_name}.stl"
        # Calculating the error
        error_estimation(reconstructed_surface_path=path_fitted_surface,\
                            point_cloud_path=path_downsampled,\
                            error_plot=color_plot)

        # Update processing status
        self.processing_status.set("Processing complete. Check your output folder.")
        self.close_button["state"] = "normal"

    def close_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PointCloudProcessingApp(root)
    root.mainloop()
