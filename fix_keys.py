
from pynput.keyboard import Key, Controller
import time

print("Releasing modifier keys...")
keyboard = Controller()

# Press and release to ensure state is reset
modifiers = [Key.ctrl_l, Key.ctrl_r, Key.shift, Key.alt_l, Key.alt_r]

for key in modifiers:
    try:
        keyboard.release(key)
        print(f"Released {key}")
    except Exception as e:
        print(f"Error releasing {key}: {e}")

print("Done. Try using your keys now.")
