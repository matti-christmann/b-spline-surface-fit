def surface_fitting(input_file_name: str="input.ply", \
                    output_path: str = "example", \
                    save_file_name: str = "approximated_surface",\
                    UDegree: int = 1, VDegree: int = 1,\
                    NbUPoles: int=5, NbVPoles: int=5,\
                    iterations: int=1, \
                    x_min: float = 1.0, x_max: float = 1.0, \
                    y_min: float = 1.0, y_max: float = 1.0):
    
    """
    Script to perform surface approximation using BSpline surfaces. The function
    relies on the implementation of FreeCAD. For this reason, FreeCAD has to be
    installed on the machine. Instructions are found below.
    The algorithm used is a surface approximation with a point distance minimizer.

    Args:
        input_file_name (str): Path to the input file
        output_path (str): Path to the location of the output file
        save_file_name (str): Name of how the output will be saved
        UDegree, VDegree (int): Polynomial degree of the BSplines used to 
                                approximate the surface in U and V direction,
                                respectively
        NbUPoles, NbVPoles (int): Number of control points of the BSplines in
                                  U and V direction, respectively
        iterations (int): Amount of iterations of the fitting algorithm
        x_min, x_max (float): X values of the Region of interest. Used to trim
                              down the surface to the relevant region.
        y_min, y_max (float): Y values of the Region of interest. Used to trim
                              down the surface to the relevant region.

    """    
    """
    The FreeCAD library cannot be installed directly through pip. It requires an
    installation of FreeCAD on the machine (found at https://www.freecad.org/). 
    The following lines of code append the installation of FreeCAD to the system path,
    so that the module can be found with the import statement.

    """
    # insert path here that goes to the installation of FreeCAD
    import os
    import sys
    FREECADPATH = r"C:\\Users\\christm2\\AppData\\Local\\Programs\\FreeCAD 0.21\\bin"
    FREECADLIBPATH = r"C:\\Users\\christm2\\AppData\\Local\\Programs\\FreeCAD 0.21\\lib"
    sys.path.append(FREECADPATH)
    sys.path.append(FREECADLIBPATH)
    
    # trying import of FreeCAD modules
    import FreeCAD
    try:
        import FreeCAD
        import Points
        import ReverseEngineering
        import Mesh
        import Part
        import Sketcher
    except:
        print("FreeCAD modules not found.")

    # Creating new FreeCad document
    doc = FreeCAD.newDocument()

    # inserting the point cloud
    Points.insert(input_file_name,"approximation")
    current_document = FreeCAD.getDocument("approximation")

    # getting the name of the input file
    file_name_without_extension = os.path.splitext(os.path.basename(input_file_name))[0]
    
    # FreeCAD function call to do the approximation
    # this can take some time depending on the chosen values
    added_object = f"Spline{UDegree}{NbUPoles}{iterations}"
    current_document.addObject("Part::Spline", added_object).Shape =\
        ReverseEngineering.approxSurface(Points = getattr(current_document.getObject(f"{file_name_without_extension}"),\
                                            current_document.getObject(f"{file_name_without_extension}").getPropertyNameOfGeometry()),\
                                            UDegree=UDegree, VDegree=VDegree, NbUPoles=NbUPoles, NbVPoles=NbVPoles, Smooth=False,\
                                            Weight=0.1, Grad=1, Bend=0, Curv=0, Iterations=iterations, PatchFactor=1.05,\
                                            Correction=True).toShape()

    # recomuting current document
    FreeCAD.ActiveDocument.recompute()

    """
    To ensure C2 continuity at the boundaries and to avoid overfitting of the point
    cloud, the fitted surface is increased with a scaled factor. Afterwards the 
    obtained surface is cut down within the region of interest. The process takes
    inspiration from the following tutorial:
     https://forum.freecad.org/viewtopic.php?style=10&t=63949
    
    """
    # Selecting point cloud and the approximated surface
    selected_objects = [current_document.getObject(f'{added_object}'), \
                        current_document.getObject(f"{file_name_without_extension}")]
    
    # Projecting points and surface into XY plane
    for object in selected_objects:
        if hasattr(object, "Points"):
            point_cloud = object
        elif hasattr(object, "Shape"):
            face = object.Shape.Face1

    shapes = []
    for point in point_cloud.Points.Points:
        u,v = face.Surface.parameter(point)
        shapes.append(Part.Vertex(FreeCAD.Vector(u,v)))

    comp = Part.Compound(shapes)
    Part.show(comp, "Flat Point Cloud")

    """
    Now boundary lines are written with respect to the previously provided
    coordinates of the region of interest. In this case assuming, the ROI
    is a rectangle. The coordinates are transformed into the XY plane aswell
    """

    FreeCAD.activeDocument().addObject('Sketcher::SketchObject', 'Sketch')
    FreeCAD.activeDocument().Sketch.Placement =\
                             FreeCAD.Placement(FreeCAD.Vector(0.000000, 0.000000, 0.000000),\
                             FreeCAD.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
    FreeCAD.activeDocument().Sketch.MapMode = "Deactivated"

    # Transformation of the ROI coordinates
    boundary_points = [FreeCAD.Vector(x_min, y_min, 0),FreeCAD.Vector(x_min, y_max, 0),\
                       FreeCAD.Vector(x_max, y_min, 0),FreeCAD.Vector(x_max, y_max, 0)]
    transformed_bp = []
    for bp in boundary_points:
        u,v = face.Surface.parameter(bp)
        transformed_bp.append(FreeCAD.Vector(u,v,0))

    # Creating the boundary lines
    FreeCAD.getDocument("approximation").getObject('Sketch').addGeometry(Part.LineSegment(transformed_bp[0], transformed_bp[2]),False)
    FreeCAD.getDocument("approximation").getObject('Sketch').addGeometry(Part.LineSegment(transformed_bp[2], transformed_bp[3]),False)
    FreeCAD.getDocument("approximation").getObject('Sketch').addGeometry(Part.LineSegment(transformed_bp[3], transformed_bp[1]),False)
    FreeCAD.getDocument("approximation").getObject('Sketch').addGeometry(Part.LineSegment(transformed_bp[1], transformed_bp[0]),False)

    FreeCAD.ActiveDocument.recompute()
    FreeCAD.getDocument('approximation').recompute()
   
    # selecting the approximating surface (untrimmed) and the boundary objects
    flat_curves = []
    selected_objects = None
    selected_objects = [current_document.getObject('Sketch'), \
                        current_document.getObject('Flat_Point_Cloud')]
    
    for object in selected_objects:
        try:
            face = object.Shape.Face1
        except AttributeError:
            flat_curves.extend(object.Shape.Edges)

    # Mapping the surface back into 3D 
    curvesOnSurf = []
    pl = Part.Plane().toShape()
    proj = pl.project(flat_curves)
    for e in proj.Edges:
        fc, fp, lp = pl.curveOnSurface(e)
        cos = fc.toShape(face.Surface, fp, lp)
        if isinstance(cos, Part.Edge):
            curvesOnSurf.append(cos)
 
    w = Part.Wire(curvesOnSurf)
    nf = Part.Face(face.Surface, w)
    nf.validate()
    Part.show(nf, "trimmed_surface")
    trimmed_surface = "trimmed_surface"

    # Exporting the created surface in BREP
    __objs__ = []
    __objs__.append(current_document.getObject(trimmed_surface))
    if hasattr(Part, "exportOptions"):
        options = Part.exportOptions(f"{output_path}\\{save_file_name}.step")
        Part.export(__objs__, f"{output_path}\\{save_file_name}.step", options)
    else:
        Part.export(__objs__, f"{output_path}\\{save_file_name}.step")
        del __objs__
    
    # Exporting the created surface as mesh for the error estimation
    __objs__ = []
    __objs__.append(current_document.getObject(trimmed_surface))
    if hasattr(Mesh, "exportOptions"):
        options = Mesh.exportOptions(f"{output_path}\\{save_file_name}.stl")
        Mesh.export(__objs__, f"{output_path}\\{save_file_name}.stl", options)
    else:
        Mesh.export(__objs__, f"{output_path}\\{save_file_name}.stl")
    del __objs__

    # defining function to clear whole FreeCAD document
    def clearAll():
        doc = FreeCAD.ActiveDocument
        if doc:
            for obj in doc.Objects:
                doc.removeObject(obj.Label)#

    clearAll()