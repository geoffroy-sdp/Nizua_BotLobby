import sys
import time
import vgamepad as vg

def create_gamepad(index):
    print(f"[PY] Creating gamepad {index}")
    gamepad = vg.VX360Gamepad()
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.2)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    print(f"[PY] Gamepad {index} ready")

if __name__ == "__main__":
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    create_gamepad(idx)
