# coding=utf-8
from utility import *
from PIL import Image
import create_tiles

def load(filename, grid):
    img = Image.open(filename).convert('YCbCr')
    pixel = img.load()
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

    for filename in os.listdir(DATAPATH):
        if(isData(filename)):
            print filename
            with open(DATAPATH + filename) as f:
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
        tile = tiles[i]
        print "tiles[{0}] = {1}".format(i, tile)
        block = Image.open(DATAPATH + tile).convert('YCbCr')
        block = block.resize((blockW, blockH))
        img.paste(block, (blockW*(i%grid), blockH*(i/grid)))

    img.save(DATAPATH + "..\\abc.jpg")


if __name__ == "__main__":
    create_tiles.do()
    load(DATAPATH + "..\\test.png", 80)
