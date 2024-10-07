from OpenGL.GL import *
import numpy as np

class Map:
    def __init__(self, mapX, mapY, mapS, map_array):
        self.mapX = mapX
        self.mapY = mapY
        self.mapS = mapS
        
        # Convert the 1D map_array into a 2D array and flip the rows
        self.map_array_2d = np.array(map_array).reshape(self.mapY, self.mapX)
        self.map_array_2d = np.flipud(self.map_array_2d)
        
    def drawMap2D(self):
        for y in range(self.mapY):
            for x in range(self.mapX):
                # Determine the color (white for walls, black for empty space)
                if self.map_array_2d[y, x] == 1:
                    glColor3f(1.0, 1.0, 1.0)  # White for walls
                else:
                    glColor3f(0.0, 0.0, 0.0)  # Black for empty space
                
                # Calculate the position of the current cell
                xo = x * self.mapS
                yo = y * self.mapS  
                
                # Draw the cell as a filled rectangle (quad)
                glBegin(GL_QUADS)
                glVertex2i(0 + xo + 1, 0 + yo + 1)
                glVertex2i(0 + xo + 1, self.mapS + yo - 1)
                glVertex2i(self.mapS + xo - 1, self.mapS + yo - 1)
                glVertex2i(self.mapS + xo - 1, 0 + yo + 1)
                glEnd()