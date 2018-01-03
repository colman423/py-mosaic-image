# coding=UTF-8
# mosaic/views.py
from django.shortcuts import render
from django.http import HttpResponse
import mosaic.create_mosaic
from threading import Thread

class createMosaic(Thread):
    def __init__(self, file, grid):
        super(createMosaic, self).__init__()
        self.file = file
        self.grid = grid
    def run(self):
        mosaic.create_mosaic.create(self.file, self.grid)

def mosaicReq(req):
    FILE = 'file'
    WAIT = 'wait'
    print req
    print mosaic.create_mosaic.progress
    if FILE in req.POST:
        print "has file"
        file = req.POST[FILE]
        createMosaic(file, 10).start()
        print "thread over"
        print "thread over"
        print "thread over"
        progress = 0
        return HttpResponse("START")
    elif WAIT in req.POST:
        progress = mosaic.create_mosaic.progress
        print "progress", progress
        try:
            flt = float(progress)
            return HttpResponse("progress:"+str(flt))
        except ValueError:
            return HttpResponse(progress)
    else:
        print "no file"
        return render(req, 'mosaic.html')
