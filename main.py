from djitellopy import Tello
import cv2
import mediapipe as mp
import tensorflow as tf
import time
from utils import predict_gesture, get_current_landmarks, Action


drone = Tello()
drone.connect()
print(f"BATTERY : {drone.get_battery()}%")

HOLD_TIME_THRESHOLD = 1
model_save_path = "main_model.hdf5"
classFile = 'gesture.names'
model = tf.keras.models.load_model(model_save_path)
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
    print()
    print()
    print()
    print()
    print(classNames)
    print()
    print()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.7, min_tracking_confidence=0.5)


first_run = True
set_gesture = None
cap = cv2.VideoCapture(0)
time.sleep(3)
drone.takeoff()
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    cv2.putText(frame, f"FPS: {fps}", (1000, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Detections
    results = hands.process(image)
    # image back to BGR for rendering
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            landmarks = get_current_landmarks(image, hand_landmarks)
            current_gesture = predict_gesture(model, landmarks)
            cv2.putText(image, current_gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
            if first_run:
                set_gesture = current_gesture
                hold_start_time = time.time()
                prev_gesture = current_gesture
                first_run = False
                
            if current_gesture != prev_gesture:
                hold_start_time = time.time()
                prev_gesture = current_gesture
                
            if time.time() - hold_start_time > HOLD_TIME_THRESHOLD:
                set_gesture = current_gesture
            
            if set_gesture != current_gesture:
                print(f"Next Change: Hold {current_gesture} for {round(HOLD_TIME_THRESHOLD - (time.time() - hold_start_time), 2)}s")
            print(f"label: {set_gesture}\n")

            Action(set_gesture, drone)

    cv2.imshow('Webcam Feed', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Clean up
# tello.streamoff()
cv2.destroyAllWindows()
