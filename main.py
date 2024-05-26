# +---------------------------------------------------------------------------------------------------------------------
# |         main.py
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
import logging

# +--- Standard libs

# +--- Qt libs
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QVector3D

# +--- Custom libs
from Core.QCustomWidget.Q3DScene import Q3DScene
import Core.Logger


class Main:
    """
    This is the main object.
    It creates a Qt app context + OpenGL Qt widget.
    Then stop until Qt context finish.
    """

    def __init__(self):
        """
        Ctor
        """

        my_app = QApplication()

        my_window = QMainWindow()

        my_scene = Q3DScene(parent=my_window)
        my_window.setCentralWidget(my_scene)
        my_window.resize(640, 480)
        my_window.show()

        my_app.exec()
        my_window.deleteLater()


if __name__ == "__main__":
    """
    Program main entrance
    """
    Main()
