#!/usr/bin/env python3
import math
import sys
import itertools

import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

depth = 3
size = 5
base_tetra = [[0.0, 0.0,size * 1.0],
              [0.0, size * 0.942809,size * -0.333333],
              [size * -0.816497, size * -0.471405,size * -0.333333],
              [size * 0.816497,size * -0.471405,size * -0.333333]]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)


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


def draw_triangle(a, b, c):
    glBegin(GL_TRIANGLES)

    glColor3fv(interpolate_color(a))
    glVertex3fv(a)
    glColor3fv(interpolate_color(b))
    glVertex3fv(b)
    glColor3fv(interpolate_color(c))
    glVertex3fv(c)

    glEnd()


def divide_triangle(a, b, c, m):
    v0 = [0, 0, 0]
    v1 = [0, 0, 0]
    v2 = [0, 0, 0]
    if m > 0:
        for j in range(3):
            v0[j] = (a[j] + b[j]) / 2
            v1[j] = (a[j] + c[j]) / 2
            v2[j] = (b[j] + c[j]) / 2
        divide_triangle(a, v0, v1, m - 1)
        divide_triangle(b, v0, v2, m - 1)
        divide_triangle(c, v1, v2, m - 1)
    else:
        draw_triangle(a, b, c)


def interpolate_color(v):
    return [
        (v[0] + 1.0) / 2.0,
        (v[1] + 1.0) / 2.0,
        (v[2] + 1.0) / 2.0,
    ]


def sierpinski_gasket(m):
    divide_triangle(base_tetra[0], base_tetra[1], base_tetra[2], m)
    divide_triangle(base_tetra[1], base_tetra[2], base_tetra[3], m)
    divide_triangle(base_tetra[0], base_tetra[2], base_tetra[3], m)
    divide_triangle(base_tetra[0], base_tetra[1], base_tetra[3], m)


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    axes()
    sierpinski_gasket(depth)

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
