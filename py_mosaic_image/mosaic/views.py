# coding=UTF-8
# mosaic/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django_socketio.events import on_connect
from django_socketio.events import on_message
from django_socketio.events import on_error

def mosaicReq(req):
    FILE = 'file'
    print req
    if FILE in req.POST:
        print "has file"
        file = req.POST[FILE]
        print file
        output = ""
        return HttpResponse(output)

    else:
        print "no file"
        return render(req, 'mosaic.html')

@on_connect
def on_connect(message):
    print "FUfghfghK"
    print "FUfghfghK"
    print "FUfghfghK"
    print "FUfghfghK"
    print "FUfghfghK"
    print "FUfghfghK"

@on_message
def notification(request, socket, context, message):
    print "NONONO"
    socket.broadcast_channel({'id': message['id']})

@on_error
def on_error(request, socket, context, exception):
    print "sdf"

from websocket import server
# ws = create_connection("ws://127.0.0.1:9000/")
# ws.send("Hello, World")