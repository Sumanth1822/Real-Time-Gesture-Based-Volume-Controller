import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

class VolumeController:
    def __init__(self):
        # Initialize audio devices and volume interface
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Get volume range
        self.volume_range = self.volume.GetVolumeRange()
        self.min_vol = self.volume_range[0]
        self.max_vol = self.volume_range[1]
        
        # Volume control parameters
        self.smoothness = 5  # Higher value = smoother volume changes
        self.vol_history = []
        
    def set_volume(self, vol_percentage):
        """Set system volume based on percentage (0-100)"""
        try:
            # Smooth volume changes
            self.vol_history.append(vol_percentage)
            if len(self.vol_history) > self.smoothness:
                self.vol_history.pop(0)
            
            # Calculate smoothed volume
            smooth_vol = sum(self.vol_history) / len(self.vol_history)
            
            # Convert percentage to volume range
            vol_db = np.interp(smooth_vol, [0, 100], [self.min_vol, self.max_vol])
            
            # Set volume
            self.volume.SetMasterVolumeLevel(vol_db, None)
            return smooth_vol
        except Exception as e:
            print(f"Volume control error: {e}")
            return vol_percentage
    
    def get_current_volume(self):
        """Get current volume percentage"""
        try:
            current_db = self.volume.GetMasterVolumeLevel()
            current_percentage = np.interp(current_db, [self.min_vol, self.max_vol], [0, 100])
            return current_percentage
        except:
            return 0
    
    def mute_volume(self):
        """Toggle mute"""
        try:
            current_mute = self.volume.GetMute()
            self.volume.SetMute(not current_mute, None)
            return not current_mute
        except:
            return False