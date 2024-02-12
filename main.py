#!/usr/bin/python
"""
Move a wireframe shape with arrow keys + "n" and "m"
Reset shape with "r"

Most math from Gustavo Niemeyer
"""
from pygame.locals import *
import pygame.draw
import pygame.time

from math import sin, cos

ORIGINX = 0
ORIGINY = 0

CAMERA_FOCAL_DISTANCE = 200
CAMERA_X = 0
CAMERA_Y = 0
CAMERA_Z = 0

def draw_3dline(surface, color, a, b, camera_distance): 
    """Convert 3D coordinates to 2D with perspective projection and draw line."""
    try:
        ax = (a[0] - CAMERA_X) / (1 - (a[2] - CAMERA_Z) / camera_distance) + surface.get_width() / 2
        ay = (a[1] - CAMERA_Y) / (1 - (a[2] - CAMERA_Z) / camera_distance) + surface.get_height() / 2
        bx = (b[0] - CAMERA_X) / (1 - (b[2] - CAMERA_Z) / camera_distance) + surface.get_width() / 2
        by = (b[1] - CAMERA_Y) / (1 - (b[2] - CAMERA_Z) / camera_distance) + surface.get_height() / 2
        pygame.draw.line(surface, color, (ax, ay), (bx, by))
    except Exception:
        pass

def draw_shape(surface, color, shape):
    """Draw 3D shape."""
    a, b, c, d, e, f, g, h = shape
    draw_3dline(surface, color, a, b, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, b, c, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, c, d, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, d, a, CAMERA_FOCAL_DISTANCE)
    
    draw_3dline(surface, color, e, f, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, f, g, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, g, h, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, h, e, CAMERA_FOCAL_DISTANCE)
    
    draw_3dline(surface, color, a, e, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, b, f, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, c, g, CAMERA_FOCAL_DISTANCE)
    draw_3dline(surface, color, d, h, CAMERA_FOCAL_DISTANCE)

def rotate_3dpoint(p, angle, axis, camera_pos):
    """Rotate a 3D point around given axis."""
    x, y, z = p
    cx, cy, cz = camera_pos

    # Translate point relative to camera position
    x -= cx
    y -= cy
    z -= cz

    cosAngle = cos(angle)
    sinAngle = sin(angle)

    # Apply rotation based on camera orientation
    if axis == (1, 0, 0):  # Rotate around X-axis
        new_y = y * cosAngle - z * sinAngle
        new_z = y * sinAngle + z * cosAngle
        y, z = new_y, new_z
    elif axis == (0, 1, 0):  # Rotate around Y-axis
        new_x = x * cosAngle + z * sinAngle
        new_z = -x * sinAngle + z * cosAngle
        x, z = new_x, new_z
    elif axis == (0, 0, 1):  # Rotate around Z-axis
        new_x = x * cosAngle - y * sinAngle
        new_y = x * sinAngle + y * cosAngle
        x, y = new_x, new_y

    # Translate point back relative to camera position
    x += cx
    y += cy
    z += cz

    return [x, y, z]

def rotate_object(obj, angle, axis):
    """Rotate an object around given axis."""
    global CAMERA_X, CAMERA_Y, CAMERA_Z
    for i in range(len(obj)):
        obj[i] = rotate_3dpoint(obj[i], angle, axis, (CAMERA_X, CAMERA_Y, CAMERA_Z))

def main():
    global ORIGINX, ORIGINY, CAMERA_X, CAMERA_Y, CAMERA_Z, CAMERA_FOCAL_DISTANCE
    pygame.init()
    screen = pygame.display.set_mode((640,400))
    # Move origin to center of screen
    ORIGINX = screen.get_width()/2
    ORIGINY = screen.get_height()/2
    shape = [(-50,50,50),  (50,50,50),  (50,-50,50),  (-50,-50,50),
            (-50,50,-50), (50,50,-50), (50,-50,-50), (-50,-50,-50)]
    while 1:
        draw_shape(screen, (255, 255, 255), shape)
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        pygame.display.flip()
        pygame.time.delay(25)
        draw_shape(screen, 0, shape)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            CAMERA_X += 3
        if keys[pygame.K_a]:
            CAMERA_X -= 3
        if keys[pygame.K_w]:
            CAMERA_Y -= 3 # Y is inverted...
        if keys[pygame.K_s]:
            CAMERA_Y += 3
        if keys[pygame.K_e]:
            CAMERA_Z += 3
        if keys[pygame.K_q]:
            CAMERA_Z -= 3
        if keys[pygame.K_n]:
            rotate_object(shape, 0.1, (0,0,1))
        if keys[pygame.K_m]:
            rotate_object(shape, -0.1, (0,0,1))
        if keys[pygame.K_RIGHT]:
            rotate_object(shape, 0.1, (0,1,0))
        if keys[pygame.K_LEFT]:
            rotate_object(shape, -0.1, (0,1,0))
        if keys[pygame.K_UP]:
            rotate_object(shape, 0.1, (1,0,0))
        if keys[pygame.K_DOWN]:
            rotate_object(shape, -0.1, (1,0,0))
        if keys[pygame.K_u]:
            CAMERA_FOCAL_DISTANCE += 3
        if keys[pygame.K_j]:
            CAMERA_FOCAL_DISTANCE -= 3
        if keys[pygame.K_r]: # Reset the shape positions
            shape = [(-50,50,50),  (50,50,50),  (50,-50,50),  (-50,-50,50),
            (-50,50,-50), (50,50,-50), (50,-50,-50), (-50,-50,-50)]
            CAMERA_X = 0
            CAMERA_Y = 0
            CAMERA_Z = 0

if __name__ == "__main__":
    main()