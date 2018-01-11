# coding=UTF-8
# mosaic/views.py
from django.shortcuts import render
from django.http import HttpResponse
from calculation.create_mosaic import *

def findProcedure(uid):
    print "finding..."
    for p in procedureList:
        print "compare="+p.getUid()+", my="+uid
        if p.sameUid(uid):
            return p
    return None

def mosaicPost(req):
    res = HttpResponse()
    if 'file' in req.POST:
        print "has file"
        file = req.POST['file']
        grid = req.POST['grid']

        print "prev count of list = "+str(len(procedureList))
        newProcedure = createMosaic(file, int(grid))
        newProcedure.start()
        procedureList.append(newProcedure)

        uid = newProcedure.getUid()
        print "new procedure! uid = ", uid
        res.write(uid)

        print "after count of list = "+str(len(procedureList))
        return res

    elif 'uid' in req.POST:

        print "count of list = "+str(len(procedureList)) #tmp
        print "request progress"
        uid = req.POST['uid']
        print "request uid = "+uid

        print "count of list = "+str(len(procedureList)) #tmp
        creating = findProcedure(uid)
        if creating==None:
            print "ERR! creating==None"

        progress = creating.getProgress()

        print "count of list = "+str(len(procedureList)) #tmp
        print "procedure #"+uid+", progress: "+str(progress)
        print "count of list = "+str(len(procedureList)) #tmp
        res.write(str(progress))

        if progress['state']==4:
            print "delete procedure"
            procedureList.remove(creating)
            del creating

        return res


def mosaicGet(req):
    create_tiles.do()
    return render(req, 'templates/mosaic.html')


def mosaicReq(req):
    print req
    if req.method=="POST":
        return mosaicPost(req)
    else:
        return mosaicGet(req)