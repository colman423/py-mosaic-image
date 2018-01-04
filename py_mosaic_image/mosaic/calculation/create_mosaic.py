# coding=utf-8
from PIL import Image

import create_tiles
from utility import *
from io import BytesIO
import base64
import time

progress = {
    'state': 0,
    'content': 0
}
def getprogress():
    print "getpro", str(progress)

def load(img, grid):
    global progress

    # ===== load image =====
    progress['state'] = 0
    progress['content'] = 0
    imgName = str(int(time.time()))
    img.save(DATAPATH + "..\\public\\input\\"+imgName+".jpg")
    pixel = img.load()
    print "pixel"
    width, height = img.size
    blockW, blockH = width/grid, height/grid

    # ===== cutting image =====
    progress['state'] += 1
    progress['content'] = 0

    colorLayoutData = [None]*(grid*grid)
    for i in xrange(grid*grid):
        w = (int)(i%grid)
        h = (int)(i/grid)
        # print w, h
        colorLayoutData[i] = doColorLayout(pixel, blockW, blockH, blockW*w, blockH*h)
        progress['content'] = 100*i/(grid*grid)


    # ===== finding tiles =====
    progress['state'] += 1
    progress['content'] = 0
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

            progress['content'] = int(100*float(i)/datacount)


    # ===== assembling new image =====
    progress['state'] += 1
    progress['content'] = 0
    for i in xrange(grid*grid):
        tile = tiles[i]
        # print "tiles[{0}] = {1}".format(i, tile)
        block = Image.open(DATAPATH + tile).convert('YCbCr')
        block = block.resize((blockW, blockH))
        img.paste(block, (blockW*(i%grid), blockH*(i/grid)))
        progress['content'] = 100*i/(grid*grid)

    img.save(DATAPATH + "..\\public\\output\\"+imgName+".jpg")

    # ===== complete =====
    progress['state'] += 1
    progress['content'] = imgName+".jpg"

    # response = HttpResponse(content_type="image/jpeg")
    # img.save(response, 'JPEG')
    #
    # progress = response  # and we're done!

def create(file, grid):
    print "create"
    img = Image.open(BytesIO(base64.b64decode(file))).convert('YCbCr')
    print "image"
    load(img, grid)


if __name__ == "__main__":
    create_tiles.do()
    # img = Image.open(DATAPATH + "..\\test.png").convert('YCbCr')
    # load(img, 80)

