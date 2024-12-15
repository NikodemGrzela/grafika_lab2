#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

viewer = [0.0, 0.0, 10.0]

direction = [0.0, 0.0, -1.0]

phi = 0.0
theta = 0.0
pix2angle = 1.0
scale = 1.0

movement_speed = 0.01

keys_pressed = set()

mouse_x_pos_old = 0
mouse_y_pos_old = 0

depth = 3
size = 5
base_tetra = [[0.0, 0.0, size * 1.0],
              [0.0, size * 0.942809, size * -0.333333],
              [size * -0.816497, size * -0.471405, size * -0.333333],
              [size * 0.816497, size * -0.471405, size * -0.333333]]


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


def draw_tetra(a, b, c, d):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glBegin(GL_TRIANGLES)
    glColor3fv(interpolate_color(a))
    glVertex3fv(a)
    glColor3fv(interpolate_color(a))
    glVertex3fv(b)
    glColor3fv(interpolate_color(a))
    glVertex3fv(c)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3fv(interpolate_color(b))
    glVertex3fv(a)
    glColor3fv(interpolate_color(b))
    glVertex3fv(b)
    glColor3fv(interpolate_color(b))
    glVertex3fv(d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3fv(interpolate_color(c))
    glVertex3fv(a)
    glColor3fv(interpolate_color(c))
    glVertex3fv(c)
    glColor3fv(interpolate_color(c))
    glVertex3fv(d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3fv(interpolate_color(d))
    glVertex3fv(b)
    glColor3fv(interpolate_color(d))
    glVertex3fv(c)
    glColor3fv(interpolate_color(d))
    glVertex3fv(d)
    glEnd()


def divide_tetra(a, b, c, d, m):
    v = [[0] * 3 for i in range(6)]
    if m > 0:
        for j in range(3):
            v[0][j] = (a[j] + b[j]) / 2

        for j in range(3):
            v[1][j] = (a[j] + c[j]) / 2

        for j in range(3):
            v[2][j] = (b[j] + c[j]) / 2

        for j in range(3):
            v[3][j] = (a[j] + d[j]) / 2

        for j in range(3):
            v[4][j] = (b[j] + d[j]) / 2

        for j in range(3):
            v[5][j] = (c[j] + d[j]) / 2

        divide_tetra(a, v[0], v[1], v[3], m - 1)
        divide_tetra(v[0], b, v[2], v[4], m - 1)
        divide_tetra(v[1], v[2], c, v[5], m - 1)
        divide_tetra(v[3], v[4], v[5], d, m - 1)
    else:
        draw_tetra(a, b, c, d)


def interpolate_color(v):
    return [
        (v[0] + 1.0) / 2.0,
        (v[1] + 1.0) / 2.0,
        (v[2] + 1.0) / 2.0,
    ]


def update_camera():
    global direction

    theta_rad = math.radians(theta)
    phi_rad = math.radians(phi)

    direction[0] = math.cos(phi_rad) * math.sin(theta_rad)
    direction[1] = math.sin(phi_rad)
    direction[2] = -math.cos(phi_rad) * math.cos(theta_rad)


def handle_movement():
    global viewer

    forward = [x * movement_speed*30 for x in direction]
    right = [
        math.sin(math.radians(theta + 90)),
        0.0,
        -math.cos(math.radians(theta + 90))
    ]

    if "W" in keys_pressed:
        viewer = [viewer[i] + forward[i] for i in range(3)]
    if "S" in keys_pressed:
        viewer = [viewer[i] - forward[i] for i in range(3)]
    if "A" in keys_pressed:
        viewer = [viewer[i] - right[i] for i in range(3)]
    if "D" in keys_pressed:
        viewer = [viewer[i] + right[i] for i in range(3)]


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    update_camera()
    handle_movement()

    look_at = [viewer[i] + direction[i] for i in range(3)]

    gluLookAt(
        viewer[0], viewer[1], viewer[2],
        look_at[0], look_at[1], look_at[2],
        0.0, 1.0, 0.0
    )

    axes()
    divide_tetra(base_tetra[0], base_tetra[1], base_tetra[2], base_tetra[3], depth)

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


def key_callback(window, key, scancode, action, mods):
    global keys_pressed

    key_map = {
        GLFW_KEY_W: "W",
        GLFW_KEY_S: "S",
        GLFW_KEY_A: "A",
        GLFW_KEY_D: "D"
    }

    if key in key_map:
        if action == GLFW_PRESS:
            keys_pressed.add(key_map[key])
        elif action == GLFW_RELEASE:
            keys_pressed.discard(key_map[key])

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global theta, phi
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    delta_y = y_pos - mouse_y_pos_old

    mouse_x_pos_old = x_pos
    mouse_y_pos_old = y_pos

    theta += delta_x * pix2angle
    phi -= delta_y * pix2angle

    phi = max(-89.0, min(89.0, phi))


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
