import RPi.GPIO as GPIO
import time

# Pin configuration
SWITCH_PIN = 9  # GPIO 9 (BCM numbering)

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up resistor

def switch_callback(channel):
    if GPIO.input(SWITCH_PIN) == GPIO.LOW:  # Switch is pressed
        print("Switch is ON")
    else:  # Switch is released
        print("Switch is OFF")

# Detect switch state changes
GPIO.add_event_detect(SWITCH_PIN, GPIO.BOTH, callback=switch_callback, bouncetime=200)

print("Monitoring GPIO 9 for switch state changes. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.1)  # Keep the program running
except KeyboardInterrupt:
    print("Exiting program.")

# Cleanup GPIO on exit
finally:
    GPIO.cleanup()
