# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 14:06:10 2018

@author: Nattawut Vejkanchana
"""

from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


img = Image.open("rullo_8.png")
img = img.convert("RGB")

img = Image.open('rullo_8.png').convert('LA')
img.save('greyscale.png')

pixdata = img.load()

width, height = img.size
for y in range(height):
    for x in range(width):
        if (pixdata[x, y][0] >= 100 and pixdata[x, y][1] >= 100 and pixdata[x, y][2] >= 100):
            pixdata[x, y] = (0, 0, 0)
        else:
            pixdata[x, y] = (255, 255, 255)

#crop
h = int(height/8)
crop_img = img.crop((0, 0, width, h))

crop_img.save("8_crop.png", "PNG")
img.save("8_converted.png", "PNG")
img = Image.open("8_converted.png")
img = Image.open("15.png")

print(pytesseract.image_to_string(img))
print(pytesseract.image_to_string(crop_img))



basewidth = 5000
img = Image.open("rullo_8.png")
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))

img = img.resize((basewidth, hsize), Image.ANTIALIAS)

img.save("8_converted.png", "PNG")
