import cv2
import mediapipe as mp
import math

# ----------------------------
# Initialize MediaPipe Face Mesh
# ----------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# ----------------------------
# Open Webcam
# ----------------------------
camera = cv2.VideoCapture(0)

# ----------------------------
# Eye Landmark IDs
# ----------------------------
LEFT_EYE = [33, 133, 159, 145]
RIGHT_EYE = [362, 263, 386, 374]

# ----------------------------
# Detection Variables
# ----------------------------
blink_count = 0
closed_frames = 0

EAR_THRESHOLD = 0.22
BLINK_FRAME_THRESHOLD = 3
DROWSY_FRAME_THRESHOLD = 30

# ----------------------------
# Distance Function
# ----------------------------
def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )

# ----------------------------
# EAR Function
# ----------------------------
def calculate_ear(points, eye):
    horizontal = distance(points[eye[0]], points[eye[1]])
    vertical = distance(points[eye[2]], points[eye[3]])

    if horizontal == 0:
        return 0

    return vertical / horizontal

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

        h, w, _ = frame.shape

        points = {}

        # Draw landmarks for both eyes
        for idx in LEFT_EYE + RIGHT_EYE:

            landmark = face.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            points[idx] = (x, y)

            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        # Calculate EAR
        left_ear = calculate_ear(points, LEFT_EYE)
        right_ear = calculate_ear(points, RIGHT_EYE)

        average_ear = (left_ear + right_ear) / 2

        # ----------------------------
        # Blink & Drowsiness Detection
        # ----------------------------
        if average_ear < EAR_THRESHOLD:

            status = "EYE CLOSED"
            color = (0, 0, 255)

            closed_frames += 1

        else:

            status = "EYE OPEN"
            color = (0, 255, 0)

            if closed_frames >= BLINK_FRAME_THRESHOLD:
                blink_count += 1

            closed_frames = 0

        # Check Drowsiness
        drowsy = closed_frames >= DROWSY_FRAME_THRESHOLD

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
            f"Right EAR: {right_ear:.2f}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Average EAR: {average_ear:.2f}",
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
            f"Blinks: {blink_count}",
            (20, 165),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            f"Closed Frames: {closed_frames}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

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

    cv2.imshow("DRISHTI - Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()