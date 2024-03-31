#!/usr/bin/python
"""
Move virtual camera with "wasd" and rotate the virtual camera with arrow keys + "n" and "m"
Reset shape with "r"

Inspired by Gustavo Niemeyer
Math from Logan Peterson
"""
from pygame.locals import *
import pygame.draw
import pygame.time

from math import sin, cos

ORIGINX = 0
ORIGINY = 0

CAMERA_FOCAL_DISTANCE = 180
CAMERA_X = 0
CAMERA_Y = 0
CAMERA_Z = 0
CAMERA_OFFSET_X = 0
CAMERA_OFFSET_Y = 0
CAMERA_OFFSET_Z = CAMERA_FOCAL_DISTANCE

def draw_3dline(surface, color, a, b, camera_focal_distance): 
    """Convert 3D coordinates to 2D with perspective projection and draw line."""
    if a[2] < (CAMERA_Z+CAMERA_OFFSET_Z) and b[2] < (CAMERA_Z+CAMERA_OFFSET_Z):
        try: # If distance is 0 then dont run it (Dont divide by 0)
            ax = (a[0] - CAMERA_X) / (1 - (a[2] - CAMERA_Z) / camera_focal_distance) + surface.get_width() / 2
            ay = (a[1] - CAMERA_Y) / (1 - (a[2] - CAMERA_Z) / camera_focal_distance) + surface.get_height() / 2
            bx = (b[0] - CAMERA_X) / (1 - (b[2] - CAMERA_Z) / camera_focal_distance) + surface.get_width() / 2
            by = (b[1] - CAMERA_Y) / (1 - (b[2] - CAMERA_Z) / camera_focal_distance) + surface.get_height() / 2
            pygame.draw.line(surface, color, (ax, ay), (bx, by))
        except ZeroDivisionError:
            pass
    else:
        try: # If distance is 0 then dont run it (Dont divide by 0)
            ax = (a[0] - CAMERA_X) / (1 - (a[2] - CAMERA_Z) / camera_focal_distance) + surface.get_width() / 2
            ay = (a[1] - CAMERA_Y) / (1 - (a[2] - CAMERA_Z) / camera_focal_distance) + (surface.get_height() / 2)
            bx = (b[0] - CAMERA_X) / (1 - (b[2] - CAMERA_Z) / camera_focal_distance) + surface.get_width() / 2
            by = (b[1] - CAMERA_Y) / (1 - (b[2] - CAMERA_Z) / camera_focal_distance) + (surface.get_height() / 2)
            pygame.draw.line(surface, color, (ax, ay), (bx, by))
        except ZeroDivisionError:
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

def rotate_3dpoint(p, angle, point1, point2):
    """Rotate a 3D point around an axis defined by two points. These points are defined in the world space, not the camera space"""
    x, y, z = p
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    # Define the axis vector
    u, v, w = x2 - x1, y2 - y1, z2 - z1

    # Translate point relative to first point of the axis
    x -= x1
    y -= y1
    z -= z1

    # Normalize the axis
    axis_length = (u**2 + v**2 + w**2)**0.5
    u /= axis_length
    v /= axis_length
    w /= axis_length

    cos_angle = cos(angle)
    sin_angle = sin(angle)

    # Apply rotation using Rodrigues' rotation formula
    x_new = (u*(u*x + v*y + w*z) * (1 - cos_angle) +
             x*cos_angle +
             (-w*y + v*z)*sin_angle)

    y_new = (v*(u*x + v*y + w*z) * (1 - cos_angle) +
             y*cos_angle +
             (w*x - u*z)*sin_angle)

    z_new = (w*(u*x + v*y + w*z) * (1 - cos_angle) +
             z*cos_angle +
             (-v*x + u*y)*sin_angle)

    # Translate point back relative to first point of the axis
    x_new += x1
    y_new += y1
    z_new += z1

    return [x_new, y_new, z_new]

def rotate_object(obj, angle, point1, point2):
    """Rotate an object around given axis."""
    global CAMERA_X, CAMERA_Y, CAMERA_Z
    for i in range(len(obj)):
        obj[i] = rotate_3dpoint(obj[i], angle, point1, point2)

def main():
    global ORIGINX, ORIGINY, CAMERA_X, CAMERA_Y, CAMERA_Z, CAMERA_FOCAL_DISTANCE
    pygame.init()
    screen = pygame.display.set_mode((1920,1080))
    # Move origin to center of screen
    ORIGINX = screen.get_width()/2
    ORIGINY = screen.get_height()/2
    shape = [[-50, 50, 50], [50, 50, 50], [50, -50, 50], [-50, -50, 50],
         [-50, 50, -50], [50, 50, -50], [50, -50, -50], [-50, -50, -50]]
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
        if keys[pygame.K_e]:
            CAMERA_Y -= 3 # Y is inverted...
        if keys[pygame.K_q]:
            CAMERA_Y += 3
        if keys[pygame.K_w]:
            CAMERA_Z -= 3
        if keys[pygame.K_s]:
            CAMERA_Z += 3
        if keys[pygame.K_n]:
            rotate_object(shape, -0.1, (CAMERA_X,CAMERA_Y,CAMERA_Z+1+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_m]:
            rotate_object(shape, 0.1, (CAMERA_X,CAMERA_Y,CAMERA_Z+1+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_RIGHT]:
            rotate_object(shape, -0.1, (CAMERA_X,CAMERA_Y+1,CAMERA_Z+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_LEFT]:
            rotate_object(shape, 0.1, (CAMERA_X,CAMERA_Y+1,CAMERA_Z+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_UP]:
            rotate_object(shape, -0.1, (CAMERA_X+1,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_DOWN]:
            rotate_object(shape, 0.1, (CAMERA_X+1,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z), (CAMERA_X,CAMERA_Y,CAMERA_Z+CAMERA_OFFSET_Z))
        if keys[pygame.K_u]:
            CAMERA_FOCAL_DISTANCE += 3
        if keys[pygame.K_j]:
            CAMERA_FOCAL_DISTANCE -= 3
        if keys[pygame.K_r]: # Reset the shape positions
            shape = [[-50, 50, 50], [50, 50, 50], [50, -50, 50], [-50, -50, 50],
         [-50, 50, -50], [50, 50, -50], [50, -50, -50], [-50, -50, -50]]
            CAMERA_X = 0
            CAMERA_Y = 0
            CAMERA_Z = 0
            CAMERA_FOCAL_DISTANCE = 180

        CAMERA_OFFSET_Z = CAMERA_FOCAL_DISTANCE

if __name__ == "__main__":
    main()