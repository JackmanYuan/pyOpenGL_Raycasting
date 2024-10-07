import glfw
from OpenGL.GL import *
import numpy as np

# Initialize the library
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(640, 480, "Hello OpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

# Make the window's context current
glfw.make_context_current(window)

# Define vertices for a triangle
vertices = np.array([
    -0.5, -0.5, 0.0,  # Left vertex
     0.5, -0.5, 0.0,  # Right vertex
     0.0,  0.5, 0.0   # Top vertex
], dtype=np.float32)

# Main render loop
while not glfw.window_should_close(window):
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Set up the triangle rendering
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    # Draw the triangle
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # Disable the client state
    glDisableClientState(GL_VERTEX_ARRAY)

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW when we're done
glfw.terminate()
