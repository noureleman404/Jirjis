import cv2
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CAMERA_INDEX = 0
BAR_POSITION = (50, 40)  # x, y start point
BAR_WIDTH = 50
BAR_HEIGHT = 290
BAR_COLOR = (250, 0, 0)   # Light gray
BAR_FILL_COLOR = (255, 0, 0)  # Green

MIN_DISTANCE = 50    # min distance between fingers
MAX_DISTANCE = 280   # max distance between fingers


cap = cv2.VideoCapture(CAMERA_INDEX)
detector = htm.handDetector(detectionCon=0.7 )

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get system volume range in dB
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img , draw= False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Thumb and index tip
        x1, y1 = lmList[4][1], lmList[4][2]   
        x2, y2 = lmList[8][1], lmList[8][2]   

        # Distance between fingers
        distance = np.hypot(x2 - x1, y2 - y1)

        # Map distance to system volume (in dB)
        vol_db = np.interp(distance, [MIN_DISTANCE, MAX_DISTANCE], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol_db, None)

        # Map distance to percentage (0–100%)
        vol_percent = np.interp(distance, [MIN_DISTANCE, MAX_DISTANCE], [0, 100])

        # Map distance to bar fill
        bar_fill = np.interp(distance, [MIN_DISTANCE, MAX_DISTANCE],
                             [BAR_POSITION[1] + BAR_HEIGHT, BAR_POSITION[1]])

        overlay = img.copy()

        # Filled rectangle (blue, transparent)
        cv2.rectangle(overlay,
                      (BAR_POSITION[0], int(bar_fill)),
                      (BAR_POSITION[0] + BAR_WIDTH, BAR_POSITION[1] + BAR_HEIGHT),
                      BAR_FILL_COLOR, cv2.FILLED)

        # Blend overlay with original image
        alpha = 0.4 
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        # Draw bar outline (always solid gray)
        cv2.rectangle(img, BAR_POSITION,
                      (BAR_POSITION[0] + BAR_WIDTH, BAR_POSITION[1] + BAR_HEIGHT),
                      BAR_COLOR, 3)

        # Volume percentage text
        cv2.putText(img, f'{int(vol_percent)} %',
                    (BAR_POSITION[0] - 10, BAR_POSITION[1] + BAR_HEIGHT + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)

    cv2.imshow("Hand Tracking Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
