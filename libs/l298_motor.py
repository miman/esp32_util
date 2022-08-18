from machine import Pin, PWM
from libs.global_props import GlobalProperties
from libs.task_base import Task

# L298 motor driver
# The motor needs to use 3 PIN's
# - a PWM motor PIN
# - a PIN controlling if the engine rotates in reverse (counter-clockwise)
# - a PIN controlling if the engine rotates in forward (clockwise)
# The PIN's used MUST be a GPIO PIN supporting output mode, see end of file
class L298Motor(object):

    def __init__(self, motor_pin, reverse_ctrl_pin, forward_ctrl_pin, freq=1000):
        self.freq = freq
        self.speed = 0
        self.motor_pwm = PWM(Pin(motor_pin, Pin.OUT), freq=self.freq, duty=self.speed)
        self.reverse_ctrl_pin = Pin(reverse_ctrl_pin, Pin.OUT)
        self.forward_ctrl_pin = Pin(forward_ctrl_pin. Pin.OUT)
        self.reverse_ctrl_pin(0)
        self.forward_ctrl_pin(0)

    # Stop the motor
    def stop(self):
        self.motor_pwm.duty(0)
        self.reverse_ctrl_pin(0)
        self.forward_ctrl_pin(0)

    # Order motor to rotate clockwise in the speed defined in self.speed
    def clockwise(self):
        self.forward_ctrl_pin(0)
        self.motor_pwm.duty(self.speed)
        self.reverse_ctrl_pin(1)

    # Order motor to rotate counter-clockwise in the speed defined in self.speed
    def counterclockwise(self):
        self.reverse_ctrl_pin(0)
        self.motor_pwm.duty(self.speed)
        self.forward_ctrl_pin(1)

    # Set the speed at which the motor should rotate (not direction)
    # Input shall be between 0-1023 (slow -> fast)
    def speed(self, speed=None):
        if speed is None:
            return self.speed
        else:
            self.speed = min(1023, max(0, speed))

# PWM PIN's
# On ESP32 the following PINS can NOT be used as PWM PIN's: 34, 35, 36, 39
