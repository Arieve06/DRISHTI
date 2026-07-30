import csv
import os
import time
from datetime import datetime


class SessionLogger:

    def __init__(self):

        # Create logs folder if it doesn't exist
        os.makedirs("logs", exist_ok=True)

        # Log filename based on current date and time
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        self.filepath = os.path.join("logs", filename)

        # Last time data was logged
        self.last_log_time = time.time()

        # Create CSV file with header
        with open(self.filepath, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Session Time",
                "EAR",
                "MAR",
                "Blink Count",
                "Yawn Count",
                "Head Direction",
                "Attention Score",
                "Driver Status"
            ])

    def log(
        self,
        session_time,
        ear,
        mar,
        blink_count,
        yawn_count,
        head_direction,
        attention_score,
        driver_status
    ):

        current = time.time()

        # Log once every second
        if current - self.last_log_time < 1:
            return

        self.last_log_time = current

        with open(self.filepath, "a", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                session_time,
                round(ear, 3),
                round(mar, 3),
                blink_count,
                yawn_count,
                head_direction,
                attention_score,
                driver_status
            ])