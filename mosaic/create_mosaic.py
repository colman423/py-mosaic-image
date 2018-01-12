# coding=utf-8
from PIL import Image
from calculation.utility import *
from calculation.color_layout import doColorLayout
from calculation.color_histogram import doColorHistogram
from io import BytesIO
import base64
from threading import Thread
import time
import numpy as np


procedureList = []
COLOR_LAYOUT = "color layout"
COLOR_HISTOGRAM = "color histogram"

class createMosaic(Thread):
    file = None
    grid = 10
    method = ""
    uid = ""
    state = 0
    content = 0


    def __init__(self, file, grid, method=COLOR_HISTOGRAM):
        super(createMosaic, self).__init__()
        self.file = file
        self.grid = grid
        self.method = method
        self.uid = str(int(time.time()))

    def getUid(self):
        return self.uid

    def getProgress(self):
        return {'state': self.state, 'content': self.content, 'uid': self.uid}

    def sameUid(self, uid):
        return self.uid==uid

    def run(self):
        self.create()

    def create(self):
        print "create new image"
        img = Image.open(BytesIO(base64.b64decode(self.file)))
        print "image loaded success"
        if self.method==COLOR_LAYOUT:
            self.colorLayout(img)
        elif self.method==COLOR_HISTOGRAM:
            self.colorHistogram(img)


    def colorHistogram(self, img):
        grid = self.grid

        # ===== load image =====
        self.state = 0
        self.content = 50
        img.save(DATAPATH + "../public/input/"+self.uid+".png")
        pixel = img.load()
        print "pixel loaded success"
        width, height = img.size
        blockW, blockH = int(round(width/float(grid))), int((height/float(grid)))


        # ===== cutting image =====
        self.state += 1
        self.content = 0

        imgData = [None for i in xrange(pow(grid,2))]
        for i in xrange(grid*grid):
            w = (int)(i%grid)
            h = (int)(i/grid)
            # print w, h
            data = doColorHistogram(pixel, blockW, blockH, width*w/grid, height*h/grid)
            imgData[i] = data
            self.content = 100*i/(grid*grid)


        # ===== finding tiles =====
        self.state += 1
        self.content = 0

        colorDis = [-1 for i in range(pow(grid,2))]
        tiles = [None for i in range(pow(grid,2))]

        filedata = [f for f in os.listdir(DATAPATH) if isData(f, ".ch")]
        datacount = len(filedata)
        for i in xrange(datacount):
            filename = filedata[i]

            with open(DATAPATH + filename) as f:
                print "comparing file "+filename
                compareData = [int(item) for item in f.read().splitlines()]
                f.close()
                # print len(np.array(compareData))

                for j in xrange(grid*grid):
                    # print len(imgData[j])
                    # combine = [abs(item[0] - item[1]) for item in zip(np.array(compareData), imgData[j])]
                    # print imgData[j]
                    combine = map(lambda x: abs(x[0] - x[1]), zip(compareData, imgData[j]))
                    for y in xrange(360):
                        if combine[y] > 180:
                            combine[y] = (360 - combine[y]) * 2
                        else:
                            combine[y] *= 2
                    for y in range(360, 460):
                        combine[y] = combine[y] / 2
                    distance = np.linalg.norm(combine)
                    print j, distance

                    if distance < colorDis[j] or colorDis[j] == -1:
                        colorDis[j] = distance
                        tiles[j] = filename[:-3]

                self.content = int(100*float(i)/datacount)

        # ===== assembling new image =====
        self.state += 1
        self.content = 0

        for i in xrange(grid * grid):
            tile = tiles[i]
            # print "tiles[{0}] = {1}".format(i, tile)
            block = Image.open(DATAPATH + tile)
            block = block.resize((blockW, blockH))
            img.paste(block, (blockW * (i % grid), blockH * (i / grid)))
            self.content = 100 * i / (grid * grid)

        img.save(DATAPATH + "../public/output/" + self.uid + ".png")

        # ===== complete =====
        self.content = self.uid + ".png"
        self.state += 1

    def colorLayout(self, img):
        grid = self.grid

        # ===== load image =====
        self.state = 0
        self.content = 0
        img.save(DATAPATH + "../public/input/"+self.uid+".png")
        pixel = img.load()
        print "pixel loaded success"
        width, height = img.size
        blockW, blockH = int(round(width/float(grid))), int((height/float(grid)))


        # ===== cutting image =====
        self.state += 1
        self.content = 0

        dataY = [None for i in range(pow(grid,2))]
        dataCb = [None for i in range(pow(grid,2))]
        dataCr = [None for i in range(pow(grid,2))]
        for i in xrange(grid*grid):
            w = (int)(i%grid)
            h = (int)(i/grid)
            # print w, h
            dataY[i], dataCb[i], dataCr[i] = doColorLayout(pixel, blockW, blockH, blockW*w, blockH*h)
            self.content = 100*i/(grid*grid)


        # ===== finding tiles =====
        self.state += 1
        self.content = 0

        colorDis = [-1 for i in range(pow(grid,2))]
        tiles = [None for i in range(pow(grid,2))]

        filedata = [f for f in os.listdir(DATAPATH) if isData(f, ".cl")]
        datacount = len(filedata)
        for i in xrange(datacount):
            filename = filedata[i]
            # print filename

            with open(DATAPATH + filename) as f:
                print "comparing file "+filename
                compareData = [item.split(' ') for item in f.read().splitlines()]
                f.close()
                compY = [float(j[0]) for j in compareData]
                compCb = [float(j[1]) for j in compareData]
                compCr = [float(j[2]) for j in compareData]

                for j in xrange(grid*grid):
                    imgY, imgCb, imgCr = dataY[j], dataCb[j], dataCr[j]

                    disY = [pow(imgY[k]-compY[k], 2) for k in xrange(64)]
                    disCb = [pow(imgCb[k]-compCb[k], 2) for k in xrange(64)]
                    disCr = [pow(imgCr[k]-compCr[k], 2) for k in xrange(64)]

                    distance = pow(sum(disY), 0.5) + pow(sum(disCb), 0.5) + pow(sum(disCr), 0.5)

                    if distance < colorDis[j] or colorDis[j] == -1:
                        colorDis[j] = distance
                        tiles[j] = filename[:-3]

                self.content = int(100*float(i)/datacount)


        # ===== assembling new image =====
        self.state += 1
        self.content = 0

        for i in xrange(grid*grid):
            tile = tiles[i]
            # print "tiles[{0}] = {1}".format(i, tile)
            block = Image.open(DATAPATH + tile).convert('YCbCr')
            block = block.resize((blockW, blockH))
            img.paste(block, (blockW*(i%grid), blockH*(i/grid)))
            self.content = 100*i/(grid*grid)

        img.save(DATAPATH + "../public/output/"+self.uid+".png")

        # ===== complete =====
        self.content = self.uid+".png"
        self.state += 1



if __name__ == "__main__":

    newProcedure = createMosaic("../dataset/ukbench00000.jpg", 10)
    # img = Image.open(DATAPATH + "..\\test.png").convert('YCbCr')
    # load(img, 80)
