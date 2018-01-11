# coding=utf-8
from PIL import Image
from utility import *
import colorsys

def do():
    listdir = os.listdir(DATAPATH)
    imageList = [f for f in listdir if isImage(f)]
    dtList = [f for f in listdir if isData(f, ".ch")]
    for f in imageList:
        try:
            dtList.index(f + '.ch')
        except:
            print f
            createData(f)

def createData(filename):
    img = Image.open(DATAPATH + filename)
    pixel = img.load()
    width, height = img.size
    hsvArr = doColorHistogram(pixel, width, height)


    f = open(DATAPATH + filename+".ch", "w")
    for i in hsvArr:
        print>>f, str(i)
    f.close()

def doColorHistogram(pixel, width, height, xStart=0, yStart=0):
    hArr = [0]*360
    sArr = [0]*101
    vArr = [0]*101
    print "info:", width, height, xStart, yStart
    pixArr = [pixel[x+xStart, y+yStart] for x in xrange(width) for y in xrange(height)]
    hsvArr = [colorsys.rgb_to_hsv(item[0]/255., item[1]/255., item[2]/255.) for item in pixArr]

    for item in hsvArr:
        hAdjust = int(item[0]*360+0.5)
        if hAdjust == 360:
            hAdjust = 0
        hArr[hAdjust] += 1
        sArr[int(item[1]*100+0.5)] += 1
        vArr[int(item[2]*100+0.5)] += 1

    return hArr+sArr+vArr

