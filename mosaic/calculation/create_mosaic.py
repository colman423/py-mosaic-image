# coding=utf-8
from PIL import Image
import create_tiles
from utility import *
from io import BytesIO
import base64
from threading import Thread
import time


procedureList = []
class createMosaic(Thread):
    file = None
    grid = 10
    uid = ""
    state = 0
    content = 0
    uidCheck = ""

    def __init__(self, file, grid):
        super(createMosaic, self).__init__()
        self.file = file
        self.grid = grid
        self.uid = str(int(time.time()))
        self.uidCheck = self.uid

    def run(self):
        self.create()

    def getUid(self):
        return self.uid

    def getProgress(self):
        return {'state': self.state, 'content': self.content, 'uid': self.uid}

    def sameUid(self, uid):
        return self.uid==uid

    def load(self, img):
        grid = self.grid

        # ===== load image =====
        self.state = 0
        self.content = 0

        img.save(DATAPATH + "../public/input/"+self.uid+".jpg")
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

        filedata = [f for f in os.listdir(DATAPATH) if isData(f)]
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

                    disY, disCb, disCr = 0, 0, 0
                    for k in xrange(64):
                        compare = 1
                        # if k==0:
                        #     compare = 10
                        # elif k==1:
                        #     compare = 5
                        # elif k==2:
                        #     compare = 3
                        disY += compare * pow(imgY[k]-compY[k], 2)
                        disCb += compare * pow(imgCb[k]-compCb[k], 2)
                        disCr += compare * pow(imgCr[k] - compCr[k], 2)

                    distance = pow(disY, 0.5) + pow(disCb, 0.5) + pow(disCr, 0.5)

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

        img.save(DATAPATH + "../public/output/"+self.uid+".jpg")

        # ===== complete =====
        self.content = self.uid+".jpg"
        self.state += 1


    def create(self):
        print "create new image"
        img = Image.open(BytesIO(base64.b64decode(self.file)))
        print "image loaded success"
        self.load(img)

    def createLocal(self):
        print "create new image local"
        img = Image.open(DATAPATH+"../"+self.file).convert('YCbCr')
        print "image loaded success"
        self.load(img)


if __name__ == "__main__":

    newProcedure = createMosaic("../dataset/ukbench00000.jpg", 10)
    newProcedure.createLocal()
    # img = Image.open(DATAPATH + "..\\test.png").convert('YCbCr')
    # load(img, 80)
