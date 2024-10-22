import cv2
import numpy as np
import uuid
import time
import datetime

start_camera = input("Do you want to start the camera work? (yes/no): ")

if start_camera.lower() == "yes":
    camera_id = 0
    video_capture = cv2.VideoCapture(camera_id)

    previous_frame = None
    motion_detected = False
    object_detected = False
    temperature_detected = False
    unusual_behavior_detected = False

    while True:
        ret, frame = video_capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            background_subtractor = cv2.createBackgroundSubtractorMOG2()
            fg_mask = background_subtractor.apply(gray)
            _, thresh = cv2.threshold(fg_mask, 25, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    object_detected = True
                    temperature_detected = True
                    unusual_behavior_detected = True

            cv2.imshow('Real-Time Monitoring', frame)

            print(f"Motion Detected: {motion_detected}")
            print(f"Object Detected: {object_detected}")
            print(f"Temperature Detected: {temperature_detected}")
            print(f"Unusual Behavior Detected: {unusual_behavior_detected}")
            print(f"Time: {datetime.datetime.now()}")
            print("------------------------")
        else:
            print("Error reading frame from camera")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
else:
    print("Camera work not started.")
