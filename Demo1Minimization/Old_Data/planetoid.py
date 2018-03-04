#python2 steganography.py -e lena.jpg output.jpg 'The quick brown fox jumps over the lazy dog.'
#python2 steganography.py -d output.jpg

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

def pixel_modification(r, g, b):
    return map(_modify, [r, g, b])

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


def _normalize(i):
    if i >= 128:
        i -= 1
    else:
        i += 1
    return i

def normalize(path, output, ext):
 
    img = Image.open(path)
    img = img.convert('RGB')
    size = img.size
    new_img = Image.new('RGB', size)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            _r, _g, _b = pixel_normalization(r, g, b)
            new_img.putpixel((x, y), (_r, _g, _b))
    new_img.save(output, ext , optimize=True)


def text_hide(path, text, ext):
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
    # save
    img.save(path, ext ,optimize=True)

def text_read(path):
    img = Image.open(path)
    count = 0
    result = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = img.getpixel((x, y))
            if is_pixel_modification(r, g, b):
                result.append(count)
            count += 1
            if count == 16:
                count = 0
    return to_str(''.join([hex(_)[-1:] for _ in result]))


def to_hex(h):
    return h.encode("hex")


def to_str(h):
    return h.decode("hex")

class Steganography(object):
    @classmethod
    def encode(cls, input_img_path, output_img_path, filedata,ext):
        normalize(input_img_path, output_img_path,ext)
        text_hide(output_img_path, filedata, ext)
        assert text_read(output_img_path) == filedata, text_read(output_img_path)

    @classmethod
    def decode(cls, image_path):
        return text_read(image_path)


# Main program
def main():
    if len(sys.argv) == 5 and sys.argv[1] == '-e':
        # encode
        print("Start Encoding")
        input_img_path = sys.argv[2]    #input file name
        output_img_path = sys.argv[3]   #output file name
        textfile = sys.argv[4]          #text data file(details file)
        
        EXT = input_img_path[-3:]       #detect extension
        print "File Detected : " + EXT
        ext = ("BMP" if (EXT == "bmp") else "PNG" if (EXT == "png") else "PNG")         # all other format(tiff,gif,jpeg) file converted into png after storing data. 
        Steganography.encode(input_img_path, output_img_path, open(textfile, "r").read(),ext)
        print("Finish:{}".format(output_img_path))
        return
    if len(sys.argv) == 3 and sys.argv[1] == '-d' :
        # decode
        input_img_path = sys.argv[2]
        print(Steganography.decode(input_img_path))
        return
if __name__ == "__main__":
    main()
