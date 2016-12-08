# $ enaml-run vtk_canvas.enaml 
# Segmentation fault


from enaml.widgets.api import Window, Container, VTKCanvas

import vtk


def create_renderer():
    quadric = vtk.vtkQuadric()
    quadric.SetCoefficients(.5, 1, .2, 0, .1, 0, 0, .2, 0, 0)

    sample = vtk.vtkSampleFunction()
    sample.SetSampleDimensions(50, 50, 50)
    sample.SetImplicitFunction(quadric)

    contours = vtk.vtkContourFilter()
    contours.SetInputConnection(sample.GetOutputPort())
    contours.GenerateValues(5, 0.0, 1.2)

    contour_mapper = vtk.vtkPolyDataMapper()
    contour_mapper.SetInputConnection(contours.GetOutputPort())
    contour_mapper.SetScalarRange(0.0, 1.2)

    contour_actor = vtk.vtkActor()
    contour_actor.SetMapper(contour_mapper)

    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(sample.GetOutputPort())

    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())

    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(0, 0, 0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(contour_actor)
    renderer.AddActor(outline_actor)
    renderer.SetBackground(.75, .75, .75)

    return renderer


enamldef Main(Window):
    title = 'VTK Canvas'
    Container:
        padding = 0
        VTKCanvas:
            renderer = create_renderer()