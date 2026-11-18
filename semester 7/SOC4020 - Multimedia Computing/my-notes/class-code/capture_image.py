import os
import cv2

# Board todo: capture an image from the live camera
# Click the "Capture" button (or press 's') to save the current frame, 'q' to quit
save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "captures")
os.makedirs(save_dir, exist_ok=True)

# Button position on the window: top-left and bottom-right corners
BTN_TL = (10, 10)
BTN_BR = (130, 50)

# The mouse callback can't save directly, so it sets a flag the loop checks
clicked = False


def on_mouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        if BTN_TL[0] <= x <= BTN_BR[0] and BTN_TL[1] <= y <= BTN_BR[1]:
            clicked = True


def draw_button(img):
    cv2.rectangle(img, BTN_TL, BTN_BR, (50, 50, 200), -1)       # filled red box (BGR)
    cv2.rectangle(img, BTN_TL, BTN_BR, (255, 255, 255), 2)      # white border
    cv2.putText(img, "Capture", (BTN_TL[0] + 12, BTN_TL[1] + 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


# Open a connection to the webcam (0 is the default webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cv2.namedWindow("Webcam Video")
cv2.setMouseCallback("Webcam Video", on_mouse)

count = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Draw the button on a copy so saved photos don't include it
    display = frame.copy()
    draw_button(display)
    cv2.imshow("Webcam Video", display)

    key = cv2.waitKey(1) & 0xFF
    # Save the current frame if the button was clicked or 's' was pressed
    if clicked or key == ord("s"):
        clicked = False
        # Skip numbers already used so earlier photos aren't overwritten
        count += 1
        while os.path.exists(os.path.join(save_dir, f"capture_{count}.jpg")):
            count += 1
        path = os.path.join(save_dir, f"capture_{count}.jpg")
        cv2.imwrite(path, frame)
        print(f"Saved {path}  size={frame.shape[1]}x{frame.shape[0]}")
    # Break the loop if 'q' is pressed
    elif key == ord("q"):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
