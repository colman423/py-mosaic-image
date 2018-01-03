# coding=utf-8
import time
def test2():
    data = [range(i, i+10000) for i in xrange(0, 100000000, 10000)]
    # print data
    start_time = time.time()

    # new = []
    # for x in xrange(10000):
    #     for y in xrange(10000):
    #         new.append(data[x][y])

    new = [0]*100000000
    for x in xrange(10000):
        for y in xrange(10000):
            new[x*1000+y] = data[x][y]


    print("--- %s seconds ---" % (time.time() - start_time))


def test3():

    start_time = time.time()
    arr = [9999999]*1000000
    print("--- %s seconds ---" % (time.time() - start_time))
if __name__=="__main__":
    test3()
