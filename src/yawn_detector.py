class YawnDetector:
    def __init__(self, mar_threshold=0.06, min_frames=15):
        self.mar_threshold = mar_threshold
        self.min_frames = min_frames

        self.counter = 0
        self.yawn_count = 0
        self.is_yawning = False

    def update(self, mar):
        """
        Returns:
            yawning (bool)
            total_yawns (int)
        """

        if mar > self.mar_threshold:
            self.counter += 1

            if self.counter >= self.min_frames:
                self.is_yawning = True

        else:
            if self.is_yawning:
                self.yawn_count += 1

            self.counter = 0
            self.is_yawning = False

        return self.is_yawning, self.yawn_count