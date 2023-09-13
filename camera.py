import logging
import os
import time
import numpy as np
from PIL import Image
import glob
from donkeycar.utils import rgb2gray
from threading import Thread
from picamera.array import PiRGBArray
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import datetime


class BaseCamera:
	
    def __init__(self):
         from picamera.array import PiRGBArray
         from picamera import PiCamera
         self.snap = False  # Initialize snap to False, this variable is essential so that 
         self.photo_res = (1920, 1080)
         self.change = False
         #self.captured = False
         self.restart = False
        
        
        
    def run_threaded(self, photo):
            
        if photo and not self.snap:
            
            self.shutdown() #stopping the camera thread so the buffer wont overload 
            self.__init__(change = True)# initialization idicating to set the higher resolution 
            self.snap = True 
            time.sleep(.5) 
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f'/home/piracer/mycar/NDT_photos/{timestamp}.jpg'
            
            with open(filename, 'wb') as f:
                self.camera.capture(f, format='jpeg')    
            
            print ('PHOTO CAPTURED AND SAVED, PRESS PHOTO TO RESUME THE STREAM')
            self.frame = [1] #for now just a black screen indicating the photo process
            self.shutdown() #closing the thread
                        
        elif not photo and self.snap:
            
            self.snap = False  
            self.__init__() #initiating the camera and the whole update thread 
            t = Thread(target=self.update, args=())
            t.daemon = True
            t.start()
            self.run_threaded(photo)
            
        return self.frame
        



class PiCamera(BaseCamera):
    def __init__(self, image_w=640, image_h=400, image_d=3, framerate=20, vflip=True, hflip=False, change = False):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        super().__init__()

        resolution = (image_w, image_h)
        # initialize the camera and stream
        self.camera = PiCamera() #PiCamera gets resolution (height, width)
        if not change:
            self.camera.resolution = resolution
        else:
            self.camera.resolution = (1920, 1080)
            
        self.camera.framerate = framerate
        self.camera.vflip = vflip
        self.camera.hflip = hflip
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="rgb", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True
        self.image_d = image_d
        
      
       
        

       

    def run(self):
        # grab the frame from the stream and clear the stream in
        # preparation for the next frame
        
        if self.stream is not None:
            f = next(self.stream)
            if f is not None:
                self.frame = f.array
                self.rawCapture.truncate(0)
                
                if self.image_d == 1:
                    self.frame = rgb2gray(self.frame)
                
        
        return self.frame

    def update(self):
        # keep looping infinitely until the thread is stopped
        while self.on:
            
            self.run()
            if not self.on: 
                break 

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        logger.info('Stopping PiCamera')
                    
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.stream = None
        self.rawCapture = None
        self.camera = None
