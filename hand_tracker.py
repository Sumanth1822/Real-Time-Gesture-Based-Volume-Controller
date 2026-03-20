import cv2
import mediapipe as mp
import numpy as np
import math  # ADD THIS IMPORT

class HandTracker:
    def __init__(self, static_image_mode=False, max_num_hands=2, 
                 min_detection_confidence=0.7, min_tracking_confidence=0.7):
        
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Custom drawing specs
        self.landmark_drawing_spec = self.mp_draw.DrawingSpec(
            color=(0, 255, 0), thickness=2, circle_radius=3
        )
        self.connection_drawing_spec = self.mp_draw.DrawingSpec(
            color=(255, 0, 0), thickness=2, circle_radius=2
        )
    
    def find_hands(self, img, draw=True):
        """Find hands in the image and return landmarks"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_lms, self.mp_hands.HAND_CONNECTIONS,
                    self.landmark_drawing_spec, self.connection_drawing_spec
                )
        return img
    
    def find_position(self, img, hand_no=0, draw=True):
        """Get landmark positions for a specific hand"""
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            h, w, c = img.shape
            
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw and id in [4, 8, 12, 16, 20]:  # Fingertips
                    cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
        
        return lm_list
    
    def get_finger_distance(self, img, finger1=4, finger2=8, draw=True):
        """Calculate distance between two finger tips"""
        lm_list = self.find_position(img, draw=False)
        
        if len(lm_list) != 0 and finger1 < len(lm_list) and finger2 < len(lm_list):
            x1, y1 = lm_list[finger1][1], lm_list[finger1][2]
            x2, y2 = lm_list[finger2][1], lm_list[finger2][2]
            
            # Calculate distance using math.hypot
            length = math.hypot(x2 - x1, y2 - y1)
            
            if draw:
                # Draw line and circles
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), 2)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), 2)
                
                # Draw midpoint
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)
            
            return length, [x1, y1, x2, y2, cx, cy]
        
        return 0, []
    
    def get_hand_gesture(self, img):
        """Detect specific hand gestures"""
        lm_list = self.find_position(img, draw=False)
        
        if len(lm_list) == 0:
            return "No Hand"
        
        # Check for fist (all fingers closed)
        fingers = []
        
        # Thumb - check if thumb is to the left of thumb base (for right hand)
        if lm_list[4][1] < lm_list[3][1]:
            fingers.append(1)  # Thumb is open
        else:
            fingers.append(0)  # Thumb is closed
        
        # Other fingers - check if fingertip is above the middle joint
        for id in [8, 12, 16, 20]:
            if lm_list[id][2] < lm_list[id-2][2]:
                fingers.append(1)  # Finger is open
            else:
                fingers.append(0)  # Finger is closed
        
        # Gesture recognition
        if fingers == [0, 0, 0, 0, 0]:
            return "Fist"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Peace"
        elif fingers == [1, 1, 1, 1, 1]:
            return "Open Hand"
        elif fingers == [0, 1, 0, 0, 0]:
            return "Pointing"
        elif fingers == [1, 0, 0, 0, 0]:
            return "Thumbs Up"
        else:
            return f"Gesture {fingers}"