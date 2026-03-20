===============================================================================
              REAL-TIME GESTURE-BASED VOLUME CONTROLLER
===============================================================================
A Python application that controls system volume using hand gestures through webcam.
Built with OpenCV and MediaPipe.
===============================================================================

QUICK START:
1. Install: pip install opencv-python mediapipe pycaw numpy comtypes
2. Run: python gesture_volume_controller.py
3. Use: 
   - Pinch fingers for volume control
   - Fist for mute/unmute
   - Peace sign for calibration
   - ESC to exit

===============================================================================

FEATURES:
✅ Real-time volume control with hand gestures
✅ Multiple gesture support (volume, mute, calibration)
✅ Auto-calibration for different hand sizes
✅ Visual feedback with color-coded volume bar
✅ On-screen instructions and status display
✅ Low latency (~35ms response time)

GESTURE CONTROLS:
📏 PINCH GESTURE - Volume Control
   • Bring thumb and index finger together
   • Move closer = Volume Down | Move apart = Volume Up

🔇 FIST GESTURE - Mute/Unmute
   • Make a fist to toggle mute

⚙️ PEACE SIGN - Calibration Mode
   • Show peace sign (V) for 2 seconds
   • Move hand closer/farther for auto-calibration

INSTALLATION:

1. INSTALL PYTHON (3.9 or higher)
   - Download from python.org
   - Check "Add Python to PATH" during installation

2. INSTALL DEPENDENCIES:
   Open Command Prompt and run:
   pip install opencv-python mediapipe pycaw numpy comtypes

3. DOWNLOAD & RUN:
   - Save the Python file as "gesture_volume_controller.py"
   - Run: python gesture_volume_controller.py

TROUBLESHOOTING:

❌ Camera not working?
   → Check if another app is using camera
   → Run as Administrator

❌ Volume control not working?
   → Run Command Prompt as Administrator
   → Ensure speakers are not muted

❌ Hand detection poor?
   → Use good lighting
   → Plain background works best
   → Keep hand clearly visible

❌ Module errors?
   → Reinstall: pip install opencv-python mediapipe pycaw numpy comtypes

PERFORMANCE TIPS:
• Use well-lit environment
• Plain background improves detection
• Keep hand within webcam frame
• Regular calibration improves accuracy

TECHNICAL DETAILS:
• Libraries: OpenCV, MediaPipe, Pycaw, NumPy
• Hand Landmarks: 21 points per hand
• Processing: Real-time at 30 FPS
• Platform: Windows (primary), extendable to Linux/macOS

FILES REQUIRED:
• gesture_volume_controller.py (main application file)

FUTURE ENHANCEMENTS:
• Multi-gesture support (media controls)
• Cross-platform compatibility
• Custom gesture training
• Mobile app version

SUPPORT:
For issues, check troubleshooting section above.
Ensure all dependencies are properly installed.

===============================================================================
              HAPPY GESTURE CONTROLLING! 🎵👋
===============================================================================
