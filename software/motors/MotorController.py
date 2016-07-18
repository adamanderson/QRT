import RPi.GPIO as GPIO
import time

class MotorControl(object):
    def __init__(self): #constructor
        self.currentPosition = 0
        self.currentPosition2 = 0
        self.updater = 0
        self.updater2 = 0

    def reset(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        for n in range(20000):
            GPIO.output(6, GPIO.HIGH)
            GPIO.output(19, GPIO.LOW)
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(18, GPIO.LOW)
            self.currentPosition = 0
            self.currentPosition2 = 0
            time.sleep(0.001)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)

    def motorcontrol(self, position, position2): #creates the function to go to a set length
        positionincounts = round(position*95.47)
        positionincounts2 = round(position2*95.47)
        self.currentPosition #calls variables
        self.currentPosition2
        self.updater = 0
        self.updater2 = 0
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        current_state = 1
        
        if current_state == 1:
            last_state = current_state - 1
        else:
            last_state = current_state + 1
            
        while (self.currentPosition) != positionincounts: #creates a loop till it gets to the position it needs to be at
            last_state = current_state
            current_state = GPIO.input(17)
            if (self.currentPosition) < positionincounts: #checks if the motor needs to go in or out
                if last_state == 0 and current_state == 1: #counting everytime the pulse changes
                    self.currentPosition += 1 #extends the motor
                    self.updater += 1 #update timer
                if last_state == 1 and current_state == 0:
                    self.currentPosition = self.currentPosition + 1
                    self.updater += 1
                GPIO.output(6, GPIO.LOW)
                GPIO.output(19, GPIO.HIGH)
                if self.updater == 1: #prints out position at a certain interval and resets the update timer 
                    print('Your current position is (A) in motor 1 ',self.currentPosition)
                    self.updater = 0
                time.sleep(0.001)
            if (self.currentPosition) > positionincounts:
                if last_state == 0 and current_state == 1:
                    self.currentPosition -= 1 #retracts the motor
                    self.updater += 1
                if last_state == 1 and current_state == 0:
                    self.currentPosition -= 1
                    self.updater += 1
                GPIO.output(6, GPIO.HIGH)
                GPIO.output(19, GPIO.LOW)
                if self.updater == 1:
                    print('Your current position is (B) in motor 1 ',(self.currentPosition))
                    self.updater = 0
                time.sleep(0.001)
            time.sleep(0.001)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        currentPositionininches = positionincounts/95.47
        print('You have reached your position in motor 1')
        print(currentPositionininches)
        current_state2 = 1

        if current_state2 == 1:
            last_state2 = current_state2 - 1
        else:
            last_state2 = current_state2 + 1
        print(self.currentPosition2)
        print(positionincounts2)
        while (self.currentPosition2) != positionincounts2: #creates a loop till it gets to the position it needs to be at
            print('Current state 2 is ',current_state2)
            print('Last state 2 is ',last_state2)
            last_state2 = current_state2
            current_state2 = GPIO.input(12)
            if (self.currentPosition2) < positionincounts2: #checks if the motor needs to go in or out
                if last_state2 == 0 and current_state2 == 1: #counting everytime the pulse changes
                    self.currentPosition2 += 1 #extends the motor
                    self.updater2 += 1 #update timer
                if last_state2 == 1 and current_state2 == 0:
                    self.currentPosition2 = self.currentPosition2 + 1
                    self.updater2 += 1
                GPIO.output(24, GPIO.LOW)
                GPIO.output(18, GPIO.HIGH)
                if self.updater2 == 1: #prints out position at a certain interval and resets the update timer 
                    print('Your current position is (A) in motor 2 ',self.currentPosition2)
                    self.updater2 = 0
                time.sleep(0.001)
            if (self.currentPosition2) > positionincounts2:
                if last_state2 == 0 and current_state2 == 1:
                    self.currentPosition2 -= 1 #retracts the motor
                    self.updater2 += 1
                if last_state2 == 1 and current_state2 == 0:
                    self.currentPosition2 -= 1
                    self.updater2 += 1
                GPIO.output(24, GPIO.HIGH)
                GPIO.output(18, GPIO.LOW)
                if self.updater2 == 1:
                    print('Your current position is (B) in motor 2 ',(self.currentPosition2))
                    self.updater2 = 0
                time.sleep(0.001)
            time.sleep(0.001)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        currentPositionininches2 = positionincounts2/95.47
        print('You have reached your position in motor 2')
        print(currentPositionininches2)
