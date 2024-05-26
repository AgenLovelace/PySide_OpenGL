# +---------------------------------------------------------------------------------------------------------------------
# |         Q3DScene.py
# |    This is the main entrance file. This program create a OpenGL context within Qt app to display 3D object.
# +---------------------------------------------------------------------------------------------------------------------
# |     Information :
# | Creation    : 04/05/2024
# | By          : A. Lovelace
# | Last update : 04/05/2024
# +---------------------------------------------------------------------------------------------------------------------
# |     Updates :
# | * N/A
# +---------------------------------------------------------------------------------------------------------------------
# |     ToDo :
# | * N/A
# +---------------------------------------------------------------------------------------------------------------------

# +--- Standard libs
import numpy as np
import ctypes

# +--- OpenGL libs
from OpenGL import GL

# +--- Qt libs
from PySide6.QtWidgets import QWidget
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt

# +--- Custom libs


# +--- Class Definition ------------------------------------------------------------------------------------------------
class Q3DScene(QOpenGLWidget):


    def __init__(self,  parent: QWidget=None):

        # +--- Call parent Ctor
        QOpenGLWidget.__init__(self, parent=parent)

        # +--- Set focus policy to the openGL widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # +--- Define class attribut


    def __init_shader(self):
        """
        Private method.
        Used to load, compile and link shader program.
        """

        print("Q3DScene : Initialize shaders.")

        # +--- Load and compile vertex shader
        vertex_shader_sources = ""
        with open("./Core/Shaders/simple.vert") as vertex_file:
            vertex_shader_sources = vertex_file.read()

        vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        GL.glShaderSource(vertex_shader, vertex_shader_sources)

        # +--- Check compilation error
        error_status = GL.glGetShaderiv(vertex_shader, GL.GL_COMPILE_STATUS)
        if error_status != 0:
            print(f"Q3DScene : Failed to compile vertex shader ! {error_status}")
            print(f"Q3DScene : {GL.glGetShaderInfoLog(vertex_shader)}")


        # +--- Load and compile fragment shader
        fragment_shader_sources = ""
        with open("./Core/Shaders/simple.frag") as fragment_file:
            fragment_shader_sources = fragment_file.read()

        fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(fragment_shader, fragment_shader_sources)

        # +--- Check compilation error
        error_status = GL.glGetShaderiv(fragment_shader, GL.GL_COMPILE_STATUS)
        if error_status != 0:
            print(f"Q3DScene : Failed to compile fragment shader ! {error_status}")
            print(f"Q3DScene : {GL.glGetShaderInfoLog(fragment_shader)}")


        # +--- Link shader
        self.__shader_program = GL.glCreateProgram()
        GL.glAttachShader(self.__shader_program, vertex_shader)
        GL.glAttachShader(self.__shader_program, fragment_shader)
        GL.glLinkProgram(self.__shader_program)

        # +--- Check linking status
        error_status = GL.glGetProgramiv(self.__shader_program, GL.GL_LINK_STATUS)
        if error_status != 1:
            print(f"Q3DScene : Failed to link shader program! {error_status}")
            print(f"Q3DScene : {GL.glGetProgramInfoLog(self.__shader_program)}")

        # +--- clean shader compile sources
        GL.glDeleteShader(vertex_shader)
        GL.glDeleteShader(fragment_shader)


    def initializeGL(self):
        """
        QOpenGLWidget override method.
        Initialize all the OpenGL context.
        """

        self.__init_shader()

        # +--- Setup vertices
        vertices = np.array([
            (-0.5, -0.5, 0.0),
            (0.5, -0.5, 0.0),
            (0.0, 0.5, 0.0)
        ], dtype=np.float32)

        # +--- Create VBO and VAO
        self.__VAO = GL.glGenVertexArrays(1)
        self.__VBO = GL.glGenBuffers(1)
        GL.glBindVertexArray(self.__VAO)

        print(f"Q3DScene : Total vertices size : {vertices.nbytes}")
        print(f"Q3DScene : Stride : {vertices.strides[0]}")

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.__VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, vertices.strides[0], ctypes.c_void_p(0 * vertices.itemsize))
        GL.glEnableVertexAttribArray(0)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)


    def resizeGL(self, width, height):
        """
        QOpenGLWidget override method.
        Trigger method called when widget is resized.
        PARAM :
            width (float) : widget width.
            height (float) : widget height.
        """
        pass


    def paintGL(self):
        """
        QOpenGLWidget override method.
        Methode call each time a redraw is needed.
        The redraw is managed by Pyside.
        """

        # +--- Render
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.__shader_program)
        GL.glBindVertexArray(self.__VAO)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


    def update(self):
        """
        QOpenGLWidget override method.
        Methode call at each frame (exactly when frame buffer are swapped).
        """
        pass


    def print_openGL_infos(self):
        """
        Used to print OpenGL information
        """

        vendor         = GL.glGetString(GL.GL_VENDOR)
        renderer       = GL.glGetString(GL.GL_RENDERER)
        version        = GL.glGetString(GL.GL_VERSION)
        shader_version = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)

        print(f"Q3DScene : Running on OpenGL --->\n\tVENDOR : {vendor}\n\tRENDERER : {renderer}\n\tVERSION : {version}\n\tSHADER_VERSION : {shader_version}")


    def keyPressEvent(self, event):
        """
        Manage Key press event
        """
        if event.key() == Qt.Key.Key_Escape:
            self.__cleanGL()
            self.parent().close()


    def __cleanGL(self):
        pass
        # GL.glDeleteVertexArrays(1, self.__VAO)
        # GL.glDeleteBuffers(1, self.__VBO)
        # GL.glDeleteProgram(self.__shader_program)


