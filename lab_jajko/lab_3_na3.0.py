#!/usr/bin/env python3
import math
import sys
import itertools

import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def calculate_egg_points(N):
    tab = np.zeros((N, N, 3))
    tab_u_y = np.linspace(0.0, 1.0, N)
    for u in range(N):
        for y in range(N):
            tab[u, y, 0] = (-90 * (tab_u_y[u] ** 5) + 225 * (tab_u_y[u] ** 4) - 270 * (tab_u_y[u] ** 3) + 180 * (
                    tab_u_y[u] ** 2) - 45 * tab_u_y[u]) * math.cos(math.pi * tab_u_y[y])
            tab[u, y, 1] = 160 * (tab_u_y[u] ** 4) - 320 * (tab_u_y[u] ** 3) + 160 * (tab_u_y[u] ** 2) - 5
            tab[u, y, 2] = (-90 * (tab_u_y[u] ** 5) + 225 * (tab_u_y[u] ** 4) - 270 * (tab_u_y[u] ** 3) + 180 * (
                    tab_u_y[u] ** 2) - 45 * tab_u_y[u]) * math.sin(math.pi * tab_u_y[y])
    return tab


def draw_egg(tab, N):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            x, y, z = tab[i, j]
            glVertex(x, y, z)
    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    N = 50
    tab = calculate_egg_points(int(N))

    axes()
    draw_egg(tab, int(N))

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
