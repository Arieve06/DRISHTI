import csv
import os
from datetime import datetime


class SessionLogger:

    def __init__(self):

        self.file_path = "logs/session.csv"

        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(self.file_path):

            with open(self.file_path, "w", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Timestamp",
                    "Left EAR",
                    "Right EAR",
                    "Average EAR",
                    "Blink Count",
                    "Head",
                    "Vertical",
                    "Drowsy",
                    "Distracted"
                ])

    def log(
        self,
        left_ear,
        right_ear,
        average_ear,
        blink_count,
        head,
        vertical,
        drowsy,
        distracted
    ):

        with open(self.file_path, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%H:%M:%S"),
                round(left_ear, 3),
                round(right_ear, 3),
                round(average_ear, 3),
                blink_count,
                head,
                vertical,
                drowsy,
                distracted
            ])
        