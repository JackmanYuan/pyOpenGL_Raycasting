from OpenGL.GL import *
import numpy as np
import math
import glfw

class Player:
    def __init__(self, px, py, pa, mapS):
        self.px = px  # Player x position
        self.py = py  # Player y position
        self.pa = pa  # Player angle
        self.pdx = math.cos(math.radians(self.pa))  # Player direction x component
        self.pdy = -math.sin(math.radians(self.pa))  # Player direction y component
        self.mapS = mapS  # Size of map cellsapY, self.mapX)
        self.speed = 1
        
    def handle_input(self, window, map_obj):
        # Rotate left
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            self.pa -= 2
            self.pa = self.FixAng(self.pa)
            self.pdx = math.cos(math.radians(self.pa))
            self.pdy = -math.sin(math.radians(self.pa))
        
        # Rotate right
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.pa += 2
            self.pa = self.FixAng(self.pa)
            self.pdx = math.cos(math.radians(self.pa))
            self.pdy = -math.sin(math.radians(self.pa))
        
        # Move forward
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            new_px = self.px + self.pdx * self.speed
            new_py = self.py + self.pdy * self.speed
            if not self.collision(new_px, new_py, map_obj):
                self.px = new_px
                self.py = new_py
        
        # Move backward
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            new_px = self.px - self.pdx * self.speed
            new_py = self.py - self.pdy * self.speed
            if not self.collision(new_px, new_py, map_obj):
                self.px = new_px
                self.py = new_py
    
    def FixAng(self, a):
        if a > 359:
            a -= 360
        if a < 0:
            a += 360
        return a
    
    def collision(self, new_px, new_py, map_obj):
        # Check for collision with walls based on new position.
        grid_x = int(new_px // self.mapS)
        grid_y = int(new_py // self.mapS)
        
        # Check if the new position is inside a wall cell
        if map_obj.map_array_2d[grid_y, grid_x] == 1:
            return True # Collision detected
        return False
    
    def drawPlayer2D(self):
        glColor3f(1, 1, 0)  # Yellow color to display player
        glPointSize(8)
        glLineWidth(4)
        
        # Draw player as a point
        glBegin(GL_POINTS)
        glVertex2f(float(self.px), float(self.py))
        glEnd()
        
        # Draw direction line
        glBegin(GL_LINES)
        glVertex2f(float(self.px), float(self.py))  # Player's position
        glVertex2f(float(self.px + self.pdx * 20), float(self.py + self.pdy * 20))  # Player's direction
        glEnd()