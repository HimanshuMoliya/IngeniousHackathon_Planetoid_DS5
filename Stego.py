# Himanshu Moliya,Rahul Rachh
# hackthon : Aadhar card data minimization 

import cv2
from __future__ import absolute_import, unicode_literals
import random, sys
from PIL import Image

BIT = 8

def pixel_normalization(r, g, b):
    if is_pixel_modification(r, g, b):
        seed = random.randint(1, 3)
        if seed == 1:
            r = _normalize(r)
        if seed == 2:
            g = _normalize(g)
        if seed == 3:
            b = _normalize(b)
    return r, g, b

def is_pixel_modification(r, g, b):
    return r % BIT == g % BIT == b % BIT == 1

def _normalize(i):
    if i >= 128:
        i -= 1
    else:
        i += 1
    return i

def bitgenerator(message):
    for k in (message):
        p = ord(k)
        for i in range(8):
            yield (p & (1 << i)) >> i

# design a generator for the hidden message
filename = input("Enter name of your details file ? ")
hidden_message = bitgenerator(open(filename, "r").read() * 10) 
imagename = input("Enter name of image file ?(.bmp or .png) ")
# Read original image
img = cv2.imread(imagename, cv2.IMREAD_GRAYSCALE)

for h in range(len(img)):
    for w in range(len(img[0])):
        # Write the hidden message -->the least significant bit
        img[h][w] = (img[h][w] & ~1) | next(hidden_message)

# Write out the image with hidden message
cv2.imwrite("out"+imagename, img)
print("please find output file")
