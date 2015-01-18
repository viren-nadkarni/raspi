import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

try:
    while True:
        GPIO.output(14, True)
        time.sleep(0.2)
        GPIO.output(14, False)

        GPIO.output(15, True)
        time.sleep(0.2)
        GPIO.output(15, False)

except KeyboardInterrupt:
    GPIO.cleanup()
