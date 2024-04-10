import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

data_type_vertex = np.dtype(
    {
        "names": ["x", "y", "z", "color"],
        "formats": [np.float32, np.float32, np.float32, np.uint32],
        "offsets": [0, 4, 8, 12],
        "itemsize": 16,
    }
)


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
