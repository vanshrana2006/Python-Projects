import cv2
import requests
import base64
import numpy as np
import uuid

# Function to generate a unique API URL for each request
def generate_api_url():
    return f"http://your-joget-instance/api/upload/{uuid.uuid4()}"

# Generate API URL
api_url = generate_api_url()
print(f"Generated API URL: {api_url}")
print("Please copy and link this URL to Joget in the Joget app.")

# Prompt user to start camera work
start_camera = input("Do you want to start the camera work? (yes/no): ")

if start_camera.lower() == "yes":
    # Define camera IDs (e.g., 0, 1, 2, etc.)
    camera_ids = [0, 1, 2]

    # Create a dictionary to store video capture objects
    video_captures = {}

    # Initialize video capture objects
    for camera_id in camera_ids:
        video_captures[camera_id] = cv2.VideoCapture(camera_id)

    # Function to send frame to Joget
    def send_frame_to_joget(frame, camera_id):
        # Encode frame as JPEG
        _, encoded_image = cv2.imencode('.jpg', frame)
        # Convert to base64 string
        base64_image = base64.b64encode(encoded_image).decode('utf-8')

        # Prepare the payload for Joget (adjust data structure as needed)
        payload = {
            'camera_id': camera_id,
            'image': base64_image
        }

        # Save the payload to a file for later use
        with open("payload.json", "w") as f:
            import json
            json.dump(payload, f)
        print("Payload saved to payload.json")

    # Read frames from each camera and process them
    while True:
        for camera_id, video_capture in video_captures.items():
            ret, frame = video_capture.read()
            if ret:
                # Example processing: convert frame to grayscale
                processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Send the processed frame to Joget for further analysis
                send_frame_to_joget(processed_frame, camera_id)

                # Display the frame locally for debugging
                cv2.imshow(f"Camera {camera_id}", processed_frame)

            else:
                print(f"Error reading frame from camera {camera_id}")

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video captures and close windows
    for video_capture in video_captures.values():
        video_capture.release()
    cv2.destroyAllWindows()
else:
    print("Camera work not started.")