#!/usr/bin/env python3
import math
import sys
import numpy as np

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def shutdown():
    pass


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


def calculate_egg_normal_points(N):
    tab = np.zeros((N, N, 3))
    tab_u_y = np.linspace(0.0, 1.0, N)
    for u in range(N):
        for y in range(N):
            xu = (-450 * tab_u_y[u] ** 4 + 900 * tab_u_y[u] ** 3 - 810 * tab_u_y[u] ** 2 + 360 * tab_u_y[
                u] - 45) * math.cos(math.pi * tab_u_y[y])
            xv = math.pi * (90 * tab_u_y[u] ** 5 - 225 * tab_u_y[u] ** 4 + 270 * tab_u_y[u] ** 3 - 180 * tab_u_y[
                u] ** 2 + 45 * tab_u_y[u]) * math.sin(math.pi * tab_u_y[y])
            yu = 640 * tab_u_y[u] ** 3 - 960 * tab_u_y[u] ** 2 + 320 * tab_u_y[u]
            yv = 0
            zu = (-450 * tab_u_y[u] ** 4 + 900 * tab_u_y[u] ** 3 - 810 * tab_u_y[u] ** 2 + 360 * tab_u_y[
                u] - 45) * math.sin(math.pi * tab_u_y[y])
            zv = -math.pi * (90 * tab_u_y[u] ** 5 - 225 * tab_u_y[u] ** 4 + 270 * tab_u_y[u] ** 3 - 180 * tab_u_y[
                u] ** 2 + 45 * tab_u_y[u]) * math.cos(math.pi * tab_u_y[y])
            magnitude = math.sqrt((yu * zv - zu * yv) ** 2 + (zu * xv - xu * zv) ** 2 + (xu * yv - yu * xv) ** 2)
            if magnitude != 0:
                tab[u, y, 0] = (yu * zv - zu * yv) / magnitude
                tab[u, y, 1] = (zu * xv - xu * zv) / magnitude
                tab[u, y, 2] = (xu * yv - yu * xv) / magnitude
    return tab


def draw_egg(tab, N):
    glPointSize(1.0)
    normal_tab = calculate_egg_normal_points(N)
    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            x, y, z = tab[i, j]
            nx, ny, nz = normal_tab[i, j]
            glNormal(nx, ny, nz)
            glVertex(x, y, z)
    glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    #  spin(time * 180 / 3.1415)

    N = 50
    tab = calculate_egg_points(int(N))

    draw_egg(tab, int(N))

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
