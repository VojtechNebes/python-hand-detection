print("importing cv2")
import cv2
print("importing mediapipe")
import mediapipe as mp
print("importing pygame")
import pygame
print("importing everything else")
import time


pygame.init()

mpHands = mp.solutions.hands
webcam = cv2.VideoCapture(0)

screen = pygame.display.set_mode((1000, 1000))

hands = mpHands.Hands(max_num_hands=2)

run = True
while webcam.isOpened() and run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            run = False

    success, img = webcam.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    screen.fill((0, 0, 0))
    
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            points = [handLandmarks.landmark.pop(0) for _ in range(len(handLandmarks.landmark))]
            
            for connection in list(mpHands.HAND_CONNECTIONS):
                startPos = points[connection[0]]
                endPos = points[connection[1]]

                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    ((1-startPos.x)*1000, startPos.y*1000),
                    ((1-endPos.x)*1000, endPos.y*1000),
                    2
                )
            
            for i in range(len(points)):
                pygame.draw.circle(screen, (255, 0, i/len(points) * 255), ((1-points[i].x)*1000, points[i].y*1000), 5)

    pygame.display.update()

pygame.quit()
webcam.release()