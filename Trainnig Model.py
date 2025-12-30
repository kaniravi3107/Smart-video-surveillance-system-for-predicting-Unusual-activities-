#Import Libraries
import cv2
import numpy as np
import tensorflow 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Flatten
from tensorflow.keras.layers import LSTM,Dense,TimeDistributed

#Video Frame Extraction Functtion
def extract_frames(video_path,max_frames=30):
    cap=cv2.VideoCapture(video_path)
    frames=[]
    while len(frames) < max_frames:
        ret,frame=cap.read()
        if not ret:
            break
        frame=cv2.resize(frame,(64,64))
        frame=frame/255.0
        frames.append(frame)
    cap.release()
    while len(frames)<max_frames:
        frames.append(np.zeros((64,64,3)))
    return np.array(frames)

#CNN + LSTM Model
model=Sequential()
model.add(TimeDistributed(
    Conv2D(32,(3,3),activation='relu'),input_shape=(30,64,64,3)
)) 
model.add(TimeDistributed(Flatten()))
model.add(LSTM(64))
model.add(Dense(1,activation='sigmoid'))
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model.summary()  

#Implementing Dataset
X=[]
y=[]
#Normal
X.append(extract_frames("normal_activity,.m p4"))
y.append(0)
#Suspicious
X.append(extract_frames("suspicious_activity.mp4"))
y.append(1)
X=np.array(X)
y=np.array(y)

#Trainning model 
model.fit(X,y,epochs=10,batch_size=1)

#Activity Prediction
test_frames=extract_frames(r"C:\Users\HP\Downloads\archive.zip")
test_frames=np.expand_dims(test_frames,axis=0)
prediction=model.predict(test_frames)
if prediction[0][0] > 0.5:
    print(" Suspicious Activity Detected")
else:
    print("Normal Activity")    
    


