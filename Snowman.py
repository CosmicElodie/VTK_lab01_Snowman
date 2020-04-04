# ----------------------------------------------------------
# Laboratoire 1 - SnowMan
# Crüll Loris, Lagier Elodie
# ----------------------------------------------------------

import time
import vtk


# ----------------------------------------------------------
# CREATE OBJECTS
# ----------------------------------------------------------
def build_sphere(radius, position):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetThetaResolution(25)
    sphere.SetPhiResolution(25)
    sphere.SetCenter(position)
    sphereT = vtk.vtkTransform()
    return sphere, sphereT


def build_cone(height, radius, resolution, position):
    cone = vtk.vtkConeSource()
    cone.SetDirection(0, -90, 0)
    cone.SetHeight(height)
    cone.SetRadius(radius)
    cone.SetResolution(resolution)
    cone.SetCenter(position)
    coneT = vtk.vtkTransform()
    return cone, coneT


(head, headT) = build_sphere(1.1, (-3, 0, 0))
(left_eye, left_eye_T) = build_sphere(0.15, (-0.33, 2.5, 1))
(right_eye, right_eye_T) = build_sphere(0.15, (0.33, 2.5, 1))
(nose, noseT) = build_cone(0.4, 0.12, 20, (3, 0, 0))

(booty, bootyT) = build_sphere(1.5, (0, 0, 0))


# ----------------------------------------------------------
# CREATE ACTOR
# ----------------------------------------------------------
def create_actor(outputPort, color, object_transform):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outputPort)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    actor.SetUserTransform(object_transform)
    return actor


head_actor = create_actor(head.GetOutputPort(), (1, 0.8, 1), headT)
booty_actor = create_actor(booty.GetOutputPort(), (1, 0.8, 1), bootyT)
nose_actor = create_actor(nose.GetOutputPort(), (1, 0.5, 0.1), noseT)
left_eye_actor = create_actor(left_eye.GetOutputPort(), (0, 0, 0), left_eye_T)
right_eye_actor = create_actor(right_eye.GetOutputPort(), (0, 0, 0), right_eye_T)

# ----------------------------------------------------------
# RENDER
# ----------------------------------------------------------
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.9, 1, 1)
renderer.AddActor(head_actor)
renderer.AddActor(nose_actor)
renderer.AddActor(booty_actor)

# ----------------------------------------------------------
# CAMERA
# ----------------------------------------------------------
camera = renderer.GetActiveCamera()
camera.SetPosition(0, 0, 20)

# ----------------------------------------------------------
# RENDER WINDOW
# ----------------------------------------------------------
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(800, 600)
renWin.Render()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()


# ----------------------------------------------------------
# ON BOUUUUGE
# ----------------------------------------------------------
def move(degrees, sec, function, function_parameters):
    for i in range(0, degrees):
        time.sleep(sec)
        iren.Render()
        function(function_parameters)


move(90, 0.03, headT.RotateZ, -1)  # tête tourne autour du corps
move(15, 0.05, headT.Translate, (0.04, 0, 0))  # colle la tête au corps

move(90, 0.04, noseT.RotateY, -1)  # nez tourne autour du bonhomme
move(20, 0.04, noseT.Translate, (-0.05, 0, 0))  # avance nez vers bonhomme
move(90, 0.04, noseT.RotateZ, 1)  # rotation nez vers la tête
move(40, 0, noseT.Translate, (-0.017, 0, 0))  # descend nez
move(40, 0.02, noseT.Translate, (0, -0.053, 0))  # avance nez hors de la tête
renderer.AddActor(left_eye_actor)  # fait apparaitre les yeux
renderer.AddActor(right_eye_actor)  # fait apparaitre les yeux

move(360, 0.015, camera.Roll, 1)
move(360, 0.015, camera.Azimuth, 1)
move(90, 0.015, camera.Elevation, 1)
move(90, 0.015, camera.Elevation, -1)
