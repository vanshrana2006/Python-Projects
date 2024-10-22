import cv2

# Load Haarcascade files for face and eye detection
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Check if the classifiers loaded successfully
if face_detector.empty():
    print("Error: Could not load face detector XML file.")
if eye_detector.empty():
    print("Error: Could not load eye detector XML file.")

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame is successfully captured
        if not ret:
            print("Error: Failed to capture image")
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_detector.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

            # Region of interest for eyes inside the detected face
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect eyes within the face region
            eyes = eye_detector.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)


        # Display the resulting frame
        cv2.imshow('Face and Eye Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
