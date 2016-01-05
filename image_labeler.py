#!/bin/python

import urllib
import argparse
import time
import subprocess

RESOLUTION = "600x336"
PHANTOMJS_BIN = "./install/phantomjs/bin/phantomjs"

def label_image(image_url):
    print "downloading image from:", image_url
    # generate unitque filename for tmp file
    filename = str(time.time()).replace(".", "") + ".jpg"
    urllib.urlretrieve (image_url, "tmp/" + filename)

    # scale image to fit required resolution for our webpage
    subprocess.call(['convert', "tmp/" + filename, "-resize", RESOLUTION, "/var/www/html/render/image.jpg"])
    # TODO - use this to make multithread proof:
    # , "tmp/" + filename.replace(".jpg", "_small.jpg")])
    print "CALLED:", ['convert', "tmp/" + filename, "-resize", RESOLUTION, "/var/www/html/render/image.jpg"]

    # render output image
    subprocess.call([PHANTOMJS_BIN,
                     "labelImage.js",
                     "http://images.mixd.tv/render/image.html",
                     "/var/www/html/render/test_out.jpg",
                     "600px*336px"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to dowload image from')
    # parser.add_argument('--restore', action='store_true', default=False, help='Restore from last Backup')
    args = parser.parse_args()
    label_image(args.url)
