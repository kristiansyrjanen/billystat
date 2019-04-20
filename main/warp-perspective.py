import cv2
import numpy as np

#cap = cv2.VideoCapture(0)

while True:
    #_, frame = cap.read()
    frame = cv2.imread('emptytable.png')

    cv2.circle(frame, (550, 218), 5, (0, 0, 255), -1)
    cv2.circle(frame, (1059, 213), 5, (0, 0, 255), -1)
    cv2.circle(frame, (0, 690), 5, (0, 0, 255), -1)
    cv2.circle(frame, (1620, 672), 5, (0, 0, 255), -1)

    pts1 = np.float32([[537, 218], [1069, 213], [0, 702], [1620, 672]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    result = cv2.warpPerspective(frame, matrix, (500, 600))


    cv2.imshow("Frame", frame)
    cv2.imshow("Perspective transformation", result)

    key = cv2.waitKey(1)
    if key == 27: # Esc
        break

cap.release()
cv2.destroyAllWindows()
