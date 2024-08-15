import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from utils_prin import initialize_model_and_tracker, perform_inference, process_and_display_results

class VideoCapture(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Object Detection')
        self.setGeometry(100, 100, 1000, 500)

        # Initialize the model and tracker
        self.model, self.tracker = initialize_model_and_tracker()

        # Create a QLabel to display the video
        self.image_label = QLabel(self)
        self.image_label.resize(720, 480)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer for updating the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Open the camera

        url ='/home/anas/DetectionNavette/test3.mp4'
        self.cap = cv2.VideoCapture(url)

        #self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open video stream.")
            self.close()

        self.frame = None

        # Automatically start detection
        self.start_detection()

    def start_detection(self):
        self.timer.start(30)  # Update every 30 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            return

        frame = cv2.resize(frame, (1000, 500))
        results = perform_inference(self.model, frame, device='0')
        process_and_display_results(frame, results, self.model)

        # Convert frame to QImage
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        q_img = QImage(frame.data, width, height, width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Update the QLabel with the new frame
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        #cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCapture()
    window.show()
    sys.exit(app.exec_())
