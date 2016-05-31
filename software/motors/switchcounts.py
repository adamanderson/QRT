import RPi.GPIO as GPIO
import time

n_Up = 0
n_Down = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
current_state = GPIO.input(17)


for n in range(10000):
    last_state = current_state
    current_state = GPIO.input(17)
    if last_state == 0 and current_state == 1:
        n_Up = n_Up + 1
    if last_state == 1 and current_state == 0:
        n_Down = n_Down + 1
    time.sleep(0.001)
print("n_Up - " + str(n_Up))
print("n_Down - " + str(n_Down))
