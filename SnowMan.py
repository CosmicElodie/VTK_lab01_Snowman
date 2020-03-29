#!/usr/bin/env python
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
    return sphere


def build_cone(height, radius, resolution, position):
    cone = vtk.vtkConeSource()
    cone.SetDirection(0, -90, 0)
    cone.SetHeight(height)
    cone.SetRadius(radius)
    cone.SetResolution(resolution)
    cone.SetCenter(position)
    return cone


head = build_sphere(1, (-3, 0, 0))
left_eye = build_sphere(0.15, (-0.33, 2.3, 1))
right_eye = build_sphere(0.15, (0.33, 2.3, 1))
nose = build_cone(0.4, 0.12, 20, (3, 0, 0))

booty = build_sphere(1.5, (0, 0, 0))


# ----------------------------------------------------------
# FILTER OBJECTS
# source 1 : https://www.programcreek.com/python/example/12960/vtk.vtkTransform
# source 2 : https://vtk.org/Wiki/VTK/Examples/Python/RotationAroundLine
# ----------------------------------------------------------
def filter_object(object_to_modify, transformed_obj):
    filtered_object = vtk.vtkTransformPolyDataFilter()
    filtered_object.SetTransform(transformed_obj)
    filtered_object.SetInputConnection(object_to_modify.GetOutputPort())
    filtered_object.Update()
    return transformed_obj, filtered_object


(transformed_head, filtered_head) = filter_object(head, vtk.vtkTransform())
(transformed_nose, filtered_nose) = filter_object(nose, vtk.vtkTransform())
(transformed_booty, filtered_booty) = filter_object(booty, vtk.vtkTransform())
(transformed_left_eye, filtered_left_eye) = filter_object(left_eye, vtk.vtkTransform())
(transformed_right_eye, filtered_right_eye) = filter_object(right_eye, vtk.vtkTransform())

transformed_head.PostMultiply()
transformed_booty.PostMultiply()
transformed_nose.PostMultiply()


# ----------------------------------------------------------
# CREATE ACTOR
# ----------------------------------------------------------
def create_actor(outputPort, color):
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(outputPort)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(color)
    return actor


head_actor = create_actor(filtered_head.GetOutputPort(), (1, 0.8, 1))
booty_actor = create_actor(filtered_booty.GetOutputPort(), (1, 0.8, 1))
nose_actor = create_actor(filtered_nose.GetOutputPort(), (1, 0.5, 0.1))
left_eye_actor = create_actor(filtered_left_eye.GetOutputPort(), (0, 0, 0))
right_eye_actor = create_actor(filtered_right_eye.GetOutputPort(), (0, 0, 0))

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

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()


def move(range_limit, sec, function, function_parameters):
    for i in range(0, range_limit):
        time.sleep(sec)
        iren.Render()
        function(function_parameters)


move(90, 0.03, transformed_head.RotateZ, -1)
move(16, 0.07, transformed_head.Translate, (0, -0.05, 0))

move(90, 0.03, transformed_nose.RotateY, -1)
move(16, 0.03, transformed_nose.Translate, (0, 0, -0.05))
move(90, 0.03, transformed_nose.RotateX, -1)

move(3, 0.03, transformed_nose.Translate, (0, -0.05, 0))
move(22, 0.03, transformed_nose.Translate, (0, 0, 0.05))
move(4, 0.03, transformed_nose.Translate, (0, 0.01, 0))

renderer.AddActor(left_eye_actor)
renderer.AddActor(right_eye_actor)

move(360, 0.02, camera.Roll, 1)
move(360, 0.02, camera.Azimuth, 1)
move(90, 0.02, camera.Elevation, 1)
move(90, 0.02, camera.Elevation, -1)
