# Himanshu Moliya, Rahul Rachh
# hackthon : Aadhar card data minimization
# this file is use for restor data from image
import cv2

imagename = input("Enter name of Encoded image file ?(.bmp or .png) ")
# Try to restore the message from image.
img = cv2.imread(imagename, cv2.IMREAD_GRAYSCALE)
i = 0
bits = ''
chars = []
for row in img:
    for pixel in row:
        bits = str(pixel & 0x01) + bits
        i += 1
        if(i == 8):
            chars.append(chr(int(bits, 2)))
            i = 0
            bits = ''
print(''.join(chars))


