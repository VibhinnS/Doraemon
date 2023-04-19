from vosk import Model, KaldiRecognizer
import pyaudio
from djitellopy import Tello
import cv2
import time


img = cv2.imread(r'images/black_bg.jpg')

try:
    drone = Tello()
    drone.connect()
    print(f"BATTERY : {drone.get_battery()}%")
except:
    pass


classFile = 'gesture.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')
    print()
    print()
    print()
    print(classNames)
    print()
    print()

model= Model(r"vosk-model-small-en-in-0.4/vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)


mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

def main():
    speed = 40
    lr = fb = ud = 0
    while True:
        data = stream.read(4096)
        cv2.putText(img, f"Battery : {drone.get_battery()}%", (170,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow('Image', img)
        # cv2.waitKey(1)
        img[:] = (0, 0, 0)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            print(text[14:-3])
            command = text[14:-3]
            command = command.lower()
            cv2.putText(img, command, (64,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Image', img)
            cv2.waitKey(1)

            if command == "exit":
                break
            if "land" in command:
                drone.land()
                break

            elif "take off" in command:
                drone.takeoff()

            elif "forward" in command:
                fb = speed

            elif "backward" in command:
                fb = -speed

            elif "left" in command:
                lr = -speed

            elif "right" in command:
                lr = speed

            elif "up" in command:
                ud = speed

            elif "down" in command:
                ud = -speed

            elif "flip" in command:
                drone.flip_left()

            # send_rc_control(left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity)
            drone.send_rc_control(lr, fb, ud, 0)
            lr = fb = ud = 0


main()

cv2.destroyAllWindows()


