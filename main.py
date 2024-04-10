from pathlib import Path

import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

glfw.ERROR_REPORTING = "warn"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


def create_shader_module(filepath: str, module_type: int) -> int:
    """
    Compile a shader module.

    Parameters:

        filepath: filepath to the module source code.

        module_type: indicates which type of module to compile.

    returns:

        A handle to the created shader module.
    """

    source_code = ""
    with open(filepath, "r") as file:
        source_code = file.readlines()

    return compileShader(source_code, module_type)


def create_shader_program(vertex_filepath: str, fragment_filepath: str) -> int:
    """
    Compile and link a shader program.

    Parameters:

        vertex_filepath: filepath to the vertex module source code.

        fragment_filepath: filepath to the fragment module source code.

    returns:

        A handle to the created shader program.
    """

    vertex_module = create_shader_module(vertex_filepath, GL_VERTEX_SHADER)
    fragment_module = create_shader_module(fragment_filepath, GL_FRAGMENT_SHADER)

    shader = compileProgram(vertex_module, fragment_module)

    glDeleteShader(vertex_module)
    glDeleteShader(fragment_module)

    return shader


class App:
    window_name = "Title"

    def __init__(self, window_name=None):
        if window_name is not None:
            self.window_name = window_name

        """Initialise the program"""
        # Initialize the library
        if not glfw.init():
            print("Could not initialize OpenGL context")
            exit(1)

        # Use GLFW 3.3 since (3.4 is broken atm)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
        )
        glfw.window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE
        )

        # n.b. the last two parameters None, None set up the
        #  - monitor - where to create the window (defaults to primary)
        #  - share - the context with which this window shares resources (textures, vertex/element buffers, etc...)
        self.window = glfw.create_window(
            SCREEN_WIDTH, SCREEN_HEIGHT, self.window_name, None, None
        )
        if not self.window:
            glfw.terminate()
            print(f"Could not initialize window '{self.window_name}'")
            exit(1)

        glfw.make_context_current(self.window)

        # setup callbacks - glfw does not pull for keys events so we need to listen for them
        glfw.set_key_callback(self.window, self._key_callback)

        glClearColor(0.1, 0.4, 0.2, 1)

    def _key_callback(self, window, key, scancode, action, mods):
        print(key)
        if action == glfw.PRESS:
            print(f"Key {key} was pressed")

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def run(self):
        """Run the app"""

        while not glfw.window_should_close(self.window):

            glfw.poll_events()

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.window)

    def quit(self):
        """cleanup the app, run exit code"""
        glfw.destroy_window(self.window)
        glfw.terminate()


my_app = App("Wassup Gangstas")
my_app.run()
my_app.quit()
