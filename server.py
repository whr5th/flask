from flask import Flask, render_template 
import requests
import gopigo
import time
import picamera
from gtts import gTTS
import os

import argparse
import base64
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

camera = picamera.PiCamera()
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('homepage.html')

@app.route('/label')
def label():
    print('labeling picture')
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('label.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 2
                }]
            }]
        }) 
        response = service_request.execute()

    def parse_response(response):
        label = json.dumps(response, indent=4, sort_keys=True)
        items = json.loads(label)['responses'][0]['labelAnnotations']

        item = items[0]['description']
        item2 = items[1]['description']

        print("Welcome! We are identifying the item now")
        print
        print
        print
        print("This is likely a " + item)
        print
        print("This is likely a " + item2)
        print
        print("Have a good day!")
        print("______________________________________________________")
        print
        string = item+ " or a " +item2
        tts = gTTS("Welcome! We are identifying this now.     This is likely a" + string, lang='en')
        tts.save("label.mp3")
        os.system("mpg321 label.mp3")
        with open("label.json", "w") as response2:
                json.dump(response, response2)

    parse_response(response)
    return render_template('label.html')
@app.route('/dutch')
def dutch():
        print("dutch")
        tts=gTTS(text='Please take my vest off! I want to be pet!', lang='en')
        tts.save("dutch.mp3")

@app.route('/picture')
def picture():
        print("Taking Picture")
        camera.capture('label.jpg')
        print("Picture taken")
        return render_template('picture.html')

@app.route('/forward')
def forward():
        print("Forward!")
        gopigo.fwd()    # Send the GoPiGo Forward
        time.sleep(1)   # for 1 second.
        gopigo.stop()   # the stop the GoPiGo
	return render_template('forward.html')

@app.route('/backward')
def backward():

        print("Backward!")
        gopigo.bwd()    # Send the GoPiGo Backward
        time.sleep(1)   # for 1 second
        gopigo.stop()   # and then stop the GoPiGo.
        return render_template('backward.html')

@app.route('/left')
def left():
        print("Left!")
        gopigo.left()
        time.sleep(1)
        gopigo.stop()
        return render_template('left.html')

@app.route('/right')
def right():
        print("Right!")
        gopigo.right()
        time.sleep(1)
        gopigo.stop()
        return render_template('right.html')

@app.route('/dance')
def dance():
        print("Dance!")
        for each in range(0,5):
                gopigo.right()
                time.sleep(0.25)
                gopigo.left()
                time.sleep(0.25)
                gopigo.bwd()
                time.sleep(0.25)
        gopigo.stop()
        return 'Dance!'

@app.route('/hello/<name>')
def hello(name):
  return render_template('name.html', name=name)

@app.route('/<command>')
def command(command):
  return render_template('command.html', command=command)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4000')
