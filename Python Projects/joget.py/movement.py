import cv2
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
    # Initialize camera
    camera_id = 0
    video_capture = cv2.VideoCapture(camera_id)

    while True:
        ret, frame = video_capture.read()
        if ret:
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply background subtraction
            background_subtractor = cv2.createBackgroundSubtractorMOG2()
            fg_mask = background_subtractor.apply(gray)

            # Threshold the foreground mask
            _, thresh = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)

            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Iterate through contours
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    # Draw bounding rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display output
            cv2.imshow('Movement Detection', frame)

        else:
            print("Error reading frame from camera")

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close window
    video_capture.release()
    cv2.destroyAllWindows()
else:
    print("Camera work not started.")