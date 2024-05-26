# +---------------------------------------------------------------------------------------------------------------------
# |         Q3DScene.py
# |    This is the main entrance file. This program create a OpenGL context within Qt app to display 3D object.
# +---------------------------------------------------------------------------------------------------------------------
# |     Information :
# | Creation    : 26/05/2024
# | By          : A. Lovelace
# | Last update : 04/05/2024
# +---------------------------------------------------------------------------------------------------------------------
# |     Updates :
# | * N/A
# +---------------------------------------------------------------------------------------------------------------------
# |     ToDo :
# | * N/A
# +---------------------------------------------------------------------------------------------------------------------
import os.path

# +--- Standard libs
import numpy as np
import ctypes

# +--- OpenGL libs
from OpenGL import GL

# +--- Qt libs


# +--- Custom libs

# +--- Class Definition ------------------------------------------------------------------------------------------------
class Q3DObject:

    def __init__(self, name="new_object", origin=(0.0, 0.0, 0.0), color=(1.0, 1.0, 1.0), scene=None):

        # +--- Give object a name
        self.name = name

        # +--- Store reference to the scene were object is displayed
        self.scene = scene

        # +--- Define origin point from screen center
        self.origin = origin
        self.color  = color

        # +--- Define array container for position + color and vertex attribute array and indices array.
        self.vertex_array = np.array([
            (-0.3 - self.origin[0], -0.2 - self.origin[1], 0.0 - self.origin[2]), (self.color[0], self.color[1], self.color[2]),
            (0.3 - self.origin[0], -0.2 - self.origin[1], 0.0 - self.origin[2]), (self.color[0], self.color[1], self.color[2]),
            (0.0 - self.origin[0], 0.3 - self.origin[1], 0.0 - self.origin[2]), (self.color[0], self.color[1], self.color[2])
        ], dtype=np.float32)
        self.indices_array = np.array([
            (0, 1, 2)
        ])

        # +--- Handler to VAO, VBO and EBO buffers
        # +--- Handler to shader program
        self.VAO = 0
        self.VBO = 0
        self.EBO = 0
        self.shader_program = 0

        # +--- Store bool info on good init
        self.is_initialized = False

        # +--- Load all info into GC
        self.__init_shader("default", "./Core/Shaders/")
        self.__init_buffer()


    def __init_shader(self, shader_name, shader_dir_path):
        """
        Private method.
        Used to load, compile and link shader program to our 3DObject.
        """

        print(f"Q3DObject {self.name} : Initialize shaders.")
        vertex_shader_path = os.path.join(shader_dir_path, shader_name + ".vert")
        fragment_shader_path = os.path.join(shader_dir_path, shader_name + ".frag")

        if not os.path.exists(vertex_shader_path):
            print(f"Q3DObject {self.name} : Failed to find vertex shader. PATH = {vertex_shader_path}")
            return

        elif not os.path.exists(fragment_shader_path):
            print(f"Q3DObject {self.name} : Failed to find fragment shader. PATH = {fragment_shader_path}")
            return

        # +--- Load and compile vertex shader
        is_no_error = True
        vertex_shader_sources = ""
        with open(vertex_shader_path) as vertex_file:
            vertex_shader_sources = vertex_file.read()

        vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(vertex_shader, vertex_shader_sources)

        # +--- Check compilation error
        error_status = GL.glGetShaderiv(vertex_shader, GL.GL_COMPILE_STATUS)
        if error_status != 0:
            print(f"Q3DObject {self.name} : Failed to compile vertex shader ! {error_status}")
            print(f"Q3DObject {self.name} : {GL.glGetShaderInfoLog(vertex_shader)}")
            is_no_error = False

        # +--- Load and compile fragment shader
        fragment_shader_sources = ""
        with open(fragment_shader_path) as fragment_file:
            fragment_shader_sources = fragment_file.read()

        fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(fragment_shader, fragment_shader_sources)

        # +--- Check compilation error
        error_status = GL.glGetShaderiv(fragment_shader, GL.GL_COMPILE_STATUS)
        if error_status != 0:
            print(f"Q3DObject {self.name} : {GL.glGetShaderInfoLog(fragment_shader)}")
            print(f"Q3DObject {self.name} : Failed to compile fragment shader ! {error_status}")
            is_no_error = False

        # +--- Link shader
        self.__shader_program = GL.glCreateProgram()
        GL.glAttachShader(self.__shader_program, vertex_shader)
        GL.glAttachShader(self.__shader_program, fragment_shader)
        GL.glLinkProgram(self.__shader_program)

        # +--- Check linking status
        error_status = GL.glGetProgramiv(self.__shader_program, GL.GL_LINK_STATUS)
        if error_status != 1:
            print(f"Q3DObject {self.name} : Failed to link shader program! {error_status}")
            print(f"Q3DObject {self.name} : {GL.glGetProgramInfoLog(self.__shader_program)}")
            is_no_error = True

        # +--- clean shader compile sources
        GL.glDeleteShader(vertex_shader)
        GL.glDeleteShader(fragment_shader)

        # +--- Signal that no error occurs
        if is_no_error:
            self.is_initialized = True


    def __init_buffer(self):

        # +--- Create VBO and VAO
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = GL.glGenBuffers(1)
        self.EBO = GL.glGenBuffers(1)
        GL.glBindVertexArray(self.VAO)

        print(f"Q3DScene : Total vertices size : {self.vertex_array.nbytes}")
        print(f"Q3DScene : Stride : {self.vertex_array.strides[0]}")
        print(f"Q3DScene : Total indices size : {self.indices_array.nbytes}")

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertex_array.nbytes, self.vertex_array, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.indices_array.nbytes, self.indices_array, GL.GL_STATIC_DRAW)

        # +--- Load vertex position
        # +--- Vertex array : X,Y,Z, R,G,B
        # +---                ^      ^
        # +---  position offset      color offset
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, self.vertex_array.strides[0], ctypes.c_void_p(0 * self.vertex_array.itemsize))
        GL.glEnableVertexAttribArray(0)

        # +--- Load color position
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, self.vertex_array.strides[0], ctypes.c_void_p(3 * self.vertex_array.itemsize))
        GL.glEnableVertexAttribArray(1)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)  # +--- To disable triangle fill.


    def render(self):

        if self.is_initialized:
            GL.glUseProgram(self.shader_program)
            GL.glBindVertexArray(self.VAO)
            GL.glDrawElements(GL.GL_TRIANGLES,
                              6,
                              GL.GL_UNSIGNED_INT,
                              ctypes.c_void_p(0))  # +--- Last ARGS = offset ---> 0

        else:
            print(f"Q3DObject {self.name} : Object not initialized !!")


    def destroy(self):
        GL.glDeleteVertexArrays(1, self.VAO)
        GL.glDeleteBuffers(1, self.EBO)
        GL.glDeleteBuffers(1, self.VBO)
        GL.glDeleteProgram(self.shader_program)