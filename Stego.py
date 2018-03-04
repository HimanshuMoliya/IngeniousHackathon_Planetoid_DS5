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

def pixel_modification(r, g, b):
    return map(_modify, [r, g, b])

def is_pixel_modification(r, g, b):
    return r % BIT == g % BIT == b % BIT == 1

def _normalize(i):
    if i >= 128:
        i -= 1
    else:
        i += 1
    return i


def normalize(path, output):
 
    img = Image.open(path)
    img = img.convert('RGB')
    size = img.size
    new_img = Image.new('RGB', size)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            _r, _g, _b = pixel_normalization(r, g, b)
            new_img.putpixel((x, y), (_r, _g, _b))
    new_img.save(output, "PNG", optimize=True)

def _modify(i):
    if i >= 128:
        for x in xrange(BIT + 1):
            if i % BIT == 1:
                return i
            i -= 1
    else:
        for x in xrange(BIT + 1):
            if i % BIT == 1:
                return i
            i += 1
    raise ValueError
    

def hide_text(path, text):
    text = str(text)

    # convert text to hex for write
    write_param = []
    _base = 0
    for _ in to_hex(text):
        write_param.append(int(_, 16) + _base)
        _base += 16

    # hide hex-text to image
    img = Image.open(path)
    count = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if count in write_param:
                r, g, b = img.getpixel((x, y))
                r, g, b = pixel_modification(r, g, b)
                img.putpixel((x, y), (r, g, b))
            count += 1

    
def to_hex(s):
    return s.encode("hex")


def to_str(s):
    return s.decode("hex")

    
 def encode(cls, input_img_path, output_img_path, filedata,ext):
        normalize(input_img_path, output_img_path,ext)
        text_hide(output_img_path, filedata, ext)
        assert text_read(output_img_path) == filedata, text_read(output_img_path)
        
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
