import cv2
from ultralytics import YOLO
import datetime
import time
import os

# --- INITIALIZATION ---
# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Fix: Use CAP_DSHOW for Windows stability and index 0 for the default camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Ensure the 'templates' directory exists for saving alerts
if not os.path.exists('templates'):
    os.makedirs('templates')

last_alert_time = 0  # Cooldown tracker (in seconds)
alert_cooldown = 5   # Time to wait between saving photos

print("System Started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not access the camera.")
        break

    # Run detection
    results = model(frame, stream=True,conf=0.25)
    
    for r in results:
        #This will print all detectedobjects 
        if len(r.boxes) > 0:
            print(f"Detected {len(r.boxes)} objects")
        boxes = r.boxes
        for box in boxes:
            # 1. Rectify coordinates: convert Tensors to standard Python integers
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            
            # 2. Rectify data types: convert Tensors to float/int
            confidence = float(box.conf[0])
            cls_idx = int(box.cls[0])
            label = model.names[cls_idx]

            # Default color is green
            color = (0, 255, 0)

            # --- ALERT LOGIC ---
            if label == "person" and confidence > 0.5:
                # Change box color to red for visual alert
                color = (0, 0, 255)
                
                # Check if 5 seconds have passed since the last alert
                current_time = time.time()
                if current_time - last_alert_time > alert_cooldown:
                    last_alert_time = current_time
                    
                    # Create unique filename with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_path = f"templates/ALERT_CAM_{timestamp}.jpg"
                    
                    # Save the frame
                    cv2.imwrite(file_path, frame)
                    print(f"!!! ALERT: Human Detected. Photo saved: {file_path} !!!")

            # 3. Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Display the resulting frame
    cv2.imshow("Security Monitoring System", frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
cap.release()
cv2.destroyAllWindows()