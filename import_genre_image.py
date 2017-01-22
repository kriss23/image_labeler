# -*- coding: UTF-8 -*-
#!/bin/python

import argparse
import subprocess
import os.path

import sys
reload(sys)
sys.setdefaultencoding('utf8')

IMAGE_URL = "http://portal.deutschemailbox.de/dmb/medianet/image.php?resolution=2&sidnr=%i"
USERNAME = "mixd3bild"
PASSWORD = "7cp9UKrj"
OUTPUT_RESOLUTION = "852x480"

def label_image(broadcastID, mainGenreString, subGenreString):
	image_url = IMAGE_URL % int(broadcastID)

	print "downloading image from:" + image_url
	# generate unitque filename for tmp file
	output_filename = mainGenreString + "_" + subGenreString + ".jpg"

	if not os.path.exists(output_filename):
		subprocess_call_list = [
			"wget",
			"--user=" + USERNAME,
			"--password=" + PASSWORD,
			image_url,
			"--output-document=" + output_filename
		]
		print "Calling Subprocess for Image Download:", subprocess_call_list
		subprocess.call(subprocess_call_list)

		# #### convert image to target resolution ####
		subprocess_call_list = [
			'convert',
			output_filename,
			"-resize",
			OUTPUT_RESOLUTION,
			output_filename
		]
		# scale image to fit required resolution for our webpage
		print "Calling Subprocess for Image Conversion", subprocess_call_list
		subprocess.call(subprocess_call_list)
	# the image should be there now

	print "Done. Image rendered can be found on: http://images.mixd.tv/images/852/" + output_filename,

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--broadcastID', help='Broadcast ID - to get the right Image for it')
	parser.add_argument('--mainGenreString', help='Main Genre to identify image')
	parser.add_argument('--subGenreString', help='Sub Genre to identify image')

	args = parser.parse_args()
	label_image(args.broadcastID, args.mainGenreString, args.subGenreString)
