import cv2

# Key landmarks
NOSE = 1
LEFT_FACE = 234
RIGHT_FACE = 454
TOP_FACE = 10
BOTTOM_FACE = 152


def estimate_head_pose(face, frame):

    h, w, _ = frame.shape

    nose = face.landmark[NOSE]
    left = face.landmark[LEFT_FACE]
    right = face.landmark[RIGHT_FACE]
    top = face.landmark[TOP_FACE]
    bottom = face.landmark[BOTTOM_FACE]

    nose_x = nose.x * w
    nose_y = nose.y * h

    left_x = left.x * w
    right_x = right.x * w

    top_y = top.y * h
    bottom_y = bottom.y * h

    # Horizontal ratio
    horizontal_ratio = (nose_x - left_x) / (right_x - left_x)

    # Vertical ratio
    vertical_ratio = (nose_y - top_y) / (bottom_y - top_y)

    # Determine horizontal direction
    if horizontal_ratio < 0.42:
        horizontal = "LEFT"

    elif horizontal_ratio > 0.58:
        horizontal = "RIGHT"

    else:
        horizontal = "FORWARD"

    # Determine vertical direction
    if vertical_ratio < 0.38:
        vertical = "UP"

    elif vertical_ratio > 0.62:
        vertical = "DOWN"

    else:
        vertical = "CENTER"

    return horizontal, vertical
    