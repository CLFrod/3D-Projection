import pygame
import numpy as np
import math
from math import *

import pygame as pygame

WIDTH, HEIGHT = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
pygame.display.set_caption('3D Shapes')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

angle = 0
angle2 = 0
scale = 100
midpoint = (WIDTH / 2, HEIGHT / 2)

points = []


# VERTICES 1-8
points.append(np.matrix([-1, -1, 1]))  # 0 - AND THE ORDER MATTERS
points.append(np.matrix([1, -1, 1]))  # 1
points.append(np.matrix([1, 1, 1]))  # 2
points.append(np.matrix([-1, 1, 1]))  # 3
points.append(np.matrix([-1, -1, -1]))  # 4
points.append(np.matrix([1, -1, -1]))  # 5
points.append(np.matrix([1, 1, -1]))  # 6
points.append(np.matrix([-1, 1, -1]))  # 7

# TAKE THE NEGATIVE OF THE # to get the opposite side
# points.append(np.matrix([0, 1, 0]))  # bottom face
# points.append(np.matrix([1, 0, 0]))  # right face
# points.append(np.matrix([0, 0, 1]))  # face at the back
# points.append(np.matrix([0, 0, 0]))  # front face

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
    # This is the whole projection matrix that multiplies with each point, except you dont need the 3rd
    # part of the matrix, [0,0,0] because its unchanged anyways.
])

projected_points = [[n, n] for n in range(len(points))]

clock = pygame.time.Clock()  # FIRST PART OF CLOCK SETUP


def connect_points(i, j, projected_points):
    pygame.draw.line(screen, BLACK, (projected_points[i][0], projected_points[i][1]),
                     (projected_points[j][0], projected_points[j][1]))
while True:
    clock.tick(1000)  # SETTING UP CLOCK SO THAT IT IS RUNNING AT 60fps only
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # ALLOWS YOU TO QUIT WITH THE X BUTTON AT THE CORNER OF WINDOW
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  # ALLOWS TO QUIT WHEN PRESSING ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


    # update stuff
    # ROTATION MATRICES
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1]
    ])
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)]
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)]
    ])
    d = 5
    keys = pygame.key.get_pressed()
    dt = clock.tick(60)
    if keys[pygame.K_LEFT]:
        angle += 0.01
    if keys[pygame.K_RIGHT]:
        angle -= 0.01

    screen.fill(WHITE)
    height = 0
    # draw stuff
    i = 0
    for point in points:
        # radius = distancefrommid()
        # r = radius * scale
        # h = y - 300

        # POINT.reshape changes the array shapes to 2d
        rotated3d = np.dot(rotation_z, point.reshape(3, 1))
        rotated3d = np.dot(rotation_y, rotated3d)
        # y axis rotation by applying dot product of y matrix
        # rotated2d = np.dot(rotation_z, rotated2d)  # x axist rotation

        projected2d = np.dot(projection_matrix, rotated3d)
        x = int(projected2d[0][0] * scale) + midpoint[0]

        # Grabs list 0 aka the first value, and then grabs the value from that
        y = int(projected2d[1][0] * scale) + midpoint[1]

        projected_points[i] = [x, y]

        pygame.draw.circle(screen, BLUE, ((x), (y)), 5)
        # pygame.draw.circle(screen, RED, (500, 200), 5)
        i += 1

    for p in range(4):
        connect_points(p, (p + 1) % 4, projected_points)
        connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
        connect_points(p + 4, ((p + 4) % 4), projected_points)

    #    pygame.draw.circle(screen, BLUE, (x, y), 5)  # allows to draw circle
    # updater per frame of loop
    pygame.display.update()
