import face_recognition
import cv2
import numpy as np

# Load sample images and learn how to recognize them
image_of_person_1 = face_recognition.load_image_file("Shivam.jpg")
image_of_person_2 = face_recognition.load_image_file("Vansh.jpg")

# Encode the loaded face images
person_1_encoding = face_recognition.face_encodings(image_of_person_1)[0]
person_2_encoding = face_recognition.face_encodings(image_of_person_2)[0]

# Create arrays of known face encodings and names
known_face_encodings = [person_1_encoding, person_2_encoding]
known_face_names = ["Person 1", "Person 2"]

# Open a handle to the webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture a single frame from the webcam
    ret, frame = video_capture.read()

    # Resize the frame to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR (OpenCV format) to RGB (face_recognition format)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Initialize a list for names of recognized faces
    face_names = []

    for face_encoding in face_encodings:
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # Use the closest match if there are multiple matches
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale the face locations back to the original frame size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Display the video feed with the recognized faces
    cv2.imshow('Live Face Recognition', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam handle and close windows
video_capture.release()
cv2.destroyAllWindows()
