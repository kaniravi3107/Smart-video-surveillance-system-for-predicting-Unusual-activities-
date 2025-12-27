import cv2
import numpy 
cap=cv2.VideoCapture(0)
bg_subtractor=cv2.createBackgroundSubtractorMOG2(history=500,varThreshold=16,detectShadows=True)
while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame_resized=cv2.resize(frame,(640,480))  
    frame_blur=cv2.GaussianBlur(frame_resized,(5,5),0)
    fg_mask=bg_subtractor.apply(frame_blur)
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    fg_mask=cv2.morphologyEx(fg_mask,cv2.MORPH_OPEN,kernel)
    normalized_frame=cv2.normalize(frame_blur,None,0,255,cv2.NORM_MINMAX)
    cv2.imshow("Original Frame",frame)
    cv2.imshow("Resized & Blurred Frame",frame_blur)
    cv2.imshow("Background subtraction",fg_mask)
    cv2.imshow("Normalized Frame",normalized_frame)
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()            


