# coding=UTF-8
import os
import scipy.fftpack as fft
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

# def convertZigzac(arr):
#     convert = [0, 1, 8, 16, 9, 2, 3, 10,
#                17, 24, 32, 25, 18, 11, 4, 5,
#                12, 19, 26, 33, 40, 48, 41, 34,
#                27, 20, 13, 6, 7, 14, 21, 28,
#                35, 42, 49, 56, 57, 50, 43, 36,
#                29, 22, 15, 23, 30, 37, 44, 51,
#                58, 59, 52, 45, 38, 31, 39, 46,
#                53, 60, 61, 54, 47, 55, 62, 63]
#     newArr = [None]*64
#     for i in xrange(len(convert)):
#         newArr[i] = arr[convert[i]]
#
#     return newArr

def convertZigzac(arr):
    convert = [[0, 1, 5, 6, 14, 15, 27, 28],
            [2, 4, 7, 13, 16, 26, 29, 42],
            [3, 8, 12, 17, 25, 30, 41, 43],
            [9, 11, 18, 24, 31, 40, 44, 53],
            [10, 19, 23, 32, 39, 45, 52, 54],
            [20, 22, 33, 38, 46, 51, 55, 60],
            [21, 34, 37, 47, 50, 56, 59, 61],
            [35, 36, 48, 49, 57, 58, 62, 63]]
    data=[None]*64
    for i in xrange(8):
        for j in xrange(8):
            data[convert[i][j]] = arr[i][j]
    # print "convertEnd"
    # print data
    return data

def doColorLayout(pixel, width, height, xStart=0, yStart=0):
    # print "start doing color layout!, x, y start = ", xStart, yStart
    blockW, blockH = width/8, height/8
    representY = [[0 for i in range(8)] for j in range(8)]
    representCb = [[0 for i in range(8)] for j in range(8)]
    representCr = [[0 for i in range(8)] for j in range(8)]
    for xBlock in xrange(8):
        for yBlock in xrange(8):
            xBase = blockW*xBlock+xStart
            yBase = blockH*yBlock+yStart
            print "block: ", xBlock, yBlock, "Base: ", xBase, yBase

            pixArr = []
            for x in xrange(blockW):
                for y in xrange(blockH):
                    try:
                        pixArr.append(pixel[x+xBase, y+yBase])
                    except:
                        pass

            # pixArr = [ pixel[x+xBase, y+yBase] for x in xrange(blockW) for y in xrange(blockH)]
            if len(pixArr)!=0:
                colR = sum([col[0] for col in pixArr]) / float(len(pixArr))
                colG = sum([col[1] for col in pixArr]) / float(len(pixArr))
                colB = sum([col[2] for col in pixArr]) / float(len(pixArr))
                print "RGB:", colR, colG, colB

                colY, colCb, colCr = _ycc(colR, colG, colB)
                representY[xBlock][yBlock] = colY
                representCb[xBlock][yBlock] = colCb
                representCr[xBlock][yBlock] = colCr
            else:
                x, y = getSide(xBlock, yBlock)
                representY[xBlock][yBlock] = representY[x][y]
                representCb[xBlock][yBlock] = representCb[x][y]
                representCr[xBlock][yBlock] = representCr[x][y]


    print "block success"
    # print representY
    # print representCb
    # print representCr

    # mosaicArr = convertZigzac(mosaicArr)
    dctY = fft.dct(representY)
    dctCb = fft.dct(representCb)
    dctCr = fft.dct(representCr)

    return convertZigzac(dctY), convertZigzac(dctCb), convertZigzac(dctCr)

def _ycc(r, g, b): # in (0,255) range
    y = .299*r + .587*g + .114*b
    cb = 128 -.168736*r -.331364*g + .5*b
    cr = 128 +.5*r - .418688*g - .081312*b
    return y, cb, cr

def getSide(x, y):
    if x==7:
        return getSide(6, y)
    elif y==7:
        return getSide(x, 6)
    else:
        return x, y