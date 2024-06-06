# b-spline-surface-fit
Application for the fitting of B-spline surfaces to point clouds.
This Python project is the output of my masters thesis and work done as a reasearch assistant in the Marine and Arctic Technology research team. The motivation was to provide an easy and accesible programm to characterize distortion shapes of welded thin-deck ship panels to enable further investigations on their strength capabilities. The thesis can be accessed [here](https://libguides.aalto.fi/c.php?g=653791&p=5137711). 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Installation
The scripts can be used in two ways; either as standalone scripts, where the raw functions are provided or as an application to enable easy usability.
### Dependencies
Dependency check is implemented in the beginning of each script, with the option to install during execution. Alternatively, these libraries can be easily installed through `pip install`.
* [open3D](https://www.open3d.org/): Library for 3D data processing. Used for voxel downsampling in this project.
* [numpy](https://numpy.org/): Fundamental package for scientific computing in Python.
* [pyMeshLab](https://github.com/cnr-isti-vclab/meshlab): pyMeshLab is a Python library that enables users to write scripts using the various functions available in Meshlab.

Furthermore, the installation of [FreeCAD v0.21](https://www.freecad.org/) on the local machine is required. The local installation path needs to be added to the script `surface_fitting.py` in the following line. Replace USER with the user on the local machine.
```python
  # insert path here that goes to the installation of FreeCAD
    FREECADPATH = r"C:\\Users\\USER\\AppData\\Local\\Programs\\FreeCAD 0.21\\bin"
    FREECADLIBPATH = r"C:\\Users\\USER\\AppData\\Local\\Programs\\FreeCAD 0.21\\lib"
```


## Usage
The package can be used either by running `ui2_app.py` which gives an GUI for the user to setup the surface reconstruction process. The second option is to utilize the scripts `crop_geometry.py` `voxel_downsampling.py` and `surface_fitting.py` to build an own application
1. **Run the Application:**
   ```sh
   python ui2_app.py

 <img src="/pictures/GUI.jpg?raw=true" alt="GUI Screenshot" title="Optional Title" width="350"/>
   
2. **Follow the GUI instructions:**
   Starting point for the reconstruction is a planar type point cloud in `.ply` format.
   Load `.ply` file.
   Set up parameters for the surface reconstruction process. Parameters are strongly case dependant, recommendations for plate fields (based on investigations done in the thesis) are:
   ```sh
    voxel size = 2
    UDegree = 3
    VDegree = 3
    NbUPoles = 15
    NbVPoles = 15
    Iterations = 3 

3. **Perform reconstruction and error analysis:**
   The reconstructed surface will be saved as `.step` format in the specified output folder. The application also gives maximum / minimum point to surface distance, as well as the mean average error of the reconstruction as output per default. These can be changed by modifying `error_estimation.py`.


## Contributing

## License

## Contact Information
