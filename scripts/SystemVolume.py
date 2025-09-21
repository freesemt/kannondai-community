""""
Change the system volume on Windows.
"""
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

def set_system_volume(vol):  # vol: 0.0〜1.0
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(vol, None)

if __name__ == "__main__":
    # 例: 50%に設定
    set_system_volume(0.5)