#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    resolution = 500

    random.seed()
    for x in range(resolution):
        for y in range(resolution):
            real = (x / resolution) * 4 - 2
            imag = (y / resolution) * 4 - 2
            c = real + imag * 1j

            mandelbrot_set(0, c, 20)
    glFlush()


def mandelbrot_set(z, c, number_of_checks):
    limit = z
    for x in range(number_of_checks):
        limit = limit**2 + c
        if abs(limit) > 2:
            glColor3f(1.0, 0.0, 0.0)
            break
    else:
        glColor3f(0.0, 0.0, 0.0)

    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2f(c.real * 2.0, c.imag * 2.0)
    glEnd()


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
        glOrtho(-5.0, 5.0, -5.0 / aspect_ratio, 5.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
