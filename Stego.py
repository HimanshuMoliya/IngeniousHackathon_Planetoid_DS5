import cv2

def bitgenerator(message):
    for k in (message):
        p = ord(k)
        for i in range(8):
            yield (p & (1 << i)) >> i

# design a generator for the hidden message
hidden_message = bitgenerator(open("info.txt", "r").read() * 10) 

# Read original image
img = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)

for h in range(len(img)):
    for w in range(len(img[0])):
        # Write the hidden message -->the least significant bit
        img[h][w] = (img[h][w] & ~1) | next(hidden_message)

# Write out the image with hidden message
cv2.imwrite("output.png", img)
