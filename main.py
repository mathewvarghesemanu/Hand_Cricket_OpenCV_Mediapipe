from os import times
import cv2
import mediapipe as mp
from hand_recognition import HandDetector
from computer_logic import Computer_logic
import math
import numpy as np
from itertools import cycle
import time
from score import Score 
import GUI


WINDOW_NAME = "Hand Cricket"


def get_screen_size():
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception:
        return 1280, 720


def resize_to_fit(image, max_width, max_height):
    height, width = image.shape[:2]
    scale = min(max_width / width, max_height / height, 1.0)
    new_width = max(1, int(width * scale))
    new_height = max(1, int(height * scale))
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)
if not webcamFeed.isOpened():
    raise RuntimeError(
        "Could not open the camera. On macOS, enable camera access for the terminal "
        "app you are using, then run the game again."
    )

webcamFeed.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
webcamFeed.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

screen_width, screen_height = get_screen_size()
window_max_width = int(screen_width * 0.9)
window_max_height = int(screen_height * 0.85)

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

computer_brain=Computer_logic()
scores=Score()

counter = cycle([' 3', ' 2', ' 1',  'Show'])
test_computer_logic = cycle([3, 2, 1])

timespan=0
loop_timespan=0
curr_counter=3 
computer_logic_output=0

while True:
    scores.batsman_state="bat"
    scores.is_game_over()
    status, image = webcamFeed.read()
    if not status or image is None:
        raise RuntimeError(
            "Failed to read a frame from the camera. Check that camera access is allowed "
            "and that no other app is using the webcam."
        )

    handDetector.reset_allf()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    handDetector.gesture_count_to_finger_mapping(handLandmarks)
    hand_count=handDetector.fingerlogic()
    if handLandmarks==[0, 0, 0, 0]:
      hand_count=0
    image1=image
    image2=np.zeros(image.shape,np.uint8)
    
    if (time.time()-loop_timespan)>.5:  
      loop_timespan=time.time()
      curr_counter=next(counter)
      if curr_counter=="Show":
        timespan=time.time()
        computer_logic_output=computer_brain.generate_random()
        # computer_logic_output=next(test_computer_logic)
        scores.add_score(hand_count)

        
    if abs(time.time()-timespan)<0.3 and not scores.is_game_over():
      if computer_logic_output==hand_count:
        time.sleep(0.2)
        if computer_logic_output==hand_count:
          scores.set_batsman_state()
          scores.add_wickets()
          scores.sub_score(hand_count)

    image1,image2=GUI.draw_GUI(image1, image2,scores,curr_counter,computer_logic_output,hand_count)
    
    numpy_vertical = np.hstack((image1, image2))
    display_frame = resize_to_fit(numpy_vertical, window_max_width, window_max_height)
    cv2.imshow(WINDOW_NAME, display_frame)
    if scores.is_game_over():
      cv2.waitKey(0)
      scores.reset_game_over()
    else:
      cv2.waitKey(4)
    if scores.batsman_state=="Out":
      scores.reset_batsman_state()


    
