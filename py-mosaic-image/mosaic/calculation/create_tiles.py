# coding=utf-
import os
from PIL import Image
from utility import *


def do():
    listdir = os.listdir(DATAPATH)
    imageList = [f for f in listdir if isImage(f)]
    dtList = [f for f in listdir if isData(f)]
    for f in imageList:
        if noData(f, dtList):
            print f
            createData(f)

def createData(filename):
    img = Image.open(DATAPATH + filename).convert('YCbCr')
    pixel = img.load()
    width, height = img.size
    data = doColorLayout(pixel, width, height)


    text = open(DATAPATH + filename + ".dt", "w")
    for item in data:
        print>>text, ' '.join(str(e) for e in item)
    text.close()




if __name__=="__main__":
    do()