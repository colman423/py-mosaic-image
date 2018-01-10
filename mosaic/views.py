# coding=UTF-8
# mosaic/views.py
from django.shortcuts import render
from django.http import HttpResponse
from calculation.create_mosaic import *

procedureList = []
def findProcedure(uid):
    for p in procedureList:
        if p.sameUid(uid):
            return p
    return None

def mosaicPost(req):
    res = HttpResponse()
    if 'file' in req.POST:
        print "has file"
        file = req.POST['file']
        grid = req.POST['grid']

        newProcedure = createMosaic(file, int(grid))
        newProcedure.start()
        procedureList.append(newProcedure)

        uid = newProcedure.getUid()
        print "new procedure! uid = ", uid
        res.write(uid)
        return res

    elif 'uid' in req.POST:
        print "request progress"
        uid = req.POST['uid']
        creating = findProcedure(uid)
        if creating==None:
            print "ERR! creating==None"

        progress = creating.getProgress()

        print "procedure #"+uid+", progress: "+str(progress)
        res.write(str(progress))

        if progress['state']==4:
            procedureList.remove(creating)
            del creating

        return res


def mosaicGet(req):
    return render(req, 'templates/mosaic.html')


def mosaicReq(req):
    print req
    if req.method=="POST":
        return mosaicPost(req)
    else:
        return mosaicGet(req)