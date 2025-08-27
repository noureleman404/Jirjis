import cv2
import mediapipe as mp
import time

# Hand Detector class using MediaPipe
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        """
        Initializes the hand detector.
        mode: (bool) Whether to treat input images as a batch of images or a video stream.
        maxHands: Maximum number of hands to detect.
        detectionCon: (float) Minimum confidence for detection.
        trackCon: (float) Minimum confidence for tracking.
        """

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # Initialize MediaPipe Hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        # Drawing utility for landmarks
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Detects hands in the given image.
        img: input image (BGR format from OpenCV).
        draw: (bool) Whether to draw landmarks on the image.
        Returns: processed image with/without drawn hand landmarks.
        """

        # Convert image from BGR to RGB for MediaPipe processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # If hands are detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw landmarks and connections on the hand
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds the positions (x,y) of landmarks for a specific hand.
        img: input image
        handNo: index of the hand we track (default: first hand)
        draw: (bool) Whether to draw circles at landmark positions
        Returns: list of [id, x, y] for each landmark
        """

        lmList = []  # list of landmarks
        if self.results.multi_hand_landmarks:
            # Select the specific hand
            myHand = self.results.multi_hand_landmarks[handNo]

            # Loop through all landmarks in that hand
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # get image dimensions
                cx, cy = int(lm.x * w), int(lm.y * h)  # convert normalized coords to pixels
                lmList.append([id, cx, cy])  # add to list

                if draw:
                    # Draw a circle on each landmark
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    # For FPS calculation
    pTime = 0
    cTime = 0

    # Open webcam (0 = default cam, 1 = external cam)
    cap = cv2.VideoCapture(1)

    # Initialize hand detector
    detector = handDetector()

    while True:
        # Read frame from camera
        success, img = cap.read()

        # Detect hands and draw landmarks
        img = detector.findHands(img)

        # Get list of landmark positions
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4])

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display FPS on screen
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        # Show the processed image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # Press 'q' to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Run main function when file is executed directly
if __name__ == "__main__":
    main()
