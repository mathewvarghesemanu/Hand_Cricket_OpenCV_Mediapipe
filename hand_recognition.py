import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
class HandDetector:



    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        #when the mediapipe is first started, it detects the hands. After that it tries to track the hands
        #as detecting is more time consuming than tracking. If the tracking confidence goes down than the
        #specified value then again it switches back to detection
        self.hands = mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

        self.allf={
                        "thumbf":False,
                        "indexf":False,
                        "middlef":False,
                        "ringf":False,
                        "littlef":False,
                    }

    def reset_allf(self):
        self.allf={
                        "thumbf":False,
                        "indexf":False,
                        "middlef":False,
                        "ringf":False,
                        "littlef":False,
                    }
        return True
    def gesture_count_to_finger_mapping(self,handLandmarks):
        if(len(handLandmarks) != 0 and handLandmarks!=[0, 0, 0, 0]):
      #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
      #details: https://google.github.io/mediapipe/solutions/hands


            if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
                self.allf["thumbf"]=True

            elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
                self.allf["thumbf"]=True

            if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
                self.allf["indexf"]=True

            if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
                self.allf["middlef"]=True

            if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
                self.allf["ringf"]=True

            if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
                self.allf["littlef"]=True
        return True
        
    def fingerlogic(self):
        if not self.allf["thumbf"] and not self.allf["indexf"] and not self.allf["middlef"] and not self.allf["ringf"] and not self.allf["littlef"]:
            # count=10
            count=0
        elif self.allf["thumbf"] and self.allf["littlef"] and not self.allf["middlef"] and not self.allf["ringf"] and not self.allf["indexf"]:
            # count=9
            count=2
        elif self.allf["thumbf"] and self.allf["indexf"] and self.allf["middlef"] and not self.allf["ringf"] and not self.allf["littlef"]:
            # count=8
            count=3
        elif self.allf["thumbf"] and self.allf["indexf"] and not self.allf["middlef"] and not self.allf["ringf"] and not self.allf["littlef"]  :
            # count=7
            count=2
        elif self.allf["thumbf"] and not self.allf["indexf"] and not self.allf["middlef"] and not self.allf["ringf"] and not self.allf["littlef"]:
            count=6
        else:
            count= int(self.allf["thumbf"])+int(self.allf["indexf"])+int(self.allf["middlef"])+int(self.allf["ringf"])+int(self.allf["littlef"])
        return count

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []
        handflag=False

        if results.multi_handedness:
            label = results.multi_handedness[handNumber].classification[0].label  # label gives if hand is left or right
            #account for inversion in webcams
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"


        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands
            handflag=True
            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos, label])
                
            if draw:
                mp_drawing.draw_landmarks(originalImage, hand, mp_hands.HAND_CONNECTIONS)
        else:
            handflag=False
            landMarkList=[0, 0, 0, 0]
        return landMarkList




# # For static images:
# IMAGE_FILES = []
# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(IMAGE_FILES):
#     # Read an image, flip it around y-axis for correct handedness output (see
#     # above).
#     image = cv2.flip(cv2.imread(file), 1)
#     # Convert the BGR image to RGB before processing.
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Print handedness and draw hand landmarks on the image.
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image,
#           hand_landmarks,
#           mp_hands.HAND_CONNECTIONS,
#           mp_drawing_styles.get_default_hand_landmarks_style(),
#           mp_drawing_styles.get_default_hand_connections_style())
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
#     # Draw hand world landmarks.
#     if not results.multi_hand_world_landmarks:
#       continue
#     for hand_world_landmarks in results.multi_hand_world_landmarks:
#       mp_drawing.plot_landmarks(
#         hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)




#naive finger logic
    # if(len(handLandmarks) != 0):
    #     #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
    #     #details: https://google.github.io/mediapipe/solutions/hands


    #     if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
    #         count = count+1
    #         allf["thumbf"]=True

    #     elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
    #         count = count+1
    #         allf["thumbf"]=True

    #     if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
    #         count = count+1
    #         allf["indexf"]=True

    #     if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
    #         count = count+1
    #         allf["middlef"]=True

    #     if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
    #         count = count+1
    #         allf["ringf"]=True

    #     if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
    #         count = count+1
    #         allf["littlef"]=True