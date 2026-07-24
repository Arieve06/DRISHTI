import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# Open webcam
camera = cv2.VideoCapture(1)

# Left eye landmark IDs
LEFT_EYE = [33, 133, 159, 145]


# Function to calculate Euclidean distance
def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )


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

        # Get eye landmark coordinates
        for idx in LEFT_EYE:

            landmark = face.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            points[idx] = (x, y)

            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        # Calculate distances
        horizontal = distance(points[33], points[133])
        vertical = distance(points[159], points[145])

        # Calculate Eye Aspect Ratio
        ear = vertical / horizontal

        # Threshold for eye state
        THRESHOLD = 0.22

        if ear < THRESHOLD:
            status = "EYE CLOSED"
            color = (0, 0, 255)   # Red
        else:
            status = "EYE OPEN"
            color = (0, 255, 0)   # Green

        # Display EAR
        cv2.putText(
            frame,
            f"EAR: {ear:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # Display eye status
        cv2.putText(
            frame,
            status,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )

    cv2.imshow("DRISHTI - Eye State Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()