#!/usr/bin/python
"""
Move a wireframe shape with arrow keys + "n" and "m"

Most math from Gustavo Niemeyer
"""
from pygame.locals import *
import pygame.draw
import pygame.time

from math import sin, cos

ORIGINX = 0
ORIGINY = 0

CAMERA_FOCAL_DISTANCE = 200

# def draw_3dline(surface, color, a, b):
#     """Convert 3D coordinates to 2D and draw line.""" 
#     ax, ay = a[0]+(a[2]*0.3)+ORIGINX, a[1]+(a[2]*0.3)+ORIGINY
#     bx, by = b[0]+(b[2]*0.3)+ORIGINX, b[1]+(b[2]*0.3)+ORIGINY
#     pygame.draw.line(surface, color, (ax, ay), (bx, by))

def draw_3dline(surface, color, a, b, camera_distance): # My new code with perspective stuff
    """Convert 3D coordinates to 2D with perspective projection and draw line.""" 
    ax, ay = a[0] / (1 - a[2] / camera_distance)+ORIGINX, a[1] / (1 - a[2] / camera_distance)+ORIGINY
    bx, by = b[0] / (1 - b[2] / camera_distance)+ORIGINX, b[1] / (1 - b[2] / camera_distance)+ORIGINY
    pygame.draw.line(surface, color, (ax, ay), (bx, by))


def draw_cube(surface, color, cube):
    """Draw 3D cube."""
    a, b, c, d, e, f, g, h = cube
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

def rotate_3dpoint(p, angle, axis):
    """Rotate a 3D point around given axis."""
    ret = [0, 0, 0]
    cosang = cos(angle)
    sinang = sin(angle)
    ret[0] += (cosang+(1-cosang)*axis[0]*axis[0])*p[0]
    ret[0] += ((1-cosang)*axis[0]*axis[1]-axis[2]*sinang)*p[1]
    ret[0] += ((1-cosang)*axis[0]*axis[2]+axis[1]*sinang)*p[2]
    ret[1] += ((1-cosang)*axis[0]*axis[1]+axis[2]*sinang)*p[0]
    ret[1] += (cosang+(1-cosang)*axis[1]*axis[1])*p[1]
    ret[1] += ((1-cosang)*axis[1]*axis[2]-axis[0]*sinang)*p[2]
    ret[2] += ((1-cosang)*axis[0]*axis[2]-axis[1]*sinang)*p[0]
    ret[2] += ((1-cosang)*axis[1]*axis[2]+axis[0]*sinang)*p[1]
    ret[2] += (cosang+(1-cosang)*axis[2]*axis[2])*p[2]
    return ret

def rotate_object(obj, angle, axis):
    """Rotate an object around given axis."""
    for i in range(len(obj)):
        obj[i] = rotate_3dpoint(obj[i], angle, axis)

def main():
    global ORIGINX, ORIGINY
    pygame.init()
    screen = pygame.display.set_mode((640,400))
    # Move origin to center of screen
    ORIGINX = screen.get_width()/2
    ORIGINY = screen.get_height()/2
    cube = [(0,0,0),  (50,50,50),  (50,-50,50),  (-50,-50,50),
            (-50,50,-50), (50,50,-50), (50,-50,-50), (-50,-50,-50)]
    while 1:
        draw_cube(screen, 255, cube)
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        pygame.display.flip()
        pygame.time.delay(25)
        draw_cube(screen, 0, cube)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            rotate_object(cube, 0.1, (0,1,0))
        if keys[pygame.K_LEFT]:
            rotate_object(cube, -0.1, (0,1,0))
        if keys[pygame.K_UP]:
            rotate_object(cube, 0.1, (0,0,1))
        if keys[pygame.K_DOWN]:
            rotate_object(cube, -0.1, (0,0,1))
        if keys[pygame.K_n]:
            rotate_object(cube, 0.1, (1,0,0))
        if keys[pygame.K_m]:
            rotate_object(cube, -0.1, (1,0,0))
        if keys[pygame.K_r]: # Reset the cube positions
            cube = [(0,0,0),  (50,50,50),  (50,-50,50),  (-50,-50,50),
            (-50,50,-50), (50,50,-50), (50,-50,-50), (-50,-50,-50)]

if __name__ == "__main__":
    main()