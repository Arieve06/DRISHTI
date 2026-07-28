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
from ui import draw_ui, draw_warnings

# NEW
from mouth_tracker import calculate_mar, mouth_status
from yawn_detector import YawnDetector


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

# NEW
yawn_detector = YawnDetector()

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
        # Mouth Tracking
        # ----------------------------
        mar = calculate_mar(face, frame)

        mouth = mouth_status(mar)

        yawning, yawn_count = yawn_detector.update(mar)

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
        # Analytics
        # ----------------------------
        analytics.update_attention(
            drowsy,
            distracted,
            average_ear,
            yawning
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
        # Display
        # ----------------------------
       
           

        draw_ui(
    frame,
    left_ear,
    right_ear,
    average_ear,
    status,
    color,
    blink_detector,
    analytics,
    horizontal,
    vertical,
    mar,
    mouth,
    yawn_count,
    distraction_detector
)

        # ----------------------------
        # Warning Messages
        # ----------------------------
        draw_warnings(
    frame,
    distracted,
    drowsy,
    yawning
)

        # ----------------------------
        # Alarm Logic
        # ----------------------------
        if drowsy or distracted:

            if drowsy:
                cv2.putText(
                    frame,
                    "DROWSINESS DETECTED!",
                    (650,120),
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