#Software operating the TF Luna Lidar 

#Main goal is for the lidar to publish the value of a distance to an obstacle
#The lidar will be addded as a new part in manage.py 


#The program will follow a structure based on vehicle.py\

import time
import serial,time
import numpy as np

class Luna(object):
    '''
    https://github.com/makerportal/tfluna-python/blob/main/tfluna_realtime.py
    
    The program will get all the data fro the sensor, but for emergency brake functionality only the distance is needed
    Distance value will be the only variable returned and the only output of the part declared in manage.py
    
    '''
    def __init__(self, port="/dev/serial0", baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate, timeout=0)
        self.distance = None
        self.strength = 0
        self.temperature = 0.0
        self.on = True
        
    def open_serial(self):
        if not self.ser.isOpen():
            self.ser.open()

    def close_serial(self):
        if self.ser.isOpen():
            self.ser.close()

    def read_data(self):
        while True:
            counter = self.ser.in_waiting

            if counter > 8:
                bytes_serial = self.ser.read(9)
                self.ser.reset_input_buffer()

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    self.distance = (bytes_serial[2] + bytes_serial[3] * 256) / 100.0
                    self.strength = bytes_serial[4] + bytes_serial[5] * 256
                    raw_temperature = bytes_serial[6] + bytes_serial[7] * 256
                    self.temperature = (raw_temperature / 8.0) - 256.0

    def update(self):
        while self.on:
            self.open_serial()
            self.read_data()
        

    def run_threaded(self):
        return self.distance

    def run_threaded(self):
        print(self.distance)
      
		
        return self.distance

    def shutdown(self):
        self.close_serial()
        self.on = False
        time.sleep(2)
     
