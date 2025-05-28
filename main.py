import serial
from pynput.keyboard import Controller, Key
import time
from dataclasses import dataclass

keyboard = Controller()
# PORT: str = '/dev/cu.usbmodem3101'  # usb hub
PORT: str = '/dev/cu.usbserial-310'  # usb port on the right
DEADZONE: int = 80
MIDDLE: int = 511
MAX: int = 1023
BUFFER_SIZE = 10
INPUT_HISTORY = [0] * BUFFER_SIZE

class Input:
    def __init__(self):
        self.down: "Coordinate" = Coordinate((0, MIDDLE-DEADZONE), (MIDDLE//2 + 1, MIDDLE + MIDDLE//2 - 1))
        self.up: "Coordinate" = Coordinate((MIDDLE+DEADZONE, MAX), (MIDDLE//2 + 1, MIDDLE + MIDDLE//2 -1))
        self.right: "Coordinate" = Coordinate((MIDDLE//2 + 1, MIDDLE + MIDDLE//2 - 1), (0, MIDDLE-DEADZONE))
        self.left: "Coordinate" = Coordinate((MIDDLE//2 + 1, MIDDLE + MIDDLE//2 - 1), (MIDDLE+DEADZONE, MAX))
        self.down_right: "Coordinate" = Coordinate((0, MIDDLE//2), (0, MIDDLE//2))
        self.up_right: "Coordinate" = Coordinate((MIDDLE + MIDDLE//2, MAX), (0, MIDDLE//2))
        self.down_left: "Coordinate" = Coordinate((0, MIDDLE//2), (MIDDLE + MIDDLE//2, MAX))
        self.up_left: "Coordinate" = Coordinate((MIDDLE + MIDDLE//2, MAX), (MIDDLE + MIDDLE//2, MAX))
        
@dataclass (frozen=True)
class Coordinate:
    x: tuple
    y: tuple

def main() -> None:
    dirct = Input()
    analog_input = serial.Serial(PORT, 9600)
    time.sleep(2)
    last_key_press_time = time.time()
    rotate: bool = False
    action_taken = False
    while True:
        if analog_input.in_waiting > 0:
            try:
                stick_vals = analog_input.readline().decode('utf-8').strip().split(",")
                x_val = int(stick_vals[0])
                y_val = int(stick_vals[1])
                z_val = int(stick_vals[2])
                current_time = time.time()
                global INPUT_HISTORY
                
                if current_time - last_key_press_time > 0.05:
                    if INPUT_HISTORY[-2] == 1 and INPUT_HISTORY[-1] == 8:
                        # print('counter')
                        keyboard.type('e')
                        rotate = True
                    elif INPUT_HISTORY[-1] != 0 and INPUT_HISTORY[-2] != 0 and INPUT_HISTORY[-1] > INPUT_HISTORY[-2]:
                        # print('wise')
                        keyboard.type(',')
                        rotate = True
    
                    if INPUT_HISTORY[-2] == 8 and INPUT_HISTORY[-1] == 1:
                        # print('wise')
                        keyboard.type(',')
                        rotate = True
    
                    elif INPUT_HISTORY[-1] != 0  and INPUT_HISTORY[-1] < INPUT_HISTORY[-2]:
                        # we are rotating counter-clockwise
                        # print('counter')
                        keyboard.type('e')
                        rotate = True
                        # print(INPUT_HISTORY)

                    if INPUT_HISTORY[-1] == 0 and INPUT_HISTORY[-2] != 0 and not action_taken and not rotate:
                        # a button has been pressed
                        print('press')
                        button_out(INPUT_HISTORY[-2])
                        action_taken = True
                    
                    direction = get_direction(x_val, y_val, dirct)
                    
                    if not (direction == 0 and INPUT_HISTORY[-1] == 0):
                        INPUT_HISTORY.pop(0)
                        INPUT_HISTORY.append(direction)
                    else:
                        rotate = False
                        action_taken = True
                    
                    if 1 <= direction <= 8 and not rotate:
                        action_taken = False
                        
                    last_key_press_time = current_time
                    
            except IndexError:
                pass
            except ValueError:
                pass


def get_direction(x: int, y: int, dirct: "Input") -> int:
    """
    0 -> None
    1 -> up
    2 -> up_right
    3 -> right
    4 -> down_right
    5 -> down
    6 -> down_left
    7 -> left
    8 -> up_left
    """
    if (dirct.up.x[0] <= x <= dirct.up.x[1]
          and dirct.up.y[0] <= y <= dirct.up.y[1]):
        return 1
    elif (dirct.up_right.x[0] <= x <= dirct.up_right.x[1]
          and dirct.up_right.y[0] <= y <= dirct.up_right.y[1]):
        return 2
    elif (dirct.right.x[0] <= x <= dirct.right.x[1]
          and dirct.right.y[0] <= y <= dirct.right.y[1]):
        return 3
    elif (dirct.down_right.x[0] <= x <= dirct.down_right.x[1]
          and dirct.down_right.y[0] <= y <= dirct.down_right.y[1]):
        return 4
    elif (dirct.down.x[0] <= x <= dirct.down.x[1]
          and dirct.down.y[0] <= y <= dirct.down.y[1]):
        return 5
    elif (dirct.down_left.x[0] <= x <= dirct.down_left.x[1]
          and dirct.down_left.y[0] <= y <= dirct.down_left.y[1]):
        return 6
    elif (dirct.left.x[0] <= x <= dirct.left.x[1]
            and dirct.left.y[0] <= y <= dirct.left.y[1]):
        return 7
    elif (dirct.up_left.x[0] <= x <= dirct.up_left.x[1]
          and dirct.up_left.y[0] <= y <= dirct.up_left.y[1]):
        return 8
    return 0


def button_out(button: int) -> None:
    match button:
        case 1:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        case 7:
            # move track up
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        case 3:
            # move track down
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        case 5:
            keyboard.type('r')


if __name__ == "__main__":
    main()