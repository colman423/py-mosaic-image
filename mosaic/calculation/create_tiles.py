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
    img = Image.open(DATAPATH + filename)
    pixel = img.load()
    width, height = img.size
    dataY, dataCb, dataCr = doColorLayout(pixel, width, height)


    text = open(DATAPATH + filename + ".dt", "w")
    for i in xrange(64):
        print>>text, str(dataY[i])+' '+str(dataCb[i])+' '+str(dataCr[i])
    text.close()




if __name__=="__main__":
    do()