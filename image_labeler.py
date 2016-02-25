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
    filename = str(time.time()).replace(".", "") + ".jpg"
    imput_filename = image_title.lower().replace(" ", "_") + "_" + uuid + ".jpg"
    output_filename = image_title.lower().replace(" ", "_") + "_" + uuid + ".jpg"
    urllib.urlretrieve (image_url, "tmp/" + imput_filename)

    # scale image to fit required resolution for our webpage
    subprocess.call(['convert', "tmp/" + imput_filename, "-resize", RESOLUTION, "/var/www/html/336/" + output_filename])
    # TODO - use this to make multithread proof:
    # , "tmp/" + filename.replace(".jpg", "_small.jpg")])
    print "CALLED:", ['convert', "tmp/" + imput_filename, "-resize", RESOLUTION, "/var/www/html/336/" + output_filename]

    with open("/var/www/html/render/image.html", "wt") as fout:
        # TODO - fix this to make multithread proof:
        with open("webpage/image.html", "rt") as fin:
            for line in fin:
                fout.write(line.replace('{{IMAGE_TITLE}}', image_title))

    # render output image
    subprocess.call([PHANTOMJS_BIN,
                     "labelImage.js",
                     "http://images.mixd.tv/render/image.html",
                     "/var/www/html/336/" + output_filename,
                     "600px*336px"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to dowload image from')
    parser.add_argument('--title', help='Title to put on the image')
    parser.add_argument('--uuid', help='UUID to name the image')
    # parser.add_argument('--restore', action='store_true', default=False, help='Restore from last Backup')
    args = parser.parse_args()
    label_image(args.url, args.title, args.uuid)
