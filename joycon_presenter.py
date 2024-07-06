import hid
from pynput.mouse import Controller, Button
import pyautogui

JOYCON_VENDOR_ID = 0x057E
JOYCON_L_PRODUCT_ID = 0x2006
JOYCON_R_PRODUCT_ID = 0x2007

BUTTONS = {
    'y'     : 0x0008,
    'b'     : 0x0004,

    'right' : 0x0008,
    'down'  : 0x0002,

    'thumbstick_x' : 0x0006,
    'thumbstick_y' : 0x0007
}

def find_joycons():
    devices = hid.enumerate(JOYCON_VENDOR_ID, 0x0000)
    left_joycon = right_joycon = None
    for device in devices:
        if device['product_id'] == JOYCON_L_PRODUCT_ID:
            left_joycon = device
        elif device['product_id'] == JOYCON_R_PRODUCT_ID:
            right_joycon = device
    return left_joycon, right_joycon

def open_joycon(device_info):
    joycon = hid.device()
    joycon.open_path(device_info['path'])
    joycon.set_nonblocking(True)
    return joycon

def read_buttons(joycon):
    report = joycon.read(49)
    return report

def main():
    left_joycon_info, right_joycon_info = find_joycons()

    if not left_joycon_info and not right_joycon_info:
        print("No Joy-Cons found")
        return

    left_joycon = right_joycon = None
    mouse = Controller()

    if left_joycon_info:
        print("Left Joy-Con found")
        left_joycon = open_joycon(left_joycon_info)
    if right_joycon_info:
        print("Right Joy-Con found")
        right_joycon = open_joycon(right_joycon_info)

    while True:
        if right_joycon:
            buttons = read_buttons(right_joycon)
            if len(buttons) >= 1:
                if buttons[1] == BUTTONS['y']:
                    mouse.click(Button.left, 1)
                if buttons[1] == BUTTONS['b']:
                    mouse.click(Button.right, 1)
                    pyautogui.hotkey('alt', 'left')
                    
        if left_joycon:
            buttons = read_buttons(left_joycon)
            if len(buttons) >= 1:
                if buttons[1] == BUTTONS['right']:
                    mouse.click(Button.left, 1)
                if buttons[1] == BUTTONS['down']:
                    mouse.click(Button.right, 1)
                    pyautogui.hotkey('alt', 'left')


if __name__ == "__main__":
    main()