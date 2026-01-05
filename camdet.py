import cv2
import mediapipe as mp
import time

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils
mp_draw_styles=mp.solutions.drawing_styles

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    prev_time=0
    while cap.isOpened():
        success, frame=cap.read()
        if not success:
            print("failed")
            continue
        frame=cv2.flip(frame, 1)
        rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results=hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw_styles.get_default_hand_landmarks_style(),
                    mp_draw_styles.get_default_hand_connections_style()
                )
                hand_label=results.mutli_handedness[hand_idx].classification[0].label
                index_tip=hand_landmarks.landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                h,w,c=frame.shape
                index_x, index_y= int(index_tip.x * w), int(index_tip.y * h)
                thumb_x, thumb_y=int(thumb_tip.x * w), int(thumb_tip.y * h)

                cv2.putText(frame, f"{hand_label} Hand", (10, 30+hand_idx * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                cv2.putText(frame, f"INDEX: ({index_x}, {index_y})", (10, 60+hand_idx * 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0),1)
                curr_time=time.time()
                fps=1/(curr_time-prev_time)
                prev_time=curr_time
                cv2.putText(frame, f"FPS:{int(fps)}",(w-120, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
                cv2.imshow('handtracking', frame)
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    break
cap.release()
cv2.destroyAllWindows()
