from config import BLINK_FRAME_THRESHOLD


class BlinkDetector:

    def __init__(self):

        self.blink_count = 0
        self.closed_frames = 0

    def update(self, ear, threshold):

        if ear < threshold:

            self.closed_frames += 1

            return False

        else:

            if self.closed_frames >= BLINK_FRAME_THRESHOLD:

                self.blink_count += 1

            self.closed_frames = 0

            return True