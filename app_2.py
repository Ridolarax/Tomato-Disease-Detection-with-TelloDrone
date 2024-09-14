import tensorflow as tf
import streamlit as st
import numpy as np
import cv2
from djitellopy import Tello
from time import sleep
from tello_drone import Drone
from tensorflow.keras.models import load_model



def predict_disease(image_path):
    frame = cv2.imread(image_path)
    if frame is None:
        raise ValueError(f"failed to load image at {image_path}")
    
    # Resize the frame to the input size expected by the model
    frame_resized = cv2.resize(frame, (456, 456))
    frame_preprocessed = tf.keras.applications.efficientnet.preprocess_input(frame_resized)
    frame_expanded = np.expand_dims(frame_preprocessed, axis=0)

    # Make prediction
    model_path = "./best_model (1).h5"
    model = load_model(model_path)
    predictions = model.predict(frame_expanded)
    predicted_class = np.argmax(predictions, axis=1)
    return predicted_class


# Streamlit interface
st.title("Tomato Disease Detection With Tello Drone")
if "drone" not in st.session_state:
    st.session_state.drone = Drone()

drone = st.session_state.drone

if st.button("Check Battery Level"):
    if drone.getBattery() < 15:
        st.write(f"Drone Battery Level Low, Don't fly!")
    else:
        st.write(f"Drone Battery Level: {drone.getBattery()}")

# Button to take off
if st.button("Take Off"):
    # drone = Drone()
    drone.DroneTakeOff()
    st.write("Drone has taken off!")

if st.button("Start Streaming"):
    # Placeholder for the video stream
    frame_placeholder = st.empty()
    
    # Start streaming and display the frames in the Streamlit app
    for frame_image in drone.start_streaming():
        if frame_image:
            frame_placeholder.image(frame_image, channels="RGB")
        

if st.button("Capture Frame and Predict"):
    if hasattr(drone, "frame") and drone.frame is not None:
        screenshot_path = drone.takeShot()
        if screenshot_path:
            st.image(screenshot_path, caption= "Captured Image")
            predicted_class = predict_disease(screenshot_path)

        disease_names = {0: 'Bacterial_spot', 1: 'Early_blight', 2: 'Late_blight', 3: 'Leaf_Mold', 4: 'Septoria_leaf_spot', 5: 'Spider_mites Two-spotted_spider_mite', 6: 'Target_Spot', 7: 'Tomato_Yellow_Leaf_Curl_Virus', 8: 'Tomato_mosaic_virus', 9: 'healthy'}
        disease_names = [v for k, v in disease_names.items()]
        st.write(f"Predicted Disease: {disease_names[predicted_class[0]]}")
    else:
        st.write("No frame captured yet.")
    
    # frame = drone.takeShot()
    # predicted_class = predict_disease(frame)

    # # Display the frame
    # st.image(frame, channels="BGR")

    # Display the prediction
    # disease_names = {0: 'Bacterial_spot', 1: 'Early_blight', 2: 'Late_blight', 3: 'Leaf_Mold', 4: 'Septoria_leaf_spot', 5: 'Spider_mites Two-spotted_spider_mite', 6: 'Target_Spot', 7: 'Tomato_Yellow_Leaf_Curl_Virus', 8: 'Tomato_mosaic_virus', 9: 'healthy'}
    # disease_names = [v for k, v in disease_names.items()]
    # st.write(f"Predicted Disease: {disease_names[predicted_class[0]]}")

# Button to land the drone
if st.button("Land"):
    drone.DroneLand()
    st.write("Drone has landed!")
