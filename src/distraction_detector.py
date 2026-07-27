import time


class DistractionDetector:

    def __init__(self):

        self.start_time = None
        self.threshold = 2.0  # seconds

    def update(self, horizontal, vertical):

        distracted = (
            horizontal != "FORWARD"
            or vertical != "CENTER"
        )

        if distracted:

            if self.start_time is None:
                self.start_time = time.time()

        else:
            self.start_time = None

        return self.is_distracted()

    def is_distracted(self):

        if self.start_time is None:
            return False

        return (time.time() - self.start_time) >= self.threshold

    def get_time(self):

        if self.start_time is None:
            return 0

        return round(time.time() - self.start_time, 1)