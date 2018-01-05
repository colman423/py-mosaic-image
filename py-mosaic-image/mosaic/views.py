# coding=UTF-8
# mosaic/views.py
from django.shortcuts import render
from django.http import HttpResponse
from calculation.create_mosaic import create, progress
from threading import Thread
import os

class createMosaic(Thread):
    def __init__(self, file, grid):
        super(createMosaic, self).__init__()
        self.file = file
        self.grid = grid
    def run(self):
        create(self.file, self.grid)


def mosaicPost(req):
    res = HttpResponse()
    if 'file' in req.POST:
        print "has file"
        file = req.POST['file']
        grid = req.POST['grid']
        createMosaic(file, int(grid)).start()
        res.write(progress)
        return res

    elif 'wait' in req.POST:
        res.write(progress)
        return res

        # progress = mosaic.create_mosaic.progress
        # print "progress", progress
        # try:
        #     flt = float(progress)
        #     res.write("progress:" + str(flt))
        #     res['attr'] = "val"
        #     return res
        #
        # except ValueError:
        #     try:
        #         with open(progress, "rb") as f:
        #             data = f.read()
        #             with open(os.getcwd() + "\\trytry.jpg", "w+") as ff:
        #                 ff.write(data)
        #             return HttpResponse(data, content_type="image/jpeg")
        #     except IOError:
        #         return HttpResponse("NONONO")

                # return progress

def mosaicGet(req):
    return render(req, 'templates\\mosaic.html')


def mosaicReq(req):
    print req
    print progress
    if req.method=="POST":
        return mosaicPost(req)
    else:
        return mosaicGet(req)