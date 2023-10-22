import cv2
import numpy as np
import os
import serial
import time

ENABLED = True
PATH = ""
start_word = "hellfire"
stop_word = "recall"

for string in os.listdir("/dev"):
    if "ttyUSB" in string:
        PATH = "/dev/" + string
        break
print(PATH)
print(PATH or "no path")


def detect_color_blobs(frame, target_color_rgb, tolerance=15):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Convert the target RGB color to HSV
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color_rgb]]), cv2.COLOR_RGB2HSV)[0][0]
    
    # Define the lower and upper bounds for the color detection
    lower_bound = np.array([target_color_hsv[0] - tolerance, max(target_color_hsv[1] - 40, 0), max(target_color_hsv[2] - 40, 0)])
    upper_bound = np.array([target_color_hsv[0] + tolerance, 255, 255])
    
    # Create a mask to isolate the desired color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Noise reduction and closing operation
    kernel = np.ones((10, 10), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=3)
    mask = cv2.erode(mask, kernel, iterations=2)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    largest_area = 0
    largest_center = None
    
    # Draw bounding boxes around the detected color blobs
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter by area
        area = cv2.contourArea(contour)
        if area < 1000:  # Adjust these values based on your requirements
            continue
        
        # Filter by aspect ratio (optional)
        aspect_ratio = float(w) / h
        if 0.5 < aspect_ratio < 2:  # Adjust these values based on your requirements
            cv2.rectangle(frame, (x, y), (x + w, y + h), color(), 2)
            
            # Find the center of the largest bounding box
            if area > largest_area:
                largest_area = area
                largest_center = (x + w // 2, y + h // 2)
    
    return frame, largest_center

# Capture video from the default camera
cam = 0
import sys
if (len(sys.argv) > 1):
    cam = int(sys.argv[1])
cap = cv2.VideoCapture(cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Get the screen center
_, initial_frame = cap.read()
screen_center_x = initial_frame.shape[1] // 2
screen_center_y = initial_frame.shape[0] // 2
print(initial_frame.shape)


last_printed = None

if PATH != "":
    time.sleep(0.1)
    ser = serial.Serial(PATH)
def write(a):
    global ENABLED
    if ENABLED: ser.write(a)

def color():
    global ENABLED
    return (0,255,0) if ENABLED else (0,0,255)

def toggle():
    print("TOGGLE")
    global ENABLED
    ENABLED ^= 1
    print(color(), ENABLED)

while True:
    try:
        word = open("/tmp/sync", "r").read()
        print(word)
        if "ire" in word:
            ENABLED = True
        if "call" in word:
            ENABLED = False
    except: pass

    # Read a frame from the camera
    ret, frame = cap.read()
    width  = cap.get(3)   # float `width`
    height = cap.get(4)  # float `height`
    shooting_threshold = 100

    # If the frame was successfully captured
    if ret:
        # Process the frame and detect color blobs
        processed_frame, largest_bbox_center = detect_color_blobs(frame, target_color_rgb=(169,49,43,255), tolerance=15)
        
        # Draw an "X" at the center of the screen
        cv2.line(processed_frame, (screen_center_x - 10, screen_center_y - 10), (screen_center_x + 10, screen_center_y + 10), (0, 0, 0), 2)
        cv2.line(processed_frame, (screen_center_x - 10, screen_center_y + 10), (screen_center_x + 10, screen_center_y - 10), (0, 0, 0), 2)
        cv2.circle(processed_frame, (screen_center_x, screen_center_y), 100, color())
        # Check the position of the largest bounding box center relative to the screen center
        if largest_bbox_center:
            screen_center_array = np.array((screen_center_x, screen_center_y))
            bbox_center_array = np.array((largest_bbox_center[0], largest_bbox_center[1]))
            if PATH != "" and np.linalg.norm(screen_center_array - bbox_center_array) > shooting_threshold * 0.5:
                    # Draw an "X" at the center of the detected bounding box center
                    try:

                        if PATH != "" and np.linalg.norm(screen_center_array - bbox_center_array) < shooting_threshold:
                                write(b"S")
                                time.sleep(0.01)
                        
                        cv2.line(processed_frame, (largest_bbox_center[0] - 10, largest_bbox_center[1] - 10), (largest_bbox_center[0] + 10, largest_bbox_center[1] + 10), (0, 0, 0), 2)
                        cv2.line(processed_frame, (largest_bbox_center[0] - 10, largest_bbox_center[1] + 10), (largest_bbox_center[0] + 10, largest_bbox_center[1] - 10), (0, 0, 0), 2)
                        if largest_bbox_center[0] < screen_center_x:
                            write(b"L")
                            time.sleep(0.01)
                        elif largest_bbox_center[0] >= screen_center_x:
                            write(b"R")
                            time.sleep(0.01)
                        
                        if largest_bbox_center[1] < screen_center_y:
                            write(b"U")
                            time.sleep(0.01)
                        elif largest_bbox_center[1] >= screen_center_y:
                            write(b"D")
                            time.sleep(0.01)

                        # Convert the points to NumPy arrays
                        screen_center_array = np.array((screen_center_x, screen_center_y))
                        bbox_center_array = np.array((largest_bbox_center[0], largest_bbox_center[1]))
                    
                    except serial.SerialException as e:
                        time.sleep(0.05)
                        ser = serial.Serial(PATH)

        # Display the result
        cv2.imshow('Detected Color', processed_frame)
        
        # Break the loop if 'q' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            toggle()
    else:
        print("Failed to grab frame")

cap.release()
cv2.destroyAllWindows()
