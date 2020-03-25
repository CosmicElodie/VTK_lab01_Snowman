#!/usr/bin/env python

import vtk
import time


# -------------------------------------------------------
# CONSTRUCTION OBJETS
# -------------------------------------------------------

def build_sphere(radius):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetThetaResolution(25)
    sphere.SetPhiResolution(25)

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    return sphereMapper


headMapper = build_sphere(5)
bootyMapper = build_sphere(7)
# oeil = vtk.vtkSphereSource()
# oeil.SetRadius(2)

nose = vtk.vtkConeSource()
nose.SetHeight(2)
nose.SetRadius(0.8)
nose.SetResolution(25)
nose.SetDirection(0, -90, 0)  # nez pointe vers le bas
noseMapper = vtk.vtkPolyDataMapper()
noseMapper.SetInputConnection(nose.GetOutputPort())


# -------------------------------------------------------
# ACTEURS
# -------------------------------------------------------

def build_actor(object_mapper, r, g, b, x, y, z):
    actor = vtk.vtkActor()
    actor.SetMapper(object_mapper)
    actor.GetProperty().SetColor(r, g, b)
    actor.SetPosition(x, y, z)
    return actor


headActor = build_actor(headMapper, 1, 1, 1, -20, 0, 0)
bootyActor = build_actor(bootyMapper, 1, 1, 1, -0, 0, 0)
coneActor = build_actor(noseMapper, 1, 0.517, 0.180, 20, 0, 0)

# -------------------------------------------------------
# RENDERER
# -------------------------------------------------------
ren = vtk.vtkRenderer()
ren.AddActor(headActor)
ren.AddActor(bootyActor)
ren.AddActor(coneActor)
ren.SetBackground(0.5, 0.2, 0.3)

# -------------------------------------------------------
# FENÊTRE
# -------------------------------------------------------
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(800, 600)


# -------------------------------------------------------
# MOUVEMENTS OBJET(s)
# -------------------------------------------------------

def move_head_around_booty():
    while (headActor.GetPosition()[0] < 0) and (headActor.GetPosition()[1] <= 20):
        time.sleep(0.01)
        renWin.Render()
        headActor.SetPosition(headActor.GetPosition()[0] + 0.1,
                              headActor.GetPosition()[1] + 0.1,
                              headActor.GetPosition()[2])
        # TODO :    calculer les coordonnées x et yselon que le centre de la tête reste à 20 du
        #           centre du corps pour le mouvement


def move_head_down():
    while headActor.GetPosition()[1] < 10:
        time.sleep(0.01)
        renWin.Render()
        headActor.SetPosition(headActor.GetPosition()[0],
                              headActor.GetPosition()[1] - 0.1,
                              headActor.GetPosition()[2])


def make_moves():
    move_head_around_booty()
    move_head_down()


make_moves()