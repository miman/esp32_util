import machine
import time
import network 
import libs.wifi_credentials 
import urequests 
import dht

# Code example from:
# https://techtotinker.blogspot.com/2020/11/019-esp32-micropython-openweather.html

led = machine.Pin(2, machine.Pin.OUT)
sw = machine.Pin(0, machine.Pin.IN)
# tim0 = machine.Timer(0)

# **************************************
# Configure the ESP32 wifi as STAtion
sta = network.WLAN(network.STA_IF)
if not sta.isconnected(): 
  print('connecting to network...') 
  sta.active(True) 
  sta.connect(wifi_credentials.ssid, wifi_credentials.password) 
  while not sta.isconnected(): 
    pass 
print('network config:', sta.ifconfig())

# **************************************
# Constants and variables:
HTTP_HEADERS = {'Content-Type': 'application/json'}
request_data=False

def handle_callback(pin):
    global request_data
    request_data=True
    # print('value set to: ' + str(led.value()))

sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_callback)

led.off()

# **************************************
# Main loop:
while True: 
    if request_data:
        print('Requesting data...')
        led.on()  # LED on while fetching data
        response = urequests.get( 
          'https://jsonplaceholder.typicode.com/users', 
          headers = HTTP_HEADERS )
        # check status code of the request
        if response.status_code == 200:
            # get the json format of data
            data = response.json()
            
            for item in data:
                print('Name: ' + item['name'])
        else:
            # show error message
            print_text('Error in HTTP request.', 3, 20, 1)
            print('Error in HTTP request.')
        request_data=False
        led.off()  # data fetched -> LED off