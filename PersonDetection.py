from ultralytics import YOLO
import cv2
import cvzone
from sort import *
import time
#import Jetson.GPIO as GPIO
from utils_prin import initialize_model_and_tracker, get_detections, update_tracker, draw_lines, process_tracker_results



def main():
    #camera
    url ='test4.mp4'
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return
    
    model, tracker = initialize_model_and_tracker()
    classNames = ['green_sign', 'person', 'red_sign', 'stop_panel']

    desired_width = 720
    desired_height = 480

    # entry_line = [103, 180, 600, 180]
    # exit_line = [103, 161, 600, 161]
    # Calculer dynamiquement les positions des lignes de référence
    entry_line = (0, desired_height // 2, desired_width, desired_height // 2)  # Ligne horizontale au milieu
    exit_line = (0, (desired_height // 2) + 50, desired_width, (desired_height // 2) + 50)  # Ligne horizontale en dessous

    total_count_up = []
    total_count_down = []
    entry_crossed = set()
    exit_crossed = set()
    max_capacity = 8
    


    while True:
        ret , img = cap.read()
        img = cv2.resize(img, (desired_width, desired_height))
        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        #person_detection :
        detections = get_detections(img, model, classNames)
        results_tracker = update_tracker(tracker, detections)
        draw_lines(img, entry_line, exit_line)
        
        entry_count, exit_count, current_count  = process_tracker_results(img, results_tracker, entry_line, exit_line, entry_crossed, exit_crossed, total_count_up, total_count_down)
        







        send_data(entry_count, exit_count, current_count)

        
        cv2.imshow("PersonDetection", img)
                        
        # Stop condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()