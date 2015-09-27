__author__ = 'pi'

import time
import picamera
import os
import math

datapath = '/mnt/shareWindows'

def captureShortSeries(nsteps, maxExposureTime, mode, iso):

    global camera
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.rotation = 90
        camera.preview_fullscreen = False
        camera.preview_window = (1070,475,300,400)
        fps = float(maxExposureTime**(-1.0))
        camera.framerate = fps
        camera.iso = iso
        # Wait for the automatic gain control to settle
        time.sleep(2)
        camera.start_preview()
        # Now fix the values
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        # Finally, take several photos with the fixed settings
        for i in range(nsteps+1):
            intervalMode(mode, i, fps, nsteps)
            time.sleep(2)
            if camera.shutter_speed < 1000:
                print "["+str(i)+"] Exposure Time: "+str(camera.exposure_speed*1.0)+" us."
                print "["+str(i)+"] Shutter  Time: "+str(camera.shutter_speed*1.0)+" us."
            if 1000<camera.shutter_speed < 1e6:
                print "["+str(i)+"] Exposure Time: "+str(camera.exposure_speed/1000.0)+" ms."
                print "["+str(i)+"] Shutter  Time: "+str(camera.shutter_speed/1000.0)+" ms."
            if 1e6<camera.shutter_speed:
                print "["+str(i)+"] Exposure Time: "+str(camera.exposure_speed/1.0e6)+" s."
                print "["+str(i)+"] Shutter  Time: "+str(camera.shutter_speed/1.0e6)+" s."
            print "------------------------------------"
            camera.capture_sequence([os.path.join(datapath, 'shortSeries%02d.jpg' % i)])
        camera.stop_preview()


def intervalMode(mode, i, fps, nsteps):

        if mode == "linear":
            shutter_sp = int(i*1.0e6/(fps*nsteps*1.0))
            camera.shutter_speed = shutter_sp

        if mode == "exp":
            shutter_sp = int(i*1.0e6/(1.0*fps*nsteps*math.exp(1.0))*math.exp(float(i)*nsteps**(-1.0)))
            camera.shutter_speed = shutter_sp



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


captureShortSeries(12, 0.25, "exp", 400)
#printCameraSettings()

