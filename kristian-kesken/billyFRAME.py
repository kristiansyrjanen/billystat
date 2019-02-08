import cv2

cap = cv2.VideoCapture('topview-snooker.mp4')
ret, current_frame = cap.read()
previous_frame = current_frame

while(cap.isOpened()):
    current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)  $

    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)

    cv2.imshow('frame diff ',frame_diff)      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    previous_frame = current_frame.copy()
    ret, current_frame = cap.read()

cap.release()
cv2.destroyAllWindows()
