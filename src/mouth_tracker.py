import cv2
from utils import distance

# ----------------------------
# Mouth Landmarks (MediaPipe)
# ----------------------------

UPPER_LIP = 13
LOWER_LIP = 14

LEFT_MOUTH = 61
RIGHT_MOUTH = 291


def calculate_mar(face, frame):

    h, w, _ = frame.shape

    landmarks = []

    for landmark in face.landmark:
        landmarks.append((
            int(landmark.x * w),
            int(landmark.y * h)
        ))

    upper = landmarks[UPPER_LIP]
    lower = landmarks[LOWER_LIP]

    left = landmarks[LEFT_MOUTH]
    right = landmarks[RIGHT_MOUTH]

    vertical = distance(upper, lower)
    horizontal = distance(left, right)

    if horizontal == 0:
        return 0

    mar = vertical / horizontal

    # Draw landmarks
    cv2.circle(frame, upper, 3, (0, 255, 255), -1)
    cv2.circle(frame, lower, 3, (0, 255, 255), -1)
    cv2.circle(frame, left, 3, (255, 0, 255), -1)
    cv2.circle(frame, right, 3, (255, 0, 255), -1)

    return mar


def mouth_status(mar, threshold=0.06):

    if mar > threshold:
        return "OPEN"

    return "CLOSED"