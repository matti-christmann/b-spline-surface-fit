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

## Contributing

## License

## Contact Information
