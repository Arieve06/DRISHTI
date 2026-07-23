import cv2

# Try opening Camera 0 using macOS AVFoundation
camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# If Camera 0 fails, try Camera 1
if not camera.isOpened():
    print("Camera 0 failed. Trying Camera 1...")
    camera = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

# If both fail, exit
if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam started! Press 'q' to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Failed to capture frame.")
        break

    cv2.imshow("DRIVE-XAI Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()