from ultralytics import YOLO
import cv2
from utils_prin import initialize_model_and_tracker, perform_inference, process_and_display_results


def main():
    #Ouverture de la caméra
    #cap1 = cv2.VideoCapture(0)

    url ='test3.mp4'
    cap1 = cv2.VideoCapture(url)

    if not cap1.isOpened():
        print("Error: Could not open video stream.")
        return
    
    model, _ = initialize_model_and_tracker()
    classNames = ['green_sign', 'person', 'red_sign', 'stop_panel']

    desired_width = 720
    desired_height = 480

    while True:
        ret, frame = cap1.read()

        frame = cv2.resize(frame, (desired_width, desired_height))


        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        # Détection des objets
        results = perform_inference(model, frame, device='0')  # Assurez-vous que le modèle utilise le GPU

        # Traitement et affichage des résultats
        process_and_display_results(frame, results, model)

        cv2.imshow('PanelDetection', frame)

        # Condition d'arrêt
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
