"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import picamera
import json
import MySQLdb
from subprocess import call
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

scores = list()
descriptions = list()

def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')

def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)

    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })
        response = service_request.execute()

        for e in response["responses"][0]["labelAnnotations"]:
			scores.append(e["score"])
			descriptions.append(e["description"])
			
	for i in scores:
		print i
		
	query = "SELECT * FROM song_lyrics WHERE lyrics LIKE '%" + descriptions[0] + "%'"
	print descriptions[0]
	for i in range(1, len(descriptions)):
		query = query + " or lyrics LIKE '%" + descriptions[i] + "%'"
		print descriptions[i]

	db = MySQLdb.connect("localhost", "root", "root", "music")
	curs=db.cursor()

	print query

	curs.execute (query)

	print curs._last_executed

	for reading in curs.fetchall():
		print str(reading[0])+"	"+str(reading[1])+" 	"+str(reading[2])
		file_path = "./songs/"
		file_path+=str(reading[2])
		call(["omxplayer", "-o", "both", file_path])
		break

	"""./songs/50_Cent_In_Da_Club_Dirty.mp3"""

if __name__ == '__main__':

    main()
