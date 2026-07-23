import cv2

for i in range(3):
    cap = cv2.VideoCapture(i)
    print(f"Camera {i}: {'Opened' if cap.isOpened() else 'Not Found'}")
    cap.release()