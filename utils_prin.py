from ultralytics import YOLO
import cv2
import cvzone
import math
import numpy as np
from sort import *

import socket
import json


def send_data_objet(detected_object):
    try:
        # Configuration du socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 65432))  # Adresse IP et port du serveur
        message = json.dumps({"object": detected_object})
        sock.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending data: {e}")
    finally:
        sock.close()


        
def send_data_person(detected_person):
    try:
        # Configuration du socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 65432))  # Adresse IP et port du serveur
        message = json.dumps({"person": detected_person})
        sock.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending data: {e}")
    finally:
        sock.close()


def initialize_model_and_tracker(model_path="/home/anas/DetectionNavette/hamdi_bechir.pt"):
    model = YOLO(model_path)
    tracker = Sort(max_age=40, min_hits=3, iou_threshold=0.3)
    return model, tracker

def get_detections(img, model, classNames):
    results = model(img, stream=True)
    detections = np.empty((0, 5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            if classNames[cls] == "person" :
                current_array = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, current_array))
    return detections

def update_tracker(tracker, detections):
    return tracker.update(detections)

def draw_lines(img, entry_line, exit_line):
    cv2.line(img, (entry_line[0], entry_line[1]), (entry_line[2], entry_line[3]), (0, 0, 255), 3)
    cv2.line(img, (exit_line[0], exit_line[1]), (exit_line[2], exit_line[3]), (0, 0, 255), 3)

def process_tracker_results(img, results_tracker, entry_line, exit_line, entry_crossed, exit_crossed, total_count_up, total_count_down):
    detected_person = {
        "current": 0,
        "entry": 0,
        "exit": 0
    }
    
    for result in results_tracker:
        x1, y1, x2, y2, id = map(int, result)
        w, h = x2 - x1, y2 - y1
        cx, cy = x1 + w // 2, y1 + h // 2

        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Check if person crosses entry line
        if id not in entry_crossed and entry_line[0] < cx < entry_line[2] and entry_line[1] - 5 < cy < entry_line[1] + 5:
            entry_crossed.add(id)
            if id not in exit_crossed:
                total_count_down.append(id)

        # Check if person crosses exit line
        if id not in exit_crossed and exit_line[0] < cx < exit_line[2] and exit_line[1] - 5 < cy < exit_line[1] + 5:
            exit_crossed.add(id)
            if id not in total_count_up:
                total_count_up.append(id)
        
    entry_count = len(total_count_up)
    exit_count = len(total_count_down)
    current_count = entry_count - exit_count
    
    detected_person["current"] = current_count
    detected_person["entry"] = entry_count
    detected_person["exit"] = exit_count

    

    send_data_person(detected_person)
    
    # cvzone.putTextRect(img, f'Entry: {entry_count}', (30, 30))
    # cvzone.putTextRect(img, f'Exit: {exit_count}', (30, 60))
    # cvzone.putTextRect(img, f'Current: {current_count}', (30, 90))

    return entry_count, exit_count, current_count

def perform_inference(model, frame, device='0'):
    return model(frame, device=device)




def process_and_display_results(frame, results, model, confidence_threshold=0.5):
    detected_objects = []
    for result in results:
        boxes = result.boxes.xyxy
        labels = result.boxes.cls
        scores = result.boxes.conf

        for box, label, score in zip(boxes, labels, scores):
            if score > confidence_threshold:  # Filter results based on confidence score
                x1, y1, x2, y2 = map(int, box)
                class_name = model.names[int(label)]
                detected_object = {
                    "class": class_name,
                    "score": score.item(),
                }
                detected_objects.append(detected_object)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{class_name}: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                send_data_objet(detected_object)
    return detected_objects




def process_frame(frame, model, target_classes):
    results = model(frame)[0]
    boxes = results.boxes
    names = results.names
    
    for box in boxes:
        class_id = int(box.cls)
        if class_id in target_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = names[class_id]
            score = box.conf.item()
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 2)