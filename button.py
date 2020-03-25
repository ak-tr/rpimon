import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#left to right
#21, 29, 22, 17

brightness = 500

os.system("gpio -g mode 18 pwm")
os.system("gpio -g pwm 18 " + str(brightness))

while True:
    time.sleep(0.1)
    if not(GPIO.input(22)):
        if brightness < 500:
             brightness += 25
             os.system("gpio -g pwm 18 " + str(brightness))
    if not(GPIO.input(27)):
        os.system("pkill -f display.py")
        os.system("python3 /home/akif/Desktop/scripts/display.py > /dev/tty1&")
    if not(GPIO.input(23)):
        os.system("pkill -f display.py")
        os.system("clear > /dev/tty1")
    if not(GPIO.input(17)):
        if brightness > 0:
             brightness -= 25
             os.system("gpio -g pwm 18 " + str(brightness))

GPIO.cleanup()
