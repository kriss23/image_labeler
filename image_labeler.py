#!/bin/python

import urllib
import argparse
import time
import subprocess

RESOLUTION = "600x336"
PHANTOMJS_BIN = "/home/ubuntu/install/phantomjs/bin/phantomjs"

def label_image(image_url, image_title, uuid):
    print "downloading image from:", image_url
    # generate unitque filename for tmp file
    input_filename = image_title.lower().replace(" ", "_") + "_" + uuid + ".jpg"
    output_filename = image_title.lower().replace(" ", "_") + "_" + uuid + ".jpg"
    urllib.urlretrieve (image_url, "/var/www/html/images/tmp/" + input_filename)

    # scale image to fit required resolution for our webpage
    subprocess.call(['convert', "/var/www/html/images/tmp/" + input_filename, "-resize", RESOLUTION, "/var/www/html/images/tmp/" + output_filename])
    # TODO - use this to make multithread proof:
    # , "tmp/" + filename.replace(".jpg", "_small.jpg")])
    print "CALLED:", ['convert', "/var/www/html/images/tmp/" + input_filename, "-resize", RESOLUTION, "/var/www/html/images/tmp/" + output_filename]

    with open("/var/www/html/render/image_" + uuid + ".html", "wt") as fout:
        with open("webpage/image.html", "rt") as fin:
            for line in fin:
                # Apply templating:
                if "{{IMAGE_TITLE}}" in line:
                    line = line.replace('{{IMAGE_TITLE}}', image_title)
                if '{{IMAGE_FILE}}' in line:
                    line = line.replace('{{IMAGE_FILE}}', "http://images.mixd.tv/images/tmp/" + input_filename)
                fout.write(line)

    # render output image
    subprocess.call([PHANTOMJS_BIN,
                     "labelImage.js",
                     "http://images.mixd.tv/render/image_" + uuid + ".html",
                     "/var/www/html/images/336/" + output_filename,
                     "600px*336px"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to dowload image from')
    parser.add_argument('--title', help='Title to put on the image')
    parser.add_argument('--uuid', help='UUID to name the image')
    # parser.add_argument('--restore', action='store_true', default=False, help='Restore from last Backup')
    args = parser.parse_args()
    label_image(args.url, args.title, args.uuid)
