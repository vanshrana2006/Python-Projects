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

    # Initialize variables
    previous_frame = None
    motion_detected = False

    while True:
        ret, frame = video_capture.read()
        if ret:
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (21, 21), 0)

            # Calculate absolute difference between current and previous frames
            if previous_frame is not None:
                diff = cv2.absdiff(previous_frame, blurred)
                thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]

                # Count number of pixels that have changed
                count = np.count_nonzero(thresh)

                # Check if motion has been detected
                if count > 5000:
                    motion_detected = True
                else:
                    motion_detected = False

            # Update previous frame
            previous_frame = blurred

            # Display output
            if motion_detected:
                cv2.putText(frame, "Motion Detected", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imshow('Unusual Behavior Detection', frame)

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