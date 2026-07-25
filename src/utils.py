import math


def distance(p1, p2):
    return math.sqrt(
        (p2[0] - p1[0]) ** 2 +
        (p2[1] - p1[1]) ** 2
    )


def calculate_ear(points, eye):

    horizontal = distance(
        points[eye[0]],
        points[eye[1]]
    )

    vertical = distance(
        points[eye[2]],
        points[eye[3]]
    )

    if horizontal == 0:
        return 0

    return vertical / horizontal