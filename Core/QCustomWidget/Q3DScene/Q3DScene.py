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
from Core.QCustomWidget.Q3DScene.Q3DObject import Q3DObject


# +--- Class Definition ------------------------------------------------------------------------------------------------
class Q3DScene(QOpenGLWidget):


    def __init__(self,  parent: QWidget=None):

        # +--- Call parent Ctor
        QOpenGLWidget.__init__(self, parent=parent)

        # +--- Set focus policy to the openGL widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # +--- Define class attribut
        self.object_in_scene = []


    def initializeGL(self):
        """
        QOpenGLWidget override method.
        Initialize all the OpenGL context.
        """

        # +--- Construct 2 triangles
        self.object_in_scene.append(Q3DObject("Triangle_1", origin=(-0.5, -0.5, 0.0), color=(1.0, 0.0, 0.0), scene=self))
        self.object_in_scene.append(
            Q3DObject("Triangle_2", origin=(0.5, 0.5, 0.0), color=(0.0, 0.0, 1.0), scene=self))

        self.object_in_scene.append(
            Q3DObject("Triangle_3", origin=(0.0, 0.0, 0.0), color=(0.0, 0.0, 1.0), scene=self))


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

        for object in self.object_in_scene:
            object.render()


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

        for object in self.object_in_scene:
            object.destroy()


