from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
import sys
import os

# allow imports from different folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from video_conversion import Video_Conversion

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setFixedSize(QSize(500, 500))  

        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.video_button = QPushButton("Video Frame Stacking")
        self.video_button.clicked.connect(self.open_video_conversion)
        button_layout.addWidget(self.video_button)

        self.seestar_button = QPushButton("Seestar Stacking")
        self.seestar_button.clicked.connect(self.open_seestar_stacking)
        button_layout.addWidget(self.seestar_button)

        self.dslr_button = QPushButton("DSLR Stacking (TBD)")
        self.dslr_button.setEnabled(False)
        button_layout.addWidget(self.dslr_button)

        main_layout.addLayout(button_layout)
        center_widget.setLayout(main_layout)

    def open_video_conversion(self):
        self.video_window = Video_Conversion()
        self.video_window.show()

    def open_seestar_stacking(self):
        print("hehe")

app = QApplication(sys.argv)
main_window = Main_Window()
main_window.show()
app.exec()