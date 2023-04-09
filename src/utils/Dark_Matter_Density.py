from PyQt6.QtWidgets import QMainWindow
from utils.Setup_UI import Ui_MainWindow

class Dark_Matter_Density(QMainWindow):
    def __init__(self, data, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print(data[0])