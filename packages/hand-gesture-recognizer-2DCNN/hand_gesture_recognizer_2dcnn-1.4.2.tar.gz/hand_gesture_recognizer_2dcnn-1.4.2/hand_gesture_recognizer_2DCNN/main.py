import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands and Drawing utils
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


class GestureRecognizer:
    def __init__(self):
        self.custom_functions = {}
        self.previous_gestures = set()  # Track gestures from the previous frame
        self.previous_positions = (
            []
        )  # Track hand positions across frames for swipe detection

    def register_gesture(self, gesture_name, function):
        """
        Register a custom function for a specific gesture.
        :param gesture_name: Name of the gesture (e.g., 'fist', 'open_palm')
        :param function: Function to execute when this gesture is detected
        """
        self.custom_functions[gesture_name] = function

    def detect_gesture(self, hand_landmarks):
        """
        Detect the current gesture based on hand landmarks.
        :param hand_landmarks: Detected hand landmarks from MediaPipe
        :return: Gesture name (e.g., 'fist', 'open_palm') or None
        """
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
            (
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_PIP,
            ),
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

    def detect_swipe(self, hand_landmarks):
        """
        Detect left or right swipes based on the motion of the hand landmarks.
        :param hand_landmarks: Detected hand landmarks from MediaPipe
        :return: 'left_swipe', 'right_swipe', or None
        """
        # Use the wrist position for swipe detection
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        current_position = (wrist.x, wrist.y)

        if self.previous_positions:
            # Calculate motion direction
            prev_position = self.previous_positions[-1]
            dx = current_position[0] - prev_position[0]

            # Determine swipe direction
            if dx > 0.1:  # Adjust threshold for sensitivity
                return "right_swipe"
            elif dx < -0.1:
                return "left_swipe"

        # Store the current position for the next frame
        self.previous_positions.append(current_position)

        # Keep position history manageable
        if len(self.previous_positions) > 5:  # Adjust buffer size if needed
            self.previous_positions.pop(0)

        return None

    def handle_gesture_states(self, current_gestures):
        """
        Handle gesture state changes (appear, persist, disappear).
        :param current_gestures: Set of gestures detected in the current frame
        """
        # Detect newly appeared gestures
        new_gestures = current_gestures - self.previous_gestures

        # Detect disappeared gestures
        disappeared_gestures = self.previous_gestures - current_gestures

        # Handle new gestures
        for gesture in new_gestures:
            if gesture in self.custom_functions:
                self.custom_functions[gesture]("appear")

        # Handle disappeared gestures
        for gesture in disappeared_gestures:
            if gesture in self.custom_functions:
                self.custom_functions[gesture]("disappear")

        # Update previous gestures
        self.previous_gestures = current_gestures

    def run(self):
        cap = cv2.VideoCapture(0)
        with mp_hands.Hands(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as hands:
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
                current_gestures = set()  # Track gestures in the current frame

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Detect gesture
                        gesture = self.detect_gesture(hand_landmarks)

                        if gesture:
                            current_gestures.add(gesture)

                        # Detect swipes
                        swipe = self.detect_swipe(hand_landmarks)
                        if swipe:
                            current_gestures.add(swipe)

                        # Draw landmarks on the mask
                        mp_drawing.draw_landmarks(
                            hand_mask,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(
                                color=(255, 255, 255), thickness=2, circle_radius=2
                            ),
                            mp_drawing.DrawingSpec(
                                color=(255, 255, 255), thickness=2, circle_radius=2
                            ),
                        )

                # Handle gesture states
                self.handle_gesture_states(current_gestures)

                # Convert hand mask to grayscale
                gray_hand_mask = cv2.cvtColor(hand_mask, cv2.COLOR_BGR2GRAY)
                _, binary_hand_mask = cv2.threshold(
                    gray_hand_mask, 10, 255, cv2.THRESH_BINARY
                )

                # Combine the original image and the mask for display
                combined_view = np.hstack(
                    (image, cv2.cvtColor(binary_hand_mask, cv2.COLOR_GRAY2BGR))
                )
                cv2.imshow("Hand Gesture Recognition and Mask", combined_view)

                # Exit on pressing 'ESC'
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()
