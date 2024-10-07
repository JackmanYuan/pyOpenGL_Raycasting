import glfw
from OpenGL.GL import *
from map import Map  # Import the Map class
from player import Player  # Import the Player class
from ray import Ray # Import the Ray class

# Map dimensions and array
mapX = 10
mapY = 10
mapS = 40

# The map array (1 represents wall, 0 represents empty space)
map_array = [
    1,1,1,1,1,1,1,1,1,1,
    1,0,1,0,0,0,0,0,0,1,
    1,0,1,0,0,0,0,0,0,1,
    1,0,1,1,1,0,0,0,0,1,
    1,0,0,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,1,0,1,
    1,0,1,1,1,0,0,1,0,1,
    1,0,0,0,0,1,1,1,0,1,
    1,0,0,0,0,0,0,0,0,1,
    1,1,1,1,1,1,1,1,1,1,
]

def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW can NOT be initialized")
    
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can NOT be created")
    
    glfw.make_context_current(window)
    return window

def setup_2d_viewpoint(width, height):
    glViewport(0, 0, width, height)  # Set the viewport
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix
    glLoadIdentity()  # Reset Projection Matrix
    
    # Set up orthographic projection (for 2D rendering)
    glOrtho(0, width, 0, height, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    width = 960
    height = 480
    window = init_window(width, height, "OpenGL 2D Map")
    setup_2d_viewpoint(width, height)
    
    # Initialize the map and player objects
    map_obj = Map(mapX, mapY, mapS, map_array)
    player_obj = Player(2 * mapS, 2 * mapS, 0, mapS)
    ray_obj = Ray(num_rays=60, fov=60, screen_width=width, screen_height=height)
    
    # Main loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
        
        player_obj.handle_input(window, map_obj)  # Handle player input
        map_obj.drawMap2D()  # Draw the 2D map grid
        player_obj.drawPlayer2D()  # Draw the player
        ray_obj.cast_rays(player_obj, map_obj)
        
        # Swap front and back buffers
        glfw.swap_buffers(window)
        
        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
