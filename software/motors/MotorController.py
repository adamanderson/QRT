import RPi.GPIO as GPIO
import time
import numpy as np
from datetime import datetime
import calendar

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

    def motorcontrol(self, ra, dec): #creates the function to go to a set length, note: the values have to be in decimal form
        latitude = 41.825
        longitude = -88.2439
        radegs = ra * 15
        unitime = datetime.utcnow()
        ut = unitime.hour + unitime.minute/60.+unitime.second/3600.
        dj2000 = float((calendar.timegm(time.gmtime()) - 946727936.)/86400.)
        lst = 100.46 + 0.985647 * dj2000 + longitude + (15*ut)
        while lst < 0:
            lst += 360
            if lst > 360:
                lst -= 360

        while lst > 360:
            lst -= 360
            if lst < 0:
                lst += 360

        hourAngle = lst-radegs

        while hourAngle < 0:
            hourAngle += 360
            if hourAngle > 360:
                hourAngle -= 360

        while hourAngle > 360:
            hourAngle -= 360
            if hourAngle < 0:
                hourAngle += 360

        rightAscension = radegs*(np.pi/180)
        declination = dec*(np.pi/180)
        lat = latitude*(np.pi/180)
        longi = longitude*(np.pi/180)
        ha = hourAngle*(np.pi/180)

        sinALT = np.sin(declination)*np.sin(lat)+np.cos(declination)*np.cos(lat)*np.cos(ha)
        radALT = np.arcsin(sinALT)
        ALT = radALT*(180/np.pi)

        cosELEV = (np.sin(declination)-np.sin(radALT)*np.sin(lat))/(np.cos(radALT)*np.cos(lat))
        radELEV = np.arccos(cosELEV)
        ELEV  = radELEV*(180/np.pi)
        if np.sin(ha) < 0:
            AZ = ELEV
        else:
            AZ = 360-ELEV

        print(ALT)
        print(AZ)
        
        a = AZ*(np.pi/180)
        e = (ELEV+0.1)*(np.pi/180)
        x = np.cos(a)*np.sin((np.pi/2)-e)
        z = np.cos((np.pi/2)-e)
        alpha = np.arccos(x)
        delta = np.arccos(z/(np.sin(np.arccos(x))))
        alphaindegs = alpha*(180/np.pi)
        deltaindegs = delta*(180/np.pi)
        alphadata_extension = [0, 0.8125, 1.875, 2.125, 2.875, 3.375, 4, 4.75, 5.75, 6.5, 7.5, 8.375, 9.5, 10.5, 11.625, 12.625, 13.4375, 14.4375]
        alphadata_angle = [23.93, 28.07, 31.26, 34.13, 37.66, 40.89, 43.49, 46.77, 53.45, 58.22, 63.11, 68.13, 74.42, 80.98, 87.46, 94.3, 103.54, 105]
        position = np.interp(alphaindegs, alphadata_angle, alphadata_extension)
        deltadata_extension = [0, 1, 2, 3, 4, 5, 6, 7]
        deltadata_angle = [26, 37, 47, 55, 65, 73, 81, 90]
        position2 = np.interp(deltaindegs, deltadata_angle, deltadata_extension)
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
        if position > 1340 or position < 0:
            print('That Right Ascension is too large for the motor.')
        else:
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
        if position2 > 670 or position2 < 0:
            print('That declination is too large for the motor.')
        else:
            while (self.currentPosition2) != positionincounts2: #creates a loop till it gets to the position it needs to be at
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
        rafile = open('/home/pi/Data/ra.txt', 'w')
        rafile.write(str(ra))
        rafile.close()
        decfile = open('/home/pi/Data/dec.txt', 'w')
        decfile.write(str(dec))
        decfile.close()
        pos1file = open('/home/pi/Data/pos1.txt', 'w')
        pos1file.write(str(currentPositionininches))
        pos1file.close()
        pos2file = open('/home/pi/Data/pos2.txt', 'w')
        pos2file.write(str(currentPositionininches2))
        pos2file.close()
