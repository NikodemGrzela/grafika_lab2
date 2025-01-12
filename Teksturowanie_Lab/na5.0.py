#!/usr/bin/env python3
import math
import sys
import itertools

import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

button_pressed = 0
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

N = 20
x = np.linspace(0.0, 1.0, N)
y = np.linspace(0.0, 1.0, N)
tex_map = np.array(np.meshgrid(x, y)).transpose(1, 2, 0)
for i in range(N):
    tex_map[i, -1, :] = tex_map[-(i + 1), 0, :]


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

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("ben.tga")
    # image0_info = [image.size[0], image.size[1], image.tobytes("raw", "RGB", 0, -1)]

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


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
    tab = np.zeros((N,N,3))
    tablica_u = np.linspace(0.0, 1.0, N)
    tablica_v = np.linspace(0.0, 1.0, N)

    for i in range(N):
        for j in range(N):
            u = tablica_u[j]
            v = tablica_v[i]
            tab[i][j][0] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.cos(math.pi * v)
            tab[i][j][1] = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            tab[i][j][2] = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * math.sin(math.pi * v)
    return tab


def draw_egg(tab, N):
    tablica_u = np.linspace(0.0,1.0,N)
    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        # szerokosc
        for j in range(math.floor(N / 2)):
            vertex1 = tab[N - 1 - i,j]
            u1 = tablica_u[i] / 2 +0.75
            v = j * (1.0 / (math.floor(N / 2) - 1.0))

            glTexCoord2f(u1, v)
            glVertex3f(*vertex1)

            if i + 1 == N:
                i = -1
            vertex2 = tab[N - 2 - i, j]
            u2 = tablica_u[i + 1] / 2 + 0.75
            glTexCoord2f(u2, v)
            glVertex3f(*vertex2)
            if i == -1:
                i = N - 1

        glEnd()

    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)

        for j in range(math.floor(N / 2)):
            vertex1 = tab[N - 1 - i, N - 1 - j]
            u1 = tablica_u[i] /2 + 0.25

            v = j * (1.0 / (math.floor(N / 2) - 1.0))

            glTexCoord2f(u1, v)
            glVertex3f(*vertex1)

            if i + 1 == N:
                i = -1
            vertex2 = tab[N - 2 - i, N - 1 - j]
            u2 = tablica_u[i + 1] / 2 + 0.25
            glTexCoord2f(u2, v)
            glVertex3f(*vertex2)
            if i == -1:
                i = N - 1

        glEnd()

    glFlush()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    global N
    global theta
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # spin(time * 180 / 3.1415)
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)
    tab = calculate_egg_points(int(N))

    axes()
    draw_egg(tab, int(N))

    glFlush()


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


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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
