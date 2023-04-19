import pandas as pd
import numpy as np
import cv2


landmark_list = {
    "wrist": 0,
    "thumb_cmc": 0,
    "thumb_mcp": 0,
    "thumb_ip": 0,
    "thumb_tip": 0,
    "index_finger_mcp": 0,
    "index_finger_pip": 0,
    "index_finger_dip": 0,
    "index_finger_tip": 0,
    "middle_finger_mcp": 0,
    "middle_finger_pip": 0,
    "middle_finger_dip": 0,
    "middle_finger_tip": 0,
    "ring_finger_mcp": 0,
    "ring_finger_pip": 0,
    "ring_finger_dip": 0,
    "ring_finger_tip": 0,
    "pinky_finger_mcp": 0,
    "pinky_finger_pip": 0,
    "pinky_finger_dip": 0,
    "pinky_finger_tip": 0
}


def get_current_landmarks(image, hand_landmarks):

    landmarks = {}
    for i, key in enumerate(landmark_list.keys()):
        landmarks[key] = (int(hand_landmarks.landmark[i].x * image.shape[1]),
                          int(hand_landmarks.landmark[i].y * image.shape[0]))
    
    return landmarks

def predict_gesture(model, landmarks):
    landmarks = list(landmarks.values())

    # Make them relative to each other so that it doesnt matter if hand is on left side or right side
    landmarks = list(map(lambda l: (l[0] - landmarks[0][0], l[1] - landmarks[0][1]), landmarks))

    # Normalize them so that distance from camera doesnt matter
    getx = lambda i: abs(i[0])
    gety = lambda i: abs(i[1])

    max_x = max(list(map(getx, landmarks)))
    max_y = max(list(map(gety, landmarks)))

    # final_landmarks = list(map(lambda l: (round(l[0]/max_x, 5), round(l[1]/max_y, 5)), landmarks))
    final_landmarks = list(map(lambda l: (l[0]/max_x, l[1]/max_y), landmarks))
    
    
    arr = []
    for i in range(21):
        arr.append(final_landmarks[i][0])
        arr.append(final_landmarks[i][1])
        
    predict_result = model.predict(np.array([arr]), verbose=False)
    # print(np.squeeze(predict_result))
    result = np.argmax(np.squeeze(predict_result))
    
    dic = {
        0: "Backward",
        1: "Down",
        2: "Flip",
        3: "Forward",
        4: "Land",
        5: "Left",
        6: "Right",
        7: "Up"
    }
    
    return dic[result] 
    
def create_dataset(landmarks, label, dataset):
    landmarks = list(landmarks.values())

    # Make them relative to each other so that it doesnt matter if hand is on left side or right side
    landmarks = list(map(lambda l: (l[0] - landmarks[0][0], l[1] - landmarks[0][1]), landmarks))

    # Normalize them so that distance from camera doesnt matter
    getx = lambda i: abs(i[0])
    gety = lambda i: abs(i[1])

    max_x = max(list(map(getx, landmarks)))
    max_y = max(list(map(gety, landmarks)))

    # final_landmarks = list(map(lambda l: (round(l[0]/max_x, 5), round(l[1]/max_y, 5)), landmarks))
    final_landmarks = list(map(lambda l: (l[0]/max_x, l[1]/max_y), landmarks))

    df = pd.read_csv(dataset, index_col=0)
    columns = list(landmark_list.keys())
    
    num = df.shape[0]
    
    for i, col in enumerate(columns):
        df.loc[num, col+'_x'] = final_landmarks[i][0]
        df.loc[num, col+'_y'] = final_landmarks[i][1]
    df.loc[num, 'label'] = label

    df.to_csv(dataset)
    print(num)

def Action(gesture, tello, voice = False):
    speed = 40
    lr = fb = ud = 0
    # takeoff = False
    try:
        gesture = gesture.lower()
        if gesture == "land":
            tello.land()
            # takeoff = False

        elif gesture == "forward":
            fb = speed

        elif gesture == "backward":
            fb = -speed

        elif gesture == "left":
            lr = -speed

        elif gesture == "right":
            lr = speed

        elif gesture == "up":
            # if not takeoff:
            #     tello.takeoff()
            #     takeoff = True
            # else:
            ud = speed

        elif gesture == "down":
            ud = -speed

        elif gesture == "flip":
            tello.flip_left()

        # send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
        tello.send_rc_control(lr, fb, ud, 0)
        lr = fb = ud = 0
        if not voice:
            tello.send_rc_control(lr, fb, ud, 0)


    except Exception as e:
        print('Command exception, SHUTTING DOWN')
        tello.land()


def get_tello_video(tello):
    tello.streamon()
    frame_read = tello.get_frame_read()
    # Continuously read frames from Tello video stream
    while True:
        # Get frame from Tello video stream
        frame = tello.get_frame_read().frame

        # Display frame in OpenCV window
        cv2.imshow("Tello Video Stream", frame)

        # Wait for user to press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



