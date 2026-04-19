import cv2

cap = None
for i in range(4):
    print(f"Testing index {i}...")
    cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    ret, frame = cap.read()
    if ret:
        print(f"SUCCESS! Video stream found on index {i}")
        break
    cap.release()

if not cap or not cap.isOpened() or not ret:
    print("Failed to pull frames from any index.")
    exit()

print("Stream active! Press 'q' to quit.")
while True:
    ret, frame = cap.read()
    if not ret: break
    cv2.imshow('Raw Camera Test', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
