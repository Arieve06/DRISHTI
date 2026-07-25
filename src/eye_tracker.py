import cv2
from utils import calculate_ear
from config import LEFT_EYE, RIGHT_EYE


def get_eye_data(face, frame):

    h, w, _ = frame.shape

    points = {}

    for idx in LEFT_EYE + RIGHT_EYE:

        landmark = face.landmark[idx]

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        points[idx] = (x, y)

        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    left_ear = calculate_ear(points, LEFT_EYE)
    right_ear = calculate_ear(points, RIGHT_EYE)

    average_ear = (left_ear + right_ear) / 2

    return left_ear, right_ear, average_ear