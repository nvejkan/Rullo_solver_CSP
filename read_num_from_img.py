# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:01:35 2018

@author: Nattawut Vejkanchana
"""


from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

#load
img = Image.open("rullo_8.png")
img = img.convert("RGB")

#zoom
basewidth = 5000
img = Image.open("rullo_8.png")
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))

img = img.resize((basewidth, hsize), Image.ANTIALIAS)
 
#change color
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
crop_img = img.crop((0, h, width, h*2))

#crop again
w = int(width/8)
crop_img2 = img.crop((w+200, h+100, w*2-100, h*2-100))

#read
print(pytesseract.image_to_string(crop_img, config='-psm 6'))
crop_img.save("small_crop.png", "PNG")

crop_img2 = Image.open("small_crop.png")

#all digits

print(pytesseract.image_to_string(img, config='-psm 6'))
