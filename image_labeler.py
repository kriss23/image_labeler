#!/bin/python

import urllib
import argparse
import time

def label_image(image_url):
    print "downloading image from:", image_url
    # generate unitque filename for tmp file
    filename = str(time.time()).replace(".", "") + ".jpg"
    urllib.urlretrieve (image_url, "tmp/" + filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='URL to dowload image from')
    # parser.add_argument('--restore', action='store_true', default=False, help='Restore from last Backup')
    args = parser.parse_args()
    label_image(args.url)
