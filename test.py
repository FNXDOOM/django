from ultralytics import YOLO
import cv2
import requests # NEW: Library for making HTTP requests
import time     # NEW: Library for adding a cooldown

# ----------------------
# CONFIGURATION
# ----------------------
ENGINE_PATH = "best.engine"           # Your YOLOv8 TensorRT engine
DJANGO_API_URL = "http://127.0.0.1:8000/api/alerts/create/" # Your Django API endpoint

# IMPORTANT: Check your dataset's .yaml file for these class IDs
PERSON_CLASS_ID = 5
HELMET_CLASS_ID = 2

# Cooldown to prevent spamming alerts for the same event
ALERT_COOLDOWN_SECONDS = 30
last_alert_time = 0

# ----------------------
# NEW: FUNCTION TO SEND ALERT
# ----------------------
def send_alert_to_django(frame, violation_type):
    """Encodes the frame and sends an alert to the Django API."""
    global last_alert_time

    current_time = time.time()
    if (current_time - last_alert_time) < ALERT_COOLDOWN_SECONDS:
        # print("Cooldown active. Skipping alert.")
        return

    # Encode the image frame as JPEG
    is_success, buffer = cv2.imencode(".jpg", frame)
    if not is_success:
        print("Error: Could not encode frame.")
        return

    # Prepare data for the POST request
    payload = {
        'violation_type': violation_type,
        'camera_id': 'CAM-01'
    }
    files = {
        'snapshot': ('snapshot.jpg', buffer.tobytes(), 'image/jpeg')
    }

    try:
        response = requests.post(DJANGO_API_URL, data=payload, files=files, timeout=10)
        if response.status_code == 201:
            print(f"🚀 Alert '{violation_type}' successfully sent to Django!")
            last_alert_time = current_time  # Update the time of the last successful alert
        else:
            print(f"Error sending alert: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Django server: {e}")

# ----------------------
# LOAD MODEL
# ----------------------
model = YOLO(ENGINE_PATH)

# WEBCAM SETUP
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# ----------------------
# RUN REAL-TIME INFERENCE
# ----------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    
    # Run YOLO prediction
    results = model.predict(source=frame, device=0, verbose=False)
    
    # --- MODIFIED: VIOLATION DETECTION LOGIC ---
    persons = []
    helmets = []
    
    # Extract bounding boxes and class IDs
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        if class_id == PERSON_CLASS_ID:
            persons.append(box.xyxy[0]) # Get coordinates
        elif class_id == HELMET_CLASS_ID:
            helmets.append(box.xyxy[0])

    # Check for violations
    for person_box in persons:
        has_helmet = False
        px1, py1, px2, py2 = person_box
        
        for helmet_box in helmets:
            hx1, hy1, hx2, hy2 = helmet_box
            # Simple check: is the helmet box mostly inside or on top of the person box?
            if (px1 < (hx1 + hx2) / 2 < px2) and (py1 < hy1):
                has_helmet = True
                break
        
        if not has_helmet:
            # VIOLATION DETECTED!
            print("🚨 No-Helmet Violation Detected!")
            send_alert_to_django(frame, 'NO_HELMET')
            # Optional: break after the first violation to avoid multiple alerts per frame
            break

    # Get the annotated frame for display
    annotated_frame = results[0].plot()
    
    # Display the frame
    cv2.imshow("YOLOv8 Webcam", annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------
# CLEANUP
# ----------------------
cap.release()
cv2.destroyAllWindows()
print("✅ Exiting program.")