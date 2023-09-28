#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 20:10:44 2017

@author: wroscoe

remotes.py

The client and web server needed to control a car remotely. 
"""


import os
import json
import time
import asyncio

import requests
import tornado.ioloop
import tornado.web
import tornado.gen

from ... import utils


class RemoteWebServer():
    '''
    A controller that repeatedly polls a remote webserver and expects
    the response to be angle, throttle and drive mode. 
    '''
    
    def __init__(self, remote_url, connection_timeout=.25):

        self.control_url = remote_url
        self.time = 0.
        self.angle = 0.
        self.throttle = 0.
        self.mode = 'user'
        self.recording = False
        self.photo = False #adding photo state feature 28_08
        #use one session for all requests
        self.session = requests.Session()


        
    def update(self):
        '''
        Loop to run in separate thread the updates angle, throttle and 
        drive mode. 
        '''

        while True:
            #get latest value from server
            self.photo, self.angle, self.throttle, self.mode, self.recording = self.run() #28_08


    def run_threaded(self):
        ''' 
        Return the last state given from the remote server.
        '''
        
        #return last returned last remote response.
        return self.angle, self.throttle, self.mode, self.recording, self.photo #28_08

        
    def run(self):
        '''
        Posts current car sensor data to webserver and returns
        angle and throttle recommendations. 
        '''
        
        data = {}
        response = None
        while response == None:
            try:
                response = self.session.post(self.control_url, 
                                             files={'json': json.dumps(data)},
                                             timeout=0.25)
                
            except (requests.exceptions.ReadTimeout) as err:
                print("\n Request took too long. Retrying")
                #Lower throttle to prevent runaways.
                return self.angle, self.throttle * .8, None
                
            except (requests.ConnectionError) as err:
                #try to reconnect every 3 seconds
                print("\n Vehicle could not connect to server. Make sure you've " + 
                    "started your server and you're referencing the right port.")
                time.sleep(3)
            


        data = json.loads(response.text)
        angle = float(data['angle'])
        throttle = float(data['throttle'])
        drive_mode = str(data['drive_mode'])
        recording = bool(data['recording'])
        photo = bool(data['photo']) #28_08
        
        return angle, throttle, drive_mode, recording, photo #28_08

    def shutdown(self):
        pass
    
    
class LocalWebController(tornado.web.Application):
	
    ES_IDLE = -1
    ES_START = 0
    ES_THROTTLE_NEG_ONE = 1
    ES_THROTTLE_POS_ONE = 2
    ES_THROTTLE_NEG_TWO = 3

    def __init__(self):
        ''' 
        Create and publish variables needed on many of 
        the web handlers.
        '''

        print('Starting Donkey Server...')

        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.static_file_path = os.path.join(this_dir, 'templates', 'static')
        
        self.angle = 0.0
        self.throttle = 0.0
        self.mode = 'user'
        self.recording = False
        self.photo = False #28_08
        self.lid = True #local variable to unlock the emergency brake 
        
        self.estop_state = self.ES_IDLE

        handlers = [
            (r"/", tornado.web.RedirectHandler, dict(url="/drive")),
            (r"/drive", DriveAPI),
            (r"/video",VideoAPI),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": self.static_file_path}),
            ]

        settings = {'debug': True}

        super().__init__(handlers, **settings)
    
    def emergency_stop(self): # 27_09
        '''
        initiate a series of steps to try to stop the vehicle as quickly as possible
        '''
        print('E-Stop!!!')
        self.mode = "user"
        self.recording = False
        self.constant_throttle = False
        self.estop_state = self.ES_START
        self.throttle = 0.0

    def update(self, port=8887):
        ''' Start the tornado webserver. '''
        asyncio.set_event_loop(asyncio.new_event_loop())
        print(port)
        self.port = int(port)
        self.listen(self.port)
        tornado.ioloop.IOLoop.instance().start()

    def run_threaded(self, img_arr=None, distance = None):
        self.img_arr = img_arr
        
        if distance<=0.2 and self.lid:
		
            self.emergency_stop()
            self.lid= False
            
        elif distance >0.2 and not self.lid:
            self.lid = True
        
        #STATE MACHINe same as in controller.py
        if self.estop_state > self.ES_IDLE:
            if self.estop_state == self.ES_START:
                self.estop_state = self.ES_THROTTLE_NEG_ONE
                return 0.0, -1.0 , self.mode, False, False
            elif self.estop_state == self.ES_THROTTLE_NEG_ONE:
                self.estop_state = self.ES_THROTTLE_POS_ONE
                return 0.0, 0.01, self.mode, False, False
            elif self.estop_state == self.ES_THROTTLE_POS_ONE:
                self.estop_state = self.ES_THROTTLE_NEG_TWO
                self.throttle = -0.5
                return 0.0, self.throttle, self.mode, False, False
            elif self.estop_state == self.ES_THROTTLE_NEG_TWO:
                self.throttle += 0.05
                if self.throttle >= 0.0:
                    self.throttle = 0.0
                    self.estop_state = self.ES_IDLE
                    
                return 0.0, self.throttle, self.mode, False, False
       
            
        print(self.throttle)	
        return self.angle, self.throttle, self.mode, self.recording, self.photo #28_08
        
    def run(self, img_arr=None):
        self.img_arr = img_arr
        return self.angle, self.throttle, self.mode, self.recording, self.photo #28_08

    def shutdown(self):
        pass


class DriveAPI(tornado.web.RequestHandler):

    def get(self):
        data = {}
        self.render("templates/vehicle.html", **data)
    
    
    def post(self):
        '''
        Receive post requests as user changes the angle
        and throttle of the vehicle on a the index webpage
        '''
        data = tornado.escape.json_decode(self.request.body)
        self.application.angle = data['angle']
        self.application.throttle = data['throttle']
        self.application.mode = data['drive_mode']
        self.application.recording = data['recording']
        self.application.photo = data['photo'] #28-08


class VideoAPI(tornado.web.RequestHandler):
    '''
    Serves a MJPEG of the images posted from the vehicle. 
    '''
    async def get(self):

        self.set_header("Content-type", "multipart/x-mixed-replace;boundary=--boundarydonotcross")

        self.served_image_timestamp = time.time()
        my_boundary = "--boundarydonotcross\n"
        while True:
            
            interval = .1
            if self.served_image_timestamp + interval < time.time():


                img = utils.arr_to_binary(self.application.img_arr)

                self.write(my_boundary)
                self.write("Content-type: image/jpeg\r\n")
                self.write("Content-length: %s\r\n\r\n" % len(img)) 
                self.write(img)
                self.served_image_timestamp = time.time()
                try:
                    await self.flush()
                except tornado.iostream.StreamClosedError:
                    pass
            else:
                await tornado.gen.sleep(interval)
