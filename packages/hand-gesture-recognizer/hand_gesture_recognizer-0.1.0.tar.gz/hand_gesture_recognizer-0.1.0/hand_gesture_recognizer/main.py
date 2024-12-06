import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands and Drawing utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class GestureRecognizer:
    def __init__(self):
        self.custom_functions = {}

    def register_gesture(self, gesture_name, function):
        """
        Register a custom function for a specific gesture.
        :param gesture_name: Name of the gesture (e.g., 'fist', 'open_palm')
        :param function: Function to execute when this gesture is detected
        """
        self.custom_functions[gesture_name] = function

    def detect_gesture(self, hand_landmarks):
        fingers_extended = []

        # Thumb
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
        fingers_extended.append(thumb_tip.x < thumb_ip.x)

        # Other fingers
        for finger_tip, finger_pip in [
            (
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.INDEX_FINGER_PIP,
            ),
            (
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
            ),
            (mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP),
            (mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP),
        ]:
            tip = hand_landmarks.landmark[finger_tip]
            pip = hand_landmarks.landmark[finger_pip]
            fingers_extended.append(tip.y < pip.y)

        extended_count = sum(fingers_extended)

        if extended_count == 0:
            return "fist"
        elif extended_count == 5:
            return "open_palm"
        elif extended_count == 4:
            return "four_fingers"
        elif extended_count == 3:
            return "three_fingers"
        elif extended_count == 2:
            return "two_fingers"
        return None

    def run(self):
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                # Flip and process the image
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)

                # Convert back to BGR for display
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Initialize the hand mask
                hand_mask = np.zeros_like(image)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Detect gesture
                        gesture = self.detect_gesture(hand_landmarks)

                        # Call the corresponding custom function
                        if gesture and gesture in self.custom_functions:
                            self.custom_functions[gesture](image)

                        # Draw landmarks on the mask
                        mp_drawing.draw_landmarks(
                            hand_mask,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                            mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        )

                # Convert hand mask to grayscale
                gray_hand_mask = cv2.cvtColor(hand_mask, cv2.COLOR_BGR2GRAY)
                _, binary_hand_mask = cv2.threshold(gray_hand_mask, 10, 255, cv2.THRESH_BINARY)

                # Combine the original image and the mask for display
                combined_view = np.hstack((image, cv2.cvtColor(binary_hand_mask, cv2.COLOR_GRAY2BGR)))
                cv2.imshow("Hand Gesture Recognition and Mask", combined_view)

                # Exit on pressing 'ESC'
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()
