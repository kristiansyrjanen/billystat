import cv2
import numpy as np


cap = cv2.VideoCapture("/home/kristian/krisunvideot/00002.MTS")
empty_table = cv2.imread("/home/kristian/Desktop/empty-table.png")
 
old_frame = empty-table

while True:

    ret, frame = cap.read()

    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if old_frame is not None:
            diff_frame = gray - old_frame
            diff_frame -= diff_frame.min()
            disp_frame = np.uint8(255.0*diff_frame/float(diff_frame.max()))
            cv2.imshow('diff_frame',disp_frame)
        old_frame = gray

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        print('ERROR!')
        break

cap.release()
cv2.destroyAllWindows()
