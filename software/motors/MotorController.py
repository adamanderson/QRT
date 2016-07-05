import RPi.GPIO as GPIO
import time

class MotorControl(object):
    def __init__(self): #constructor
        self.currentPosition = 0
        self.updater = 0

    def reset(self):
        for n in range(180000):
            GPIO.output(6, GPIO.LOW)
            GPIO.output(19, GPIO.HIGH)
            time.sleep(0.001)

    def motorcontrol(self, position): #creates the function to go to a set length
        positionincounts = position*95.47
        self.currentPosition #calls variables
        self.updater = 0
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        current_state = 1
        while (self.currentPosition) != positionincounts: #creates a loop till it gets to the position it needs to be at
            last_state = current_state
            current_state = GPIO.input(17)
            if (self.currentPosition) < positionincounts: #checks if the motor needs to go in or out
                print('Current State=', current_state)
                print('Last State=', last_state)
                if last_state == 0 and current_state == 1: #counting everytime the pulse changes
                    self.currentPosition += 1 #extends the motor
                    self.updater += 1 #update timer
                if last_state == 1 and current_state == 0:
                    self.currentPosition = self.currentPosition + 1
                    self.updater += 1
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(19, GPIO.LOW)
                if self.updater == 100: #prints out position at a certain interval and resets the update timer 
                    print('Your current position is ',self.currentPosition)
                    self.updater = 0
                time.sleep(0.001)
            if (self.currentPosition) > positionincounts:
                print('Current State=', current_state)
                print('Last State=', last_state)
                if last_state == 0 and current_state == 1:
                    self.currentPosition -= 1 #retracts the motor
                    self.updater += 1
                if last_state == 1 and current_state == 0:
                    self.currentPosition -= 1
                    self.updater += 1
                GPIO.output(6, GPIO.LOW)
                GPIO.output(19, GPIO.HIGH)
                if self.updater == 100:
                    print('Your current position is ',(self.currentPosition))
                    self.updater = 0
                time.sleep(0.001)
            time.sleep(0.001)            
        GPIO.output(6, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        currentPositionincounts = self.currentPosition/95.47
        print('You have reached your position')
        print(currentPositionincounts)
