from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt
import sys
import os

# allow imports from different folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from conversion_scripts.convertVideo import extract_frames  

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

        self.select_output_button = QPushButton("Select Output Folder")
        self.select_output_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.select_output_button)

        self.output_folder_label = QLabel("No folder selected")
        self.output_folder_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output_folder_label)

        self.stack_images_button = QPushButton("Stack Frames")
        self.stack_images_button.clicked.connect(self.extract_frames_and_stack)
        layout.addWidget(self.stack_images_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        center_widget.setLayout(layout)

        self.video_path = None
        self.output_folder = None

    # load video to be converted into frames
    def load_video(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "", "Videos (*.mp4 *.avi *.mov)")
        
        if file_path:
            self.video_path = file_path
            self.video_label.setText(f"Selected: {file_path.split('/')[-1]}")

    # allow user to select where frames will be saved
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Saving to: {folder}")

    # call function in convertVideo.py
    def extract_frames_and_stack(self):
        if not self.video_path:
            QMessageBox.warning(self, "No Video Selected", "Please select a video file first.")
            return
        
        if not self.output_folder:
            QMessageBox.warning(self, "No Folder Selected", "Please select a folder to save frames.")
            return

        self.progress_bar.setValue(25)

        extracted_folder = extract_frames(self.video_path, self.output_folder)

        if extracted_folder:
            self.progress_bar.setValue(50)
            QMessageBox.information(self, "Processing Complete", f"Frames extracted to {extracted_folder}")
            self.progress_bar.setValue(100)

app = QApplication(sys.argv)
main_window = Main_Window()
main_window.show()
app.exec()