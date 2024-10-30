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

    random.seed()
    sierpinski_carpet(-50, -50, 100, 100, 3, 0)

    glFlush()


def draw_rectangle(x, y, a, b):
    red = random.random()
    green = random.random()
    blue = random.random()
    glColor3f(red, green, blue)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)

    glColor3f(blue, green, red)
    glVertex2f(x + a, y)
    glVertex2f(x + a, y + b)
    glVertex2f(x, y + b)
    glEnd()


def int_pow(base, exp):
    result = 1
    while True:
        if exp & 1:
            result = result * base
        exp >>= 1
        if not exp:
            break
        base = base * base
    return result


def sierpinski_carpet(x, y, a, b, current_depth, depth):
    for i in range(3):
        for j in range(3):
            if i == 1 and j == i:
                continue
            step = int_pow(3, (depth - current_depth))
            new_x = x + i * step
            new_y = y + j * step

            if current_depth == depth:
                rec_a = 2.0 / int_pow(3, depth)
                rec_b = 2.0 / int_pow(3, depth)
                rec_x = new_x * rec_a
                rec_y = new_y * rec_b
                draw_rectangle(rec_x, rec_y, rec_a, rec_b)
            else:
                sierpinski_carpet(new_x, new_y, a, b, current_depth + 1, depth)


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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
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
