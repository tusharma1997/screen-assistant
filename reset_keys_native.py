
import ctypes
import time

# Load user32.dll
user32 = ctypes.windll.user32

# Constants
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# Virtual Key Codes
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12  # ALT
VK_LWIN = 0x5B
VK_RWIN = 0x5C

def release_key(vk_code):
    # Press and Release to reset state? No, just release.
    # Actually, sometimes forcing a press then release ensures the state is cleared if it's "logically" stuck.
    # But let's try just release first to avoid typing things.
    
    # 0 is the scan code, usually ignored for virtual keys
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

print("Forcing release of modifier keys via Windows API...")

keys = [VK_SHIFT, VK_CONTROL, VK_MENU, VK_LWIN, VK_RWIN]

for _ in range(3): # Do it a few times to be sure
    for k in keys:
        release_key(k)
    time.sleep(0.1)

print("Done. Modifiers should be reset.")
