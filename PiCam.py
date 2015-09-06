__author__ = 'pi'

import time
import picamera
import os

datapath = '/home/pi/PycharmProjects/first_test/First-repos/data'

def captureShortSeries():

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 30
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        print g
        camera.awb_mode = 'off'
        camera.awb_gains = g
        # Finally, take several photos with the fixed settings
        for i in range(20):
            camera.shutter_speed =1+100*i**2
            print camera.shutter_speed
            camera.capture_sequence([os.path.join(datapath, 'shortSeries%02d.jpg' % i)])


def captureTimelapseSeries():

    with picamera.PiCamera() as camera:
        camera.rotation = 90
        camera.preview_fullscreen = False
        camera.preview_window = (0,0,600,800)
        time.sleep(2)
        camera.start_preview()
        try:
            for i, filename in enumerate(camera.capture_continuous(os.path.join(datapath, 'timelapseSeries{counter:03d}.jpg'))):
                camera.shutter_speed =(i+1)*5000
                print camera.exposure_speed
                print camera.shutter_speed
                print('Captured %s' % filename)
                time.sleep(1) # wait 1 sec
                if i == 1:
                    break
        finally:
            camera.stop_preview()


captureTimelapseSeries()