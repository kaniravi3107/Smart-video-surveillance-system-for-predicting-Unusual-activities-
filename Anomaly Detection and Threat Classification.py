import cv2
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D

# 1. DEFINE the extraction function correctly
def extract_frames(video_path, max_frames=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (64, 64))
        frame = frame / 255.0  # Normalization
        frames.append(frame)
    cap.release()
    
    # Padding if video is shorter than max_frames
    while len(frames) < max_frames:
        frames.append(np.zeros((64, 64, 3)))
    return np.array(frames)

# 2. DEFINE the Autoencoder architecture
def build_video_autoencoder(input_shape=(64, 64, 3)):
    input_img = Input(shape=input_shape)
    # Encoder: Learns normal behavior patterns
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    # Decoder: Reconstructs the input
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
    return Model(input_img, decoded)

# 3. INITIALIZE AND TRAIN
ae_model = build_video_autoencoder()
ae_model.compile(optimizer='adam', loss='mse')


normal_video_path = r"C:\Users\HP\Downloads\normal_activity.mp4" 
X_normal = extract_frames(normal_video_path)

print("Training autoencoder on normal patterns...")
ae_model.fit(X_normal, X_normal, epochs=20, batch_size=4, verbose=1)

# 4. THREAT CLASSIFICATION (Anomaly Detection)
def classify_threat(test_video_path):
    test_frames = extract_frames(test_video_path)
    reconstructed = ae_model.predict(test_frames)
    
    # Calculate Reconstruction Error (Model Confidence Score)
    errors = np.mean(np.square(test_frames - reconstructed), axis=(1, 2, 3))
    
    print("\n--- Threat Classification Report ---")
    for i, error in enumerate(errors):
        # Behavioral intensity thresholds
        if error < 0.01:
            risk = "Low Risk (Normal)"
        elif error < 0.03:
            risk = "Medium Risk (Suspicious)"
        else:
            risk = "High Risk (Threat)"
        print(f"Frame {i}: Error {error:.4f} | {risk}")

# Test with your suspicious data
classify_threat(r"C:\Users\HP\Downloads\suspicious_activity.mp4")