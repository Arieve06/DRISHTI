import cv2
import mediapipe as mp
import pygame

from config import EAR_THRESHOLD
from eye_tracker import get_eye_data
from blink_detector import BlinkDetector
from drowsiness_detector import DrowsinessDetector

# ----------------------------
# Initialize Alarm
# ----------------------------
pygame.mixer.init()
pygame.mixer.music.load("assets/alarm.wav")

alarm_playing = False

# ----------------------------
# Initialize MediaPipe
# ----------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

camera = cv2.VideoCapture(0)

# ----------------------------
# Initialize Detectors
# ----------------------------
blink_detector = BlinkDetector()
drowsiness_detector = DrowsinessDetector()

# ----------------------------
# Main Loop
# ----------------------------
while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        face = results.multi_face_landmarks[0]

        left_ear, right_ear, average_ear = get_eye_data(face, frame)

        blink_detector.update(average_ear, EAR_THRESHOLD)

        drowsy = drowsiness_detector.is_drowsy(
            blink_detector.closed_frames
        )

        # ----------------------------
        # Eye Status
        # ----------------------------
        if average_ear < EAR_THRESHOLD:

            status = "EYE CLOSED"
            color = (0, 0, 255)

        else:

            status = "EYE OPEN"
            color = (0, 255, 0)

        # ----------------------------
        # Display Information
        # ----------------------------
        cv2.putText(
            frame,
            f"Left EAR : {left_ear:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Right EAR : {right_ear:.2f}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Average EAR : {average_ear:.2f}",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            status,
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Blinks : {blink_detector.blink_count}",
            (20, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Closed Frames : {blink_detector.closed_frames}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        # ----------------------------
        # Drowsiness + Alarm
        # ----------------------------
        if drowsy:

            cv2.putText(
                frame,
                "DROWSINESS DETECTED!",
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

            if not alarm_playing:

                pygame.mixer.music.play(-1)

                alarm_playing = True

        else:

            if alarm_playing:

                pygame.mixer.music.stop()

                alarm_playing = False

    cv2.imshow("DRISHTI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
pygame.mixer.music.stop()
cv2.destroyAllWindows()