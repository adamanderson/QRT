import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

def set_motor_direction (direction):
    '''
    Sets linear actuator direction.

    Parameters:
    direction : str
       Set to 'out', 'in', or 'off' to control direction.

    Returns:
    None
    '''
    if direction == "in":
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(19, GPIO.LOW)
        
    elif direction == "out":
        GPIO.output(6, GPIO.LOW)
        GPIO.output(19, GPIO.HIGH)

    elif direction == "off":
        GPIO.output(6, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)

    else:
        print("error, enter direction")
