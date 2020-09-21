#!/usr/bin/env python3

import os
import requests
import time

folder = 'downloads'
num_images = 500

if not os.path.exists(folder):
    os.makedirs(folder)

url = "https://www.e-zpassny.com/vector/jcaptcha.do"
total = 0

for i in range(0, num_images):
    try:
        r = requests.get(url, timeout=60)
        p = "{}/{}.jpg".format(folder, str(total).zfill(5))
        f = open(p, "wb")
        f.write(r.content)
        f.close()
        print("downloaded: {}".format(p))
        total += 1
    except:
        print("error downloading image...")
    time.sleep(0.1)
