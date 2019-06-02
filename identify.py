import io
import os
import threading

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

from SMS import *
sms = None

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    os.path.dirname(__file__),
    'googleauth.json')

# Instantiates a client
client = vision.ImageAnnotatorClient()

label_list = None

def find_labels():
    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'bus.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    try:
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # print('Labels:')
        # for x in range(len(labels)):
        #     label_list[x] = labels[x].description
        # #     print('\t' + label.description)
        # print(label_list)

        global label_list
        label_list = labels

        match_labels(labels)
    except:
        print('An API error has occured.')

import cv2

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 470)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

def putText(image, labels):
    height, width, channels = image.shape
    if labels is not None and len(labels) > 0:
        scale = 30
        for i in range(len(labels)):
            cv2.putText(image, labels[i].description,
                        (10, int(scale * i)+ 30),
                        font,
                        fontScale,
                        fontColor,
                        lineType)
    return image


def match_labels(labels):
    for label in labels:
        for match in matchers:
            if str.lower(match) in str.lower(label.description):
                if message_sent['sent']:
                    if time.time() - message_sent['time'] < 5 * 60:
                        sms.send('The Bus is in front of your house!')
                        message_sent['sent'] = False
                        return
                sms.send('The Bus has entered!')
                message_sent['sent'] = True
                message_sent['time'] = time.time()
                print('Sent Message that the Bus has entered!')



import numpy as np
import time

cap = cv2.VideoCapture(0)
length = 0
seconds = 1

message_sent = {'sent': False, 'time': None}

matchers = {'bus', 'school'}

phone = '2677508123'
email = 'shivam4141997@gmail.com'
password = '41419977'

if __name__ == "__main__":
    sms = SMS(phone, email, password)
    sms.send('Program Starting!')
    while(1):
        # Take each frame

        # _, frame = cap.read()
        # k = cv2.waitKey(5) & 0xFF
        # cv2.imwrite( os.path.join(
        #     os.path.dirname(__file__),
        #     'frame.jpg'), frame )

        if length % (30 * seconds) == 0:
            thread = threading.Thread(target=find_labels)
            thread.start()

        # image = putText(frame, label_list)
        # cv2.imshow('Video',image)

        length = length + 1

        # if k == 27:
        #     break

        time.sleep(1)

cv2.destroyAllWindows()
