import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

mpHand = mp.solutions.hands
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils

calculated_distances = [[5, 4], [6,8], [10,12], [14,16], [18,20]]

while cap.isOpened():
    success, img = cap.read()
    
    if success:
        img = cv2.flip(img, 1)
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        results = hands.process(img_rgb)
        
        counter = 0
        if results.multi_hand_landmarks:
        
            motions = []
            
            for handLms in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
                
                for id, lm in enumerate(handLms.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    
                    if id == 4:
                        cy = ((cy + motions[3][2]) / 2) + cap.get(4) / 30
                        
                    motions.append([id,cx, cy])
        
            
            for item in calculated_distances:
                downFingerPosY  = motions[item[0]][2]
                upperFingerPosY = motions[item[1]][2]

                isFingerOpen = downFingerPosY > upperFingerPosY
                counter += 1 if isFingerOpen else 0
                
                                   
        cv2.rectangle(img, (0,0), (200, 50), (0,0,0), cv2.FILLED)
        cv2.putText(img,str(counter), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.imshow("Capture", img)
        cv2.waitKey(1)