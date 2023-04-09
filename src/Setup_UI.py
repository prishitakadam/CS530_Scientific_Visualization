from PyQt6.QtWidgets import QWidget, QSlider, QGridLayout, QLabel, QPushButton, QTextEdit
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('DVR Head')
        
        # Widgets
        self.centralWidget = QWidget(MainWindow)
        self.gridlayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)

        # Grid Layout
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 4, 4)

        MainWindow.setCentralWidget(self.centralWidget)