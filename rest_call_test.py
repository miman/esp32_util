import machine
import time
import urequests 
from libs.global_props import GlobalProperties
from libs.task_base import Task

# This is a test class which requests all users from the test REST site 'https://jsonplaceholder.typicode.com/users'
# whenever you press the BOOT button.
# The resulting list is written to the console
# Code example from: https://techtotinker.blogspot.com/2020/11/019-esp32-micropython-openweather.html
class RestCaller(Task):
    def __init__(self):
        super().__init__()
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.sw = machine.Pin(0, machine.Pin.IN)
        # tim0 = machine.Timer(0)

        # **************************************
        # Constants and variables:
        self.HTTP_HEADERS = {'Content-Type': 'application/json'}
        self.request_data=False
        self.sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.handle_callback)
        self.led.off()

    def handle_callback(self, pin):
        self.request_data=True
        # print('value set to: ' + str(led.value()))

    def init(self, global_props: GlobalProperties):
        super().init(global_props)
        
    # **************************************
    # Process function, should be called from the main loop
    def process(self):
        if self.request_data:
            print('Requesting data...')
            self.led.on()  # LED on while fetching data
            response = urequests.get( 
              'https://jsonplaceholder.typicode.com/users', 
              headers = self.HTTP_HEADERS )
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
            self.request_data=False
            self.led.off()  # data fetched -> LED off
