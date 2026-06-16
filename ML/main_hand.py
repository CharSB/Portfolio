import os
import cv2
import mediapipe as mp
import time

import main_sound as sound
import asyncio

INDEX_FINGER = 8
THUMB = 4
VOL_REFRESH= 5

# init camera
execution_path = os.getcwd()
camera = cv2.VideoCapture(0)

# hand stuff
handSolution = mp.solutions.hands
hands = handSolution.Hands()
mpDraw = mp.solutions.drawing_utils

def thumb_index_distance(hand):
    thumb_y = hand.landmark[THUMB].y
    index_y = hand.landmark[INDEX_FINGER].y
    distance = thumb_y * h - index_y * h
    return distance

def count_fingers(hand):
    finger_tips = [8, 12, 16, 20]  
    fingers_up = 0
    landmarks = hand.landmark
    
    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y: 
            fingers_up += 1

    return fingers_up
   
def detect_thumb(hand):
    landmarks = hand.landmark
    # check if thumb is on the left or right side of the index finger
    if landmarks[THUMB].x > landmarks[17].x:
        # print("Thumb is on the left side of the index finger")
        if landmarks[THUMB].x > landmarks[2].x:  
            return 1
    elif landmarks[THUMB].x < landmarks[17].x:
        # print("Thumb is on the right side of the index finger")
        if landmarks[THUMB].x < landmarks[2].x:  
            return 1
    return 0

frame = 0
thumb = 1000
fingers = ""
while True:
    frame +=1
    # Init and FPS process
    start_time = time.time()

    # Grab a single img of video
    ret, img = camera.read()
    # make mirror image
    img = cv2.flip(img, 1)  # Flip the img horizontally 

    # calculate FPS >> FPS = 1 / time to process loop
    fpsInfo = "FPS: " + str(1.0 / (time.time() - start_time)) 
    # print(fpsInfo)
    cv2.putText(img, fpsInfo, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    # Find the hands
    recHands = hands.process(img)
    if recHands.multi_hand_landmarks:
        for hand in recHands.multi_hand_landmarks:
            for datapoint_id, point in enumerate(hand.landmark):
                # Get the coordinates of the hand landmarks
                h, w, c = img.shape
                x, y = int(point.x * w), int(point.y * h)
                cv2.circle(img, (x, y), 5, (0, 255, 0), cv2.FILLED)
                # Optionally, draw lines between landmarks
                if datapoint_id > 0:
                    cv2.line(img, (prev_cx, prev_cy), (x, y), (255, 0, 0), 2)
                prev_cx, prev_cy = x, y
            
            mpDraw.draw_landmarks(img, hand, handSolution.HAND_CONNECTIONS)

        if frame % VOL_REFRESH == 0:
            # Calculate thumb and index finger distance
            thumb_index_dist = thumb_index_distance(hand)
            thumb = int(thumb_index_dist)

            # Count fingers
            fingers_up = count_fingers(hand)
            thumbs_up = detect_thumb(hand)
            fingers = f'Fingers Up: {fingers_up}, Thumbs Up: {thumbs_up}'

            frame = 0

            if thumb < 100:
                print("Playing sound")
            else:
                print("Not playing sound")

    cv2.putText(img, f'Thumb to Index Distance: {thumb}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)  
    cv2.putText(img, fingers, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
            
    # Display the resulting image
    cv2.imshow('Video', img)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
camera.release()
cv2.destroyAllWindows()