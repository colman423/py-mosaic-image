# coding=UTF-8
# mosaic/views.py
from django.shortcuts import render
from django.http import HttpResponse
from create_mosaic import *
from calculation.utility import refreshData

def findProcedure(uid):
    for p in procedureList:
        if p.sameUid(uid):
            return p
    return None

def mosaicPost(req):
    res = HttpResponse()
    if 'file' in req.POST:
        print "new file"
        file = req.POST['file']
        grid = req.POST['grid']

        newProcedure = createMosaic(file, int(grid))
        newProcedure.start()
        procedureList.append(newProcedure)

        uid = newProcedure.getUid()
        res.write(uid)

        return res

    elif 'uid' in req.POST:

        uid = req.POST['uid']
        print "request progress, uid="+uid

        creating = findProcedure(uid)
        if creating==None:
            print "ERR! creating==None"

        progress = creating.getProgress()

        print "procedure #"+uid+", progress: "+str(progress)
        res.write(str(progress))

        if progress['state']==4:
            print "delete procedure"
            procedureList.remove(creating)
            del creating

        return res


def mosaicGet(req):
    refreshData()
    return render(req, 'templates/mosaic.html')


def mosaicReq(req):
    # print req
    if req.method=="POST":
        return mosaicPost(req)
    else:
        return mosaicGet(req)