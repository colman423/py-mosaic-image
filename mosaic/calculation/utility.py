# coding=UTF-8
import os
import scipy.fftpack
import numpy as np

MULTIPLE = 3
DATAPATH = os.getcwd() + "/dataset/"

def isImage(f):
    return f.endswith('.jpg') or f.endswith('.png') or f.endswith('.bmp') or f.endswith('.gif')

def isData(f):
    return f.endswith('.dt')

def noData(f, list):
    try:
        list.index(f+'.dt')
        return False
    except:
        return True

def convertZigzac(arr):
    convert = [0, 1, 8, 16, 9, 2, 3, 10,
               17, 24, 32, 25, 18, 11, 4, 5,
               12, 19, 26, 33, 40, 48, 41, 34,
               27, 20, 13, 6, 7, 14, 21, 28,
               35, 42, 49, 56, 57, 50, 43, 36,
               29, 22, 15, 23, 30, 37, 44, 51,
               58, 59, 52, 45, 38, 31, 39, 46,
               53, 60, 61, 54, 47, 55, 62, 63]
    newArr = [None]*64
    for i in xrange(len(convert)):
        newArr[i] = arr[convert[i]]

    return newArr

def doColorLayout(pixel, width, height, xStart=0, yStart=0):
    blockW, blockH = width/8, height/8
    mosaicArr = []
    for yCount in xrange(8):
        for xCount in xrange(8):
            colArr = []
            countArr = []
            left, right = blockW*xCount, blockW*(xCount+1)
            top, bottom = blockH*yCount, blockH*(yCount+1)
            for x in range(left, right, 1):
                for y in range(top, bottom, 1):
                    tmp = pixel[x+xStart, y+yStart]
                    colArr.append(tmp)
                    countArr.append(tmp[0]+tmp[1]+tmp[2])

            median = len(countArr)/2
            colIndex = np.argsort(countArr)[median]
            mosaicArr.append(colArr[colIndex])
    # mosaicArr = convertZigzac(mosaicArr)
    dctResult = scipy.fftpack.dct(mosaicArr)

    return convertZigzac(dctResult)
