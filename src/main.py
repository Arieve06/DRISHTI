import cv2
import mediapipe as mp
import pygame

from config import EAR_THRESHOLD
from eye_tracker import get_eye_data
from blink_detector import BlinkDetector
from drowsiness_detector import DrowsinessDetector
from head_pose import estimate_head_pose
from distraction_detector import DistractionDetector
from analytics import DriverAnalytics

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
distraction_detector = DistractionDetector()
analytics = DriverAnalytics()

# ----------------------------
# Main Loop
# ----------------------------
while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    analytics.update_fps()

    if results.multi_face_landmarks:

        face = results.multi_face_landmarks[0]

        # ----------------------------
        # Eye Tracking
        # ----------------------------
        left_ear, right_ear, average_ear = get_eye_data(face, frame)

        # ----------------------------
        # Head Pose
        # ----------------------------
        horizontal, vertical = estimate_head_pose(face, frame)

        # ----------------------------
        # Blink Detection
        # ----------------------------
        blink_detector.update(
            average_ear,
            EAR_THRESHOLD
        )

        analytics.update_blink_rate(
            blink_detector.blink_count
        )

        # ----------------------------
        # Drowsiness Detection
        # ----------------------------
        drowsy = drowsiness_detector.is_drowsy(
            blink_detector.closed_frames
        )

        # ----------------------------
        # Distraction Detection
        # ----------------------------
        distracted = distraction_detector.update(
            horizontal,
            vertical
        )

        # ----------------------------
        # Driver Analytics
        # ----------------------------
        analytics.update_attention(
            drowsy,
            distracted,
            average_ear
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
        y = 35

        def put(text, colour=(255, 255, 255)):
            global y

        cv2.putText(
            frame,
            f"Left EAR : {left_ear:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Right EAR : {right_ear:.2f}",
            (20,65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Average EAR : {average_ear:.2f}",
            (20,95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            status,
            (20,130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Blinks : {blink_detector.blink_count}",
            (20,165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

        cv2.putText(
            frame,
            f"Blink Rate : {analytics.blink_rate}/min",
            (20,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Head : {horizontal}",
            (20,235),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Vertical : {vertical}",
            (20,270),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Look Away : {distraction_detector.get_time()} s",
            (20,305),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Session : {analytics.get_session_time()}",
            (20,340),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"FPS : {analytics.fps}",
            (20,375),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Attention : {analytics.attention_score}%",
            (20,410),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Status : {analytics.driver_status}",
            (20,445),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255,255,255),
            2
        )

        if distracted:
            cv2.putText(
                frame,
                "DISTRACTED DRIVER!",
                (20,480),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,165,255),
                3
            )

        # ----------------------------
        # Alarm Logic
        # ----------------------------
        if drowsy or distracted:

            if drowsy:
                cv2.putText(
                    frame,
                    "DROWSINESS DETECTED!",
                    (20,520),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
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