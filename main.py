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

    The terminology used by OpenGL can be a bit confusing :sigh:

    So, we refer to the code running at a certain step in the graphics pipeline as a *shader*, but it
    is in fact a **shader module**.

    A full shader program consists of compiled shader modules which are then linked together, e.g.
    a vertex and a fragment shader. This makes sense, since otherwise we wouldn't be able to pass
    data from one to the other (how else could the frament shader now what it can expect as `in`?)

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
        """Setup any context-specif stuff (non graphics related)"""
        if window_name is not None:
            self.window_name = window_name

        """Initialise the program"""
        self.__initialize_glfw()
        self.__initialize_opengl()

    def __initialize_glfw(self) -> None:
        """
        GLFW is a library providing a simple interface for creating windows with OpenGL / OpenGL ES.
        It is also used to handle input events.

        Initialize all glfw related stuff. Make a window, basically.
        """
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

        # makes the OpenGL context of the specified window current on the calling thread,
        # allowing for the management of multiple contexts across different threads
        glfw.make_context_current(self.window)
        # setup callbacks - glfw does not pull for keys events so we need to listen for them
        glfw.set_key_callback(self.window, self.__key_callback)
        # Set the mouse button callback
        glfw.set_mouse_button_callback(self.window, self.__mouse_button_callback)

    def __initialize_opengl(self) -> None:
        """
        Initialize any opengl related stuff.
        """
        glClearColor(0.1, 0.4, 0.2, 1)

        self.VAO = glGenVertexArrays(1)
        self.shader = create_shader_program("shaders/vertex.vert","shaders/fragment.frag")

    def __key_callback(self, window, key, scancode, action, mods):
        """
        Respond to key events that are recieved by the window.
        Currently, we just quit on ESC
        """
        if action == glfw.PRESS:
            print(f"Key {key} was pressed")

        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def __mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            xpos, ypos = glfw.get_cursor_pos(window)
            print(f"Left mouse button pressed at ({xpos}, {ypos})")
        elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
            xpos, ypos = glfw.get_cursor_pos(window)
            print(f"Left mouse button released at ({xpos}, {ypos})")

    def run(self):
        """Run the app"""

        # Classic main event loop: run forever until the user quits
        while not glfw.window_should_close(self.window):
            # clear the color buffer to a preset value (last call to glClearColor)
            glClear(GL_COLOR_BUFFER_BIT)
            
            glUseProgram(self.shader)
            glBindVertexArray(self.VAO)
            glDrawArrays(GL_TRIANGLES, 0,3)
            # we use double buffering be default. swaps the front and back buffers of the specified window
            # (see the rasterization section for info)
            glfw.swap_buffers(self.window)

            """
            processes all pending events in the event queue immediately and then returns,
            ensuring that window and input callbacks associated with those events are called.
            """
            glfw.poll_events()

    def quit(self):
        """cleanup the app, run exit code"""
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()


my_app = App("Wassup Gangstas")
my_app.run()
my_app.quit()
