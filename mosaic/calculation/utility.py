# coding=UTF-8
import os
import scipy.fftpack as fft

MULTIPLE = 3
DATAPATH = os.getcwd() + "/dataset/"

def isImage(f):
    return f.endswith('.jpg') or f.endswith('.png') or f.endswith('.bmp') or f.endswith('.gif')

def isData(f, extension):
    return f.endswith(extension)

def refreshData():
    import color_layout
    color_layout.do()
    import color_histogram
    color_histogram.do()

