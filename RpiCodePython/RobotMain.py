from MotorModule import Motor
import keyPressModule
import JoyStickModule
from time import sleep

motor= Motor(2,3,4,17,22,27)
movement = 'Joystick' #[keyboard, Joystick']


keyPressModule.init()

def main():
    if movement == 'Joystick':
        jsVal = js.getJS()
        motor.move(-(jsVal['axis2']), -(jsVal['axis1']), 0.1)
    else:
        if keyPressModule.getKey('UP'):
            motor.move(0.6, 0, 0.1)
        elif keyPressModule.getKey('DOWN'):
            motor.move(-0.6, 0, 0.1)
        elif keyPressModule.getKey('LEFT'):
            motor.move(0.5, 0.3, 0.1)
        elif keyPressModule.getKey('RIGHT'):
            motor.move(0.5, -0.3, 0.1)
        else:
            motor.stop(0.1)
            

if __name__ == '__main__':
    while True:
        main()