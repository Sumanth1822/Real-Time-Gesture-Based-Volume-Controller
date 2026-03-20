import cv2
import numpy as np
import time
from hand_tracker import HandTracker
from volume_controller import VolumeController

class GestureVolumeController:
    def __init__(self):
        self.hand_tracker = HandTracker()
        self.volume_controller = VolumeController()
        
        # Volume control parameters
        self.min_distance = 30
        self.max_distance = 250
        self.volume_bar = 400
        self.volume_percentage = 0
        self.volume_color = (0, 255, 0)
        
        # Gesture control
        self.last_gesture_time = 0
        self.gesture_cooldown = 1  # seconds
        
        # Calibration mode
        self.calibration_mode = False
        self.calibration_samples = []
        
        # FPS calculation
        self.previous_time = 0
        self.current_time = 0
        
    def draw_volume_bar(self, img, volume_percentage):
        """Draw volume bar on the screen"""
        h, w, c = img.shape
        
        # Volume bar background
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)
        
        # Volume level
        vol_height = int((volume_percentage / 100) * 250)
        cv2.rectangle(img, (50, 400 - vol_height), (85, 400), self.volume_color, cv2.FILLED)
        
        # Volume percentage text
        cv2.putText(img, f'{int(volume_percentage)}%', (40, 450), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return img
    
    def draw_controls_info(self, img):
        """Draw control instructions on screen"""
        controls = [
            "CONTROLS:",
            "Pinch: Volume Control",
            "Fist: Mute/Unmute",
            "Peace: Calibration Mode",
            "ESC: Exit"
        ]
        
        y_offset = 50
        for control in controls:
            cv2.putText(img, control, (10, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y_offset += 30
        
        return img
    
    def calibrate_volume_range(self, distance):
        """Auto-calibrate volume range based on user's hand size"""
        if len(self.calibration_samples) < 30:  # Collect 30 samples
            self.calibration_samples.append(distance)
            return False
        else:
            # Set min and max based on collected samples
            self.min_distance = min(self.calibration_samples) * 0.8
            self.max_distance = max(self.calibration_samples) * 1.2
            self.calibration_samples = []
            return True
    
    def calculate_fps(self):
        """Calculate and return FPS"""
        self.current_time = time.time()
        fps = 1 / (self.current_time - self.previous_time) if (self.current_time - self.previous_time) > 0 else 0
        self.previous_time = self.current_time
        return fps
    
    def run(self):
        """Main function to run the gesture volume controller"""
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)  # Width
        cap.set(4, 720)   # Height
        
        print("Gesture Volume Controller Started!")
        print("Controls:")
        print("- Pinch thumb and index finger to control volume")
        print("- Make a fist to mute/unmute")
        print("- Show peace sign (V) for 2 seconds to calibrate")
        print("- Press ESC to exit")
        
        # Initialize timing for FPS
        self.previous_time = time.time()
        
        calibration_start_time = 0
        current_gesture = "No Hand"
        
        while True:
            success, img = cap.read()
            if not success:
                print("Failed to read from camera")
                break
            
            # Flip image horizontally for mirror effect
            img = cv2.flip(img, 1)
            
            # Find hands
            img = self.hand_tracker.find_hands(img)
            
            # Get gesture
            gesture = self.hand_tracker.get_hand_gesture(img)
            
            # Handle gestures
            current_time = time.time()
            
            if gesture == "Peace" and current_gesture != "Peace":
                calibration_start_time = current_time
            elif gesture == "Peace" and current_gesture == "Peace":
                if current_time - calibration_start_time > 2:  # Hold for 2 seconds
                    self.calibration_mode = not self.calibration_mode
                    calibration_start_time = current_time
                    print(f"Calibration mode: {self.calibration_mode}")
            
            elif gesture == "Fist" and current_gesture != "Fist":
                if current_time - self.last_gesture_time > self.gesture_cooldown:
                    is_muted = self.volume_controller.mute_volume()
                    mute_status = "MUTED" if is_muted else "UNMUTED"
                    cv2.putText(img, mute_status, (300, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    self.last_gesture_time = current_time
            
            current_gesture = gesture
            
            # Volume control with pinch gesture
            length, points = self.hand_tracker.get_finger_distance(img, 4, 8)
            
            if length > 0:
                # Auto-calibration
                if self.calibration_mode:
                    calibrated = self.calibrate_volume_range(length)
                    if calibrated:
                        self.calibration_mode = False
                        cv2.putText(img, "CALIBRATION COMPLETE!", (300, 150), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                else:
                    # Convert distance to volume percentage
                    vol_percentage = np.interp(length, [self.min_distance, self.max_distance], [0, 100])
                    vol_percentage = max(0, min(100, vol_percentage))  # Clamp between 0-100
                    
                    # Set volume
                    smooth_vol = self.volume_controller.set_volume(vol_percentage)
                    self.volume_percentage = smooth_vol
                    
                    # Change color based on volume level
                    if smooth_vol > 80:
                        self.volume_color = (0, 0, 255)  # Red for high volume
                    elif smooth_vol > 50:
                        self.volume_color = (0, 255, 255)  # Yellow for medium
                    else:
                        self.volume_color = (0, 255, 0)  # Green for low
                    
                    # Draw volume info
                    if len(points) >= 6:  # Ensure we have all points
                        cv2.putText(img, f'Distance: {int(length)}', (points[4] - 50, points[5] - 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Draw UI elements
            img = self.draw_volume_bar(img, self.volume_percentage)
            img = self.draw_controls_info(img)
            
            # Show calibration status
            if self.calibration_mode:
                cv2.putText(img, "CALIBRATION MODE - Move hand freely", (300, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                progress = len(self.calibration_samples) / 30
                cv2.rectangle(img, (300, 120), (300 + int(200 * progress), 140), (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (300, 120), (500, 140), (255, 255, 255), 2)
            
            # Show current gesture
            cv2.putText(img, f'Gesture: {gesture}', (10, 450), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Calculate and display FPS
            fps = self.calculate_fps()
            cv2.putText(img, f'FPS: {int(fps)}', (10, 480), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show the image
            cv2.imshow("Gesture Volume Controller", img)
            
            # Exit on ESC key
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        print("Gesture Volume Controller stopped.")

# Run the application
if __name__ == "__main__":
    controller = GestureVolumeController()
    controller.run()