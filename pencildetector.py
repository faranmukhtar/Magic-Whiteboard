import cv2 as cv
import numpy as np

def nothing(x): pass

def get_pen_tip(mask, min_area=300):
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = max(contours, key=cv.contourArea)
    if cv.contourArea(c) < min_area:
        return None
    tip = tuple(c[c[:, :, 1].argmin()][0])  # topmost point
    return tip

cv.namedWindow("Trackbars")
cv.createTrackbar("L-H", "Trackbars", 0, 179, nothing)
cv.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv.createTrackbar("U-H", "Trackbars", 179, 179, nothing)
cv.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    l_h = cv.getTrackbarPos("L-H", "Trackbars")
    l_s = cv.getTrackbarPos("L-S", "Trackbars")
    l_v = cv.getTrackbarPos("L-V", "Trackbars")
    u_h = cv.getTrackbarPos("U-H", "Trackbars")
    u_s = cv.getTrackbarPos("U-S", "Trackbars")
    u_v = cv.getTrackbarPos("U-V", "Trackbars")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv.inRange(hsv, lower, upper)

    # clean up noise so contours are stable
    kernel = np.ones((5, 5), np.uint8)
    mask_clean = cv.erode(mask, kernel, iterations=1)
    mask_clean = cv.dilate(mask_clean, kernel, iterations=2)

    pen_tip = get_pen_tip(mask_clean)
    if pen_tip is not None:
        px, py = pen_tip
        cv.circle(frame, (px, py), 10, (0, 255, 0), -1)

    cv.imshow("frame", frame)
    cv.imshow("mask", mask)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()