# coding=utf-8
from PIL import Image

import create_tiles
from utility import *
from io import BytesIO
import base64
import cStringIO

progress = 0

def load(img, grid):
    global progress
    progress = 0

    pixel = img.load()
    print "pixel"
    width, height = img.size
    blockW, blockH = width/grid, height/grid

    colorLayoutData = [None]*(grid*grid)
    for i in xrange(grid*grid):
        w = (int)(i%grid)
        h = (int)(i/grid)
        print w, h
        colorLayoutData[i] = doColorLayout(pixel, blockW, blockH, blockW*w, blockH*h)


    colorDis = [-1]*(grid*grid)
    tiles = [None]*(grid*grid)

    try:
        print os.listdir(DATAPATH)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


    for filename in os.listdir(DATAPATH):
        if(isData(filename)):
            print filename
            with open(DATAPATH + filename) as f:
                progress += 0.08
                print progress
                compareData = [item.split(' ') for item in f.read().splitlines()]
                f.close()
                compareYArr = [float(i[0]) for i in compareData]
                compareCbArr = [float(i[1])  for i in compareData]
                compareCrArr = [float(i[2])  for i in compareData]

                for i in xrange(len(colorLayoutData)):
                    data = colorLayoutData[i]
                    yArr = [item[0] for item in data]
                    cbArr = [item[1] for item in data]
                    crArr = [item[2] for item in data]

                    distance = np.linalg.norm(np.array(yArr) - np.array(compareYArr))\
                               + np.linalg.norm(np.array(cbArr) - np.array(compareCbArr))\
                               + np.linalg.norm(np.array(crArr) - np.array(compareCrArr))
                    if distance < colorDis[i] or colorDis[i] == -1:
                        colorDis[i] = distance
                        tiles[i] = filename[:-3]

    for i in xrange(grid*grid):
        progress += 1
        tile = tiles[i]
        print "tiles[{0}] = {1}".format(i, tile)
        block = Image.open(DATAPATH + tile).convert('YCbCr')
        block = block.resize((blockW, blockH))
        img.paste(block, (blockW*(i%grid), blockH*(i/grid)))

    img.save(DATAPATH + "..\\abc.jpg")

    buffer = cStringIO.StringIO()
    img.save(buffer, format="JPEG")
    progress = base64.b64encode(buffer.getvalue())

def create(file, grid):
    print "create"
    data = {}
    data['img'] = file
    print "data"
    img = Image.open(BytesIO(base64.b64decode(data['img']))).convert('YCbCr')
    print "image"
    load(img, grid)


if __name__ == "__main__":
    create_tiles.do()
    # img = Image.open(DATAPATH + "..\\test.png").convert('YCbCr')
    # load(img, 80)

