from config import DROWSY_FRAME_THRESHOLD


class DrowsinessDetector:

    def is_drowsy(self, closed_frames):

        return closed_frames >= DROWSY_FRAME_THRESHOLD