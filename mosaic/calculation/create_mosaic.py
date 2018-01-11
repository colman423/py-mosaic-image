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
        pass

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
        blockW, blockH = width/grid, height/grid


        # ===== cutting image =====
        self.state += 1
        self.content = 0

        colorLayoutData = [None]*(grid*grid)
        for i in xrange(grid*grid):
            w = (int)(i%grid)
            h = (int)(i/grid)
            # print w, h
            colorLayoutData[i] = doColorLayout(pixel, blockW, blockH, blockW*w, blockH*h)
            self.content = 100*i/(grid*grid)


        # ===== finding tiles =====
        self.state += 1
        self.content = 0

        colorDis = [-1]*(grid*grid)
        tiles = [None]*(grid*grid)

        filedata = [f for f in os.listdir(DATAPATH) if isData(f)]
        datacount = len(filedata)
        for i in xrange(datacount):
            filename = filedata[i]
            # print filename

            with open(DATAPATH + filename) as f:
                compareData = [item.split(' ') for item in f.read().splitlines()]
                f.close()
                compareYArr = [float(j[0]) for j in compareData]
                compareCbArr = [float(j[1]) for j in compareData]
                compareCrArr = [float(j[2]) for j in compareData]

                for j in xrange(len(colorLayoutData)):
                    data = colorLayoutData[j]
                    yArr = [item[0] for item in data]
                    cbArr = [item[1] for item in data]
                    crArr = [item[2] for item in data]

                    distance = np.linalg.norm(np.array(yArr) - np.array(compareYArr))\
                               + np.linalg.norm(np.array(cbArr) - np.array(compareCbArr))\
                               + np.linalg.norm(np.array(crArr) - np.array(compareCrArr))
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
        # create_tiles.do()
        print "create new image"
        img = Image.open(BytesIO(base64.b64decode(self.file))).convert('YCbCr')
        print "image loaded success"
        self.load(img)


if __name__ == "__main__":
    create_tiles.do()
    # img = Image.open(DATAPATH + "..\\test.png").convert('YCbCr')
    # load(img, 80)
