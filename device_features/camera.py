# THE Port Pier 37 ID Hunters
# Camera access from the Raspberry Pi in a single file
# Press an external button to capture an image and save it annotated
# with miscelaneous information such as time, unique ID, etc.


# 1. Hardware:
# Raspberry Pi B+ 512, Pi Camera, external button

# Alternatively, use the keyboard or any other input
bcm_button_channel = 12 # PIN to which the external button is connected
output_filename = "output.jpg"

# Alternatively, use the information from a connected GPS unit
location = "46.229591 N, 6.054655 E"


# 2. Software:

# Using Python 2.7, PiCamera, RPi, OpenCV 2
# Install Raspbian, OpenCV 2 with Python bindings

from picamera import PiCamera
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import cv2
import datetime
import numpy
import time
import uuid

def button_capture():
    camera = PiCamera()
    
    def capture():
        raw = PiRGBArray(camera)
        camera.capture(raw, format="bgr")
        camera.stop_preview()
        image = raw.array
        return image

    camera.start_preview()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bcm_button_channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    print "Waiting for a button press"
    GPIO.wait_for_edge(bcm_button_channel, GPIO.FALLING)
    return capture()


def annotate(image, lines):
    scale = 1
    row = 1
    dark = (0, 0, 0)
    thick = 2*scale
    shadow = thick/2
    light = (255, 240, 240)
    thin = 1*scale

    for line in lines:
        x = 25*scale
        y = 10*scale + 30*scale*row
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, line, (x, y), font, scale, dark, thick)
        cv2.putText(image, line, (x+shadow, y+shadow), font, scale, light, thin)
        row = row + 1

        
def image_properties(picture):
    def intensity(pixel):
        return numpy.average(pixel)

    height = picture.shape[0]
    width = picture.shape[1]
    
    row = int(height/2)
    row_intensities = [intensity(picture[row, column]) for column in range(0, width)]
    average_intensity = int(numpy.average(row_intensities))
    print "The average intensity of row ", row, " is ", average_intensity

    std_intensity = int(numpy.std(row_intensities))
    print "The standard deviation of row ", row, " is ", std_intensity
    
    return [average_intensity, std_intensity]


def metadata(image):
    uid = str(uuid.uuid4())[0:13]
    when = datetime.datetime.now().time().isoformat()
    props = image_properties(image)
    attrs = str(props[0]) +" "+ str(props[1])
    return ["ID: " + uid ,
            "TIME: " + when,
            "LOCATION: " + location ,
            "IMAGE ATTRS: " + attrs]


def process():
    scale = 0.5
    
    captured = button_capture()
    print "Picture captured"

    scaled = cv2.resize(captured, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    annotate(scaled, metadata(scaled))
    cv2.imwrite(output_filename, scaled)
    print "Result saved"

    
process()
