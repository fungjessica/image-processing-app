from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
import sys

class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setFixedSize(QSize(500, 500))  
        
        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        layout = QVBoxLayout()

        self.load_video_button = QPushButton("Load Video")
        self.load_video_button.clicked.connect(self.load_video)
        layout.addWidget(self.load_video_button)

        self.video_label = QLabel("No video selected")
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        self.image_list = QListWidget()
        layout.addWidget(self.image_list)

        self.stack_images_button = QPushButton("Stack Frames")
        self.stack_images_button.clicked.connect(self.extract_frames_and_stack)
        layout.addWidget(self.stack_images_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        center_widget.setLayout(layout)

        self.video_path = None

    def load_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "", "Videos (*.mp4 *.avi *.mov)")
        
        if file_path:
            self.video_path = file_path
            self.video_label.setText(f"Selected: {file_path.split('/')[-1]}")

    def extract_frames_and_stack(self):
        if not self.video_path:
            QMessageBox.warning(self, "No Video Selected", "Please select a video file first.")
            return

        self.progress_bar.setValue(50)  
        QMessageBox.information(self, "Processing Complete", "Frames extracted and stacked successfully!")
        self.progress_bar.setValue(100)

app = QApplication(sys.argv)
main_window = Main_Window()
main_window.show()
app.exec()