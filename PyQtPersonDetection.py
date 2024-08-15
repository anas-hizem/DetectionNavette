import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import numpy as np
from utils_prin import initialize_model_and_tracker, get_detections, update_tracker, draw_lines, process_tracker_results

class VideoCapture(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize model and tracker
        self.model, self.tracker = initialize_model_and_tracker()
        self.classNames = ['green_sign', 'person', 'red_sign', 'stop_panel']
        self.cap = cv2.VideoCapture('/home/anas/DetectionNavette/test4.mp4')
        
        if not self.cap.isOpened():
            print("Error: Could not open video stream.")
            sys.exit()
        
        self.total_count_up = []
        self.total_count_down = []
        self.entry_crossed = set()
        self.exit_crossed = set()

        
        # Setup GUI
        self.initUI()
        
        # Timer for updating the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Adjust the timeout for your frame rate

    


    def initUI(self):
        self.setWindowTitle('Person Detection')
        self.setGeometry(100, 100, 1000, 500)

        
        self.image_label = QLabel(self)
        self.image_label.resize(720, 480)
        
    
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_frame(self):
        ret, img = self.cap.read()
        if not ret:
            return
                
        desired_width = 1000
        desired_height = 500

        # Calculer dynamiquement les positions des lignes de référence
        entry_line = (0, desired_height // 2, desired_width, desired_height // 2)  # Ligne horizontale au milieu
        exit_line = (0, (desired_height // 2) + 80, desired_width, (desired_height // 2) + 80)  # Ligne horizontale en dessous


        img = cv2.resize(img, (desired_width, desired_height))
        detections = get_detections(img, self.model, self.classNames)
        results_tracker = update_tracker(self.tracker, detections)
        #draw_lines(img, (0, 240, 720, 240), (0, 290, 720, 290))
        draw_lines(img, entry_line, exit_line)

        entry_count, exit_count, current_count = process_tracker_results(
            img, results_tracker, (0, 240, 720, 240), (0, 290, 720, 290),
            self.entry_crossed, self.exit_crossed, self.total_count_up, self.total_count_down
        )
        
        # Update GUI labels

        
        # Convert the image to QImage and display it
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoCapture()
    window.show()
    sys.exit(app.exec_())
