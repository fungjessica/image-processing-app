from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setFixedSize(QSize(500, 500))