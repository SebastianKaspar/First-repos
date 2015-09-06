__author__ = 'pi'

import time
import picamera
import os
import math

datapath = '/home/pi/PycharmProjects/first_test/First-repos/data'

def captureShortSeries(nsteps, maxExposureTime, mode):

    global camera
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        fps = float(maxExposureTime**(-1))
        camera.framerate = fps
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        print g
        camera.awb_mode = 'off'
        camera.awb_gains = g
        # Finally, take several photos with the fixed settings
        for i in range(nsteps+1):
            intervalMode(mode, i, fps, nsteps)
            if camera.shutter_speed < 1000:
                print "Shutter speed: "+str(camera.shutter_speed)+" us."
            if 1000<camera.shutter_speed < 1e6:
                print "Shutter speed: "+str(camera.shutter_speed/1000)+" ms."
            if 1e6<camera.shutter_speed:
                print "Shutter speed: "+str(camera.shutter_speed/1e6)+" s."
            time.sleep(1)
            camera.capture_sequence([os.path.join(datapath, 'shortSeries%02d.jpg' % i)])


def intervalMode(mode, i, fps, nsteps):

        if mode == "linear":
            camera.shutter_speed =int(i*1e6/(fps*nsteps))
        if mode == "exp":
            camera.shutter_speed =int(1e6/(fps*nsteps)*math.exp(i/nsteps))
            print math.exp(i/nsteps)



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
                time.sleep(0.5)
                print camera.exposure_speed
                print camera.shutter_speed
                print('Captured %s' % filename)
                time.sleep(1) # wait 1 sec
                if i == 1:
                    break
        finally:
            camera.stop_preview()


def recordVideo():

    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.rotation = 90
        camera.preview_fullscreen = False
        camera.preview_window = (0,0,600,800)
        camera.start_preview()
        try:
            camera.start_recording(os.path.join(datapath, 'MyVideo.jpeg'))
            camera.wait_recording(3)
        finally:
            camera.stop_recording()
            camera.stop_preview()
        #using with, the camera is automatically closed
        #camera.close()


def printCameraSettings():

    with picamera.PiCamera() as camera:
        settings = camera._get_analog_gain
        print settings


captureShortSeries(100, 0.1, "exp")
#printCameraSettings()

