import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips =[8, 12, 16, 20]
thumb_tip= 4

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            landmark_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                landmark_list.append(lm)

            finger_fold =[]
            for tip in finger_tips:
                x,y = int(landmark_list[tip].x*w), int(landmark_list[tip].y*h)
                cv2.circle(img, (x,y), 15, (255, 0, 0), cv2.FILLED)

                if landmark_list[tip].x < landmark_list[tip - 3].x:
                    cv2.circle(img, (x,y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold.append(True)
                else:
                    finger_fold.append(False)
            print(finger_fold)

            if all(finger_fold):
                if landmark_list[thumb_tip].y < landmark_list[thumb_tip-1].y < landmark_list[thumb_tip-2].y:
                    print("Like !!! " + "\U0001F60A")
                    cv2.putText(img ,"Like", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

                if landmark_list[thumb_tip].y > landmark_list[thumb_tip-1].y > landmark_list[thumb_tip-2].y:
                    print("Dislike " + "\U0001F61E")
                    cv2.putText(img ,"Dislike", (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

            mp_draw.draw_landmarks(img, hand_landmark.mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2), mp_draw.DrawingSpec((0,255,0),4,2))
    
    cv2.imshow("hand tracking", img)
    cv2.waitKey(1)