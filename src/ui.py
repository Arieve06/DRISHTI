import cv2


def draw_ui(
    frame,
    left_ear,
    right_ear,
    average_ear,
    eye_status,
    eye_color,
    blink_detector,
    analytics,
    horizontal,
    vertical,
    mar,
    mouth,
    yawn_count,
    distraction_detector,
):
    """
    Draw all UI elements on the frame.
    """

    cv2.putText(frame, f"Left EAR : {left_ear:.2f}", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.putText(frame, f"Right EAR : {right_ear:.2f}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.putText(frame, f"Average EAR : {average_ear:.2f}", (20,95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.putText(frame, eye_status, (20,130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, eye_color, 2)

    cv2.putText(frame,
                f"Blinks : {blink_detector.blink_count}",
                (20,165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,0,0),
                2)

    cv2.putText(frame,
                f"Blink Rate : {analytics.blink_rate}/min",
                (20,200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2)

    cv2.putText(frame,
                f"Head : {horizontal}",
                (20,235),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"Vertical : {vertical}",
                (20,270),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"MAR : {mar:.2f}",
                (20,305),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.putText(frame,
                f"Mouth : {mouth}",
                (20,340),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"Yawns : {yawn_count}",
                (20,375),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.putText(frame,
                f"Look Away : {distraction_detector.get_time()} s",
                (20,410),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2)

    cv2.putText(frame,
                f"Session : {analytics.get_session_time()}",
                (20,445),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.putText(frame,
                f"FPS : {analytics.fps}",
                (20,480),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2)

    cv2.putText(frame,
                f"Attention : {analytics.attention_score}%",
                (20,515),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2)

    cv2.putText(frame,
                f"Status : {analytics.driver_status}",
                (20,550),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255,255,255),
                2)

def draw_warnings(
    frame,
    distracted,
    drowsy,
    yawning
):
    """
    Draw warning messages on the screen.
    """

    if distracted:
        cv2.putText(
            frame,
            "DISTRACTED DRIVER!",
            (650, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 165, 255),
            3
        )

    if yawning:
        cv2.putText(
            frame,
            "YAWNING DETECTED!",
            (650, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            3
        )

    if drowsy:
        cv2.putText(
            frame,
            "DROWSINESS DETECTED!",
            (650, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )