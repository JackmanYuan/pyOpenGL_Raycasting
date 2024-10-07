import math
from OpenGL.GL import *

class Ray:
    def __init__(self, num_rays=60, fov=60, screen_width=640, screen_height=480):
        self.num_rays = num_rays  # Number of rays to cast
        self.fov = fov  # Field of View in degrees
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.strip_width = self.screen_width // self.num_rays  # Width of each vertical strip on screen

    def cast_rays(self, player, map_obj):
        """Cast rays from the player's position and draw them."""
        ra = self.fix_ang(player.pa - (self.fov // 2))  # Start the ray angle at the left edge of the FOV (subtract FOV/2)
        epsilon = 0.0001  # Small value to avoid division by zero
        strip_width = (self.screen_width // 2) // self.num_rays  # Adjust strip width for 3D scene on the right half

        for r in range(self.num_rays):
            dofV, dofH = 0, 0  # Depth of field
            disV, disH = 100000, 100000  # Set large initial distances
            rx, ry, vx, vy, hx, hy = 0, 0, 0, 0, 0, 0  # Ray hit coordinates
            Tan = math.tan(math.radians(ra))

            ### Vertical Raycasting (Checking intersections with vertical grid lines)
            if math.cos(math.radians(ra)) > 0.001:  # Ray pointing right
                rx = (((int(player.px) // map_obj.mapS) * map_obj.mapS) + map_obj.mapS)  # Round to next grid line
                ry = (player.px - rx) * Tan + player.py  # Calculate intersection
                xo = map_obj.mapS  # Move right by one grid unit
                yo = -xo * Tan  # Adjust y increment based on the angle
            elif math.cos(math.radians(ra)) < -0.001:  # Ray pointing left
                rx = (((int(player.px) // map_obj.mapS) * map_obj.mapS) - 0.0001)  # Round to previous grid line
                ry = (player.px - rx) * Tan + player.py
                xo = -map_obj.mapS  # Move left by one grid unit
                yo = -xo * Tan
            else:  # Ray pointing straight up or down (no vertical intersections)
                rx, ry = player.px, player.py
                dofV = map_obj.mapX

            # Check for vertical intersections
            while dofV < map_obj.mapX:
                mx = int(rx) // map_obj.mapS
                my = int(ry) // map_obj.mapS
                if 0 <= mx < map_obj.mapX and 0 <= my < map_obj.mapY:
                    if map_obj.map_array_2d[my, mx] == 1:  # Wall hit
                        dofV = map_obj.mapX
                        disV = math.sqrt((rx - player.px) ** 2 + (ry - player.py) ** 2)  # Calculate vertical distance
                        vx, vy = rx, ry  # Store vertical hit coordinates
                    else:
                        rx += xo
                        ry += yo
                        dofV += 1
                else:
                    dofV = map_obj.mapX  # Out of bounds

            ### Horizontal Raycasting (Checking intersections with horizontal grid lines)
            if math.sin(math.radians(ra)) > 0.001:  # Ray pointing down
                ry = (((int(player.py) // map_obj.mapS) * map_obj.mapS) - 0.0001)  # Round to next grid line
                rx = (player.py - ry) / Tan + player.px  # Calculate intersection (NOTE: Now using division by Tan)
                yo = -map_obj.mapS  # Move down by one grid unit
                xo = -yo / Tan
            elif math.sin(math.radians(ra)) < -0.001:  # Ray pointing up
                ry = (((int(player.py) // map_obj.mapS) * map_obj.mapS) + map_obj.mapS)  # Round to previous grid line
                rx = (player.py - ry) / Tan + player.px
                yo = map_obj.mapS  # Move up by one grid unit
                xo = -yo / Tan
            else:  # Ray pointing straight left or right (no horizontal intersections)
                rx, ry = player.px, player.py
                dofH = map_obj.mapY

            # Check for horizontal intersections
            while dofH < map_obj.mapY:
                mx = int(rx) // map_obj.mapS
                my = int(ry) // map_obj.mapS
                if 0 <= mx < map_obj.mapX and 0 <= my < map_obj.mapY:
                    if map_obj.map_array_2d[my, mx] == 1:  # Wall hit
                        dofH = map_obj.mapY
                        disH = math.sqrt((rx - player.px) ** 2 + (ry - player.py) ** 2)  # Calculate horizontal distance
                        hx, hy = rx, ry  # Store horizontal hit coordinates
                    else:
                        rx += xo
                        ry += yo
                        dofH += 1
                else:
                    dofH = map_obj.mapY  # Out of bounds

            ### Draw rays for 2D view (for debugging)
            glColor3f(0, 1, 1)  # Cyan color for rays
            
            # print("disV = ", disV, "disH = ", disH)
            if disV < disH:  # Vertical hit is closer
                glBegin(GL_LINES)
                glVertex2f(player.px, player.py)
                glVertex2f(vx, vy)
                glEnd()
                distance = disV

            else:  # Horizontal hit is closer
                glBegin(GL_LINES)
                glVertex2f(player.px, player.py)
                glVertex2f(hx, hy)
                glEnd()
                distance = disH

            # Fix for fish-eye effect
            corrected_dist = distance * math.cos(math.radians(player.pa - ra))

            # Calculate wall height based on corrected distance
            line_height = (self.screen_height * map_obj.mapS) / corrected_dist
            line_height = min(line_height, self.screen_height)  # Clamp to screen height

            # Calculate top and bottom positions of the wall slice
            line_offset = (self.screen_height // 2) - (line_height // 2)

            # Set wall color (different for vertical vs horizontal hit for shading)
            if disV < disH:
                glColor3f(0.8, 0.8, 0.8)  # Lighter color for vertical walls
            else:
                glColor3f(0.6, 0.6, 0.6)  # Darker color for horizontal walls

            # Draw the vertical strip as a quad (to simulate a 3D wall)
            glBegin(GL_QUADS)
            glVertex2f(r * strip_width + (self.screen_width // 2), line_offset)  # Bottom left
            glVertex2f((r + 1) * strip_width + (self.screen_width // 2), line_offset)  # Bottom right
            glVertex2f((r + 1) * strip_width + (self.screen_width // 2), line_offset + line_height)  # Top right
            glVertex2f(r * strip_width + (self.screen_width // 2), line_offset + line_height)  # Top left
            glEnd()

            # Move to the next ray
            ra = self.fix_ang(ra + (self.fov / self.num_rays))  # Increment angle

    def fix_ang(self, a):
        """Fix angle to ensure it stays between 0 and 359 degrees."""
        if a > 359:
            a -= 360
        if a < 0:
            a += 360
        return a
