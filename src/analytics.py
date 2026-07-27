import time


class DriverAnalytics:

    def __init__(self):

        self.session_start = time.time()

        self.last_fps_time = time.time()
        self.frame_count = 0
        self.fps = 0

        self.last_blink_count = 0
        self.last_blink_time = time.time()
        self.blink_rate = 0

        self.attention_score = 100
        self.driver_status = "ALERT"

    # -----------------------------
    # Session Time
    # -----------------------------
    def get_session_time(self):

        elapsed = int(time.time() - self.session_start)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # -----------------------------
    # FPS
    # -----------------------------
    def update_fps(self):

        self.frame_count += 1

        current = time.time()

        if current - self.last_fps_time >= 1:

            self.fps = self.frame_count

            self.frame_count = 0

            self.last_fps_time = current

    # -----------------------------
    # Blink Rate
    # -----------------------------
    def update_blink_rate(self, blink_count):

        current = time.time()

        elapsed = current - self.last_blink_time

        if elapsed >= 60:

            self.blink_rate = blink_count - self.last_blink_count

            self.last_blink_count = blink_count
            self.last_blink_time = current

    # -----------------------------
    # Attention Score
    # -----------------------------
    def update_attention(
        self,
        drowsy,
        distracted,
        average_ear
    ):

        score = 100

        if distracted:
            score -= 25

        if drowsy:
            score -= 35

        if average_ear < 0.20:
            score -= 20

        if score < 0:
            score = 0

        self.attention_score = score

        if score >= 90:
            self.driver_status = "ALERT"

        elif score >= 70:
            self.driver_status = "FOCUSED"

        elif score >= 50:
            self.driver_status = "TIRED"

        elif score >= 30:
            self.driver_status = "DROWSY"

        else:
            self.driver_status = "CRITICAL"
            