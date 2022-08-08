import machine
import time

led = machine.Pin(2, machine.Pin.OUT)
sw = machine.Pin(0, machine.Pin.IN)
tim0 = machine.Timer(0)

def handle_callback(pin):
    led.value(not led.value())
    print('value set to: ' + str(led.value()))

def turn_on(pin):
    led.on()
    print('btn pressed')

def turn_off(pin):
    led.off()
    print('btn released')

sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=turn_on)
# sw.irq(trigger=machine.Pin.IRQ_RISING, handler=turn_off)
tim0.init(period=1000, mode=machine.Timer.PERIODIC, callback=handle_callback)
