import cv2
import numpy as np

start_camera = input("Do you want to start the camera work? (yes/no): ")

if start_camera.lower() == "yes":
    camera_id = 0
    video_capture = cv2.VideoCapture(camera_id)

    # Initialize face cascade outside the loop
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = video_capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                temperature = 37.5  # Placeholder for temperature
                cv2.putText(frame, f"Temperature: {temperature}°C", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.imshow('Human Body Temperature Detection', frame)

        else:
            print("Error reading frame from camera")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
else:
    print("Camera work not started.")
