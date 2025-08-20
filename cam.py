from ultralytics import YOLO
import cv2

# engine path
ENGINE_PATH = "best.engine"           # Your YOLOv8 TensorRT engine

# ----------------------
# LOAD MODEL
# ----------------------
model = YOLO(ENGINE_PATH)             # Load your TensorRT engine

# WEBCAM SETUP
# Use OpenCV to capture video from the default webcam (usually index 0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# ----------------------
# RUN REAL-TIME INFERENCE
# ----------------------
while True:
    # Read one frame from the webcam
    # 'ret' is a boolean that is True if the frame was read successfully
    ret, frame = cap.read()

    # If 'ret' is False, it means there was a problem reading the frame
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    # Run YOLO prediction on the current frame
    results = model.predict(source=frame, device=0, verbose=False)
    
    # Get the annotated frame with bounding boxes drawn on it
    annotated_frame = results[0].plot()
    
    # Display the annotated frame in a window called "YOLOv8 Webcam"
    cv2.imshow("YOLOv8 Webcam", annotated_frame)
    
    # Wait for 1 millisecond, and check if the 'q' key was pressed
    # If 'q' is pressed, break the loop and close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------
# CLEANUP
# ----------------------
# Release the webcam capture object
cap.release()
# Close all OpenCV windows
cv2.destroyAllWindows()

print("✅ Exiting program.")