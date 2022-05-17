

import PIL
import os, sys
from PIL import Image
def load_text(infile):
    allimgs=[]
    with Image.open(infile) as im:
        im.convert('RGB')

        for x in range(6):
            for y in range(19):
                box = (x*64, y*64, x*64+64, y*64+64)

                allimgs.append(im.crop(box))
    return allimgs

def load_objs(infile):
    allimgs=[]
    with Image.open(infile) as im:
        im.convert('RGB')

        for w in range(8):
            for h  in range(5):
                x = w*128 + w
                y = h*128 + h
                box = (x, y, x+128, y+128)

                allimgs.append(im.crop(box))

                im.crop(box).save(f"{x}_{y}.png")
    return allimgs



load_objs("Z0Eplzj.png")