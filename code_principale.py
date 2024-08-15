from ultralytics import YOLO
import cv2
import cvzone
import time
#import Jetson.GPIO as GPIO
from utils_prin import initialize_model_and_tracker, get_detections, update_tracker, draw_lines, process_tracker_results,perform_inference, process_and_display_results,process_frame


def main():
    #camera
    cap = cv2.VideoCapture('tes2.mp4')
    #cap1 = cv2.VideoCapture(1)
    model, tracker = initialize_model_and_tracker()
    classNames = ['green_sign', 'person', 'red_sign', 'stop_panel']

    entry_line = [103, 180, 600, 180]
    exit_line = [103, 161, 600, 161]
    total_count_up = []
    total_count_down = []
    entry_crossed = set()
    exit_crossed = set()
    #init GPIO
    # Configuration des GPIO pour les LED
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setwarnings(False)
    LED_RED = 11   # Broche physique 11 (correspond à GPIO 17 en mode BCM)
    LED_GREEN = 13 # Broche physique 13 (correspond à GPIO 27 en mode BCM)
    LED_BLUE = 37  # Broche physique 15 (correspond à GPIO 22 en mode BCM)
    # GPIO.setup(LED_RED, GPIO.OUT)
    # GPIO.setup(LED_GREEN, GPIO.OUT)
    # GPIO.setup(LED_BLUE, GPIO.OUT)

    while True:
        success, img = cap.read()
        #success1, frame = cap1.read()
        #success2, frame1 = cap2.read()
        # Réinitialiser les LED
        # GPIO.output(LED_RED, GPIO.LOW)
        # GPIO.output(LED_GREEN, GPIO.LOW)
        # GPIO.output(LED_BLUE, GPIO.LOW)
        #person_detection :
        detections = get_detections(img, model, classNames)
        results_tracker = update_tracker(tracker, detections)
        draw_lines(img, entry_line, exit_line)
        
        total = process_tracker_results(img, results_tracker, entry_line, exit_line, entry_crossed, exit_crossed, total_count_up, total_count_down)
        
        
        #trafic :
        #results = perform_inference(model, frame, device='0')  # Ensure the model runs on GPU by specifying device='0'
        #Process and display the results
        #process_and_display_results(frame, results, model)
        

        #object
        
        #process_frame(frame,model,TARGET_CLASSES)
        
        #cv2.imshow('Live Detection', frame)
        cv2.imshow("person_compte", img)
        
        if classNames == 'stop_panel':
                        #GPIO.output(LED_BLUE, GPIO.HIGH)
                        time.sleep(1)
        if classNames == 'car':
                        #GPIO.output(LED_LED_GREEN, GPIO.HIGH)
                        time.sleep(1)
        if total == 6:
                        #GPIO.output(LED_RED, GPIO.HIGH)
                        time.sleep(1)
                        

        # Stop condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()