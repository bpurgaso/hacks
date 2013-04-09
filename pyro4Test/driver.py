'''
Created on Apr 8, 2013

@author: bpurgaso
'''

import Pyro4
import sys
import threading
import time


class Responder(threading.Thread):
    def __init__(self):
        global uri, daemon
        threading.Thread.__init__(self)

    def run(self):
        global daemon
        daemon.requestLoop()
        print "Daemon stopped."

    def doSomething(self):
        global c0, c1, size
        c0 = time.time()
        s = '#' * size
        s2 = '#' * size
        c1 = time.time()
        return s + s2

### Driver ###
'''
Factor 1

2147483637|0.71741104126s|5.38622999191s|Compression False
KABOOM:  2147483638

2147483637|0.769376039505s|20.8928408623s|Compression True
KABOOM:  2147483638
'''

'''
Factor 2

1073741818|0.718127965927s|6.58921909332s|Compression False
KABOOM!!
'''

step = 1
min = 1073741818  # @ReservedAssignment
max = 2147483637  # @ReservedAssignment
# 1073741818
# 1030000000
Pyro4.config.COMPRESSION = False
daemon = Pyro4.Daemon()
rep = Responder()
rep.start()
uri = daemon.register(rep)

time.sleep(2)
pRep = Pyro4.Proxy(uri)

print "URI:  {0}".format(uri)
for size in xrange(min, max, step):
#    time.sleep(1)
#    try:
    try:
        pRep.doSomething()
        print '{0}|{1}s|{2}s|Compression {3}'.format(size,
                                                 c1 - c0,
                                                 time.time() - c1,
                                                 Pyro4.config.COMPRESSION)
    except:
        print "".join(Pyro4.util.getPyroTraceback())
#    except:
#        print 'KABOOM:  {0}'.format(i)

try:
    daemon.shutdown()
except:
    print "omg what"
