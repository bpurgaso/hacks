#!/usr/bin/python

'''
Created on Feb 25, 2013

@author: bpurgaso

A quick two-hop port forwarding solution, with clean tunnel cleanup on exit.
Designed only for environments where password-less login is enabled and
whereconnections take less than 5 seconds.
'''

import threading
from subprocess import Popen, STDOUT, PIPE
from time import sleep


class worker(threading.Thread):
    '''
    External script executing threads
    '''

    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command

    def run(self):
        self.__shellCall(self.command)

    def __shellCall(self, command):
        self.p = Popen(
                       command,
                       stderr=STDOUT,
                       stdout=PIPE,
                       close_fds=True,
                       shell=True)
        out, err = self.p.communicate()  # @UnusedVariable
        return out.splitlines()

#get params

sshPort = 22
linkPort = 8000
destinationPort = 80
entryPort = 9091
bastionHost = "defender.pcs.cnu.edu"
destinationHost = "guardedbynarwhal.com"
tunnelDelay = 5

c1 = "ssh -L %s:%s:%s -N %s" % (linkPort,
                                destinationHost,
                                sshPort,
                                bastionHost)
c2 = "ssh -L %s:localhost:%s -N -p %s localhost" % (entryPort,
                                                    destinationPort,
                                                    linkPort)

print "Preparing to tunnel to %s through %s." % (destinationHost, bastionHost)
print "Localhost entry port:  %s" % (entryPort)

t1 = worker(c1)
t2 = worker(c2)

t1.daemon = True
t2.daemon = True

t1.start()
print "Tunneling to bastion."
sleep(tunnelDelay)
t2.start()
print "Tunneling to remote host"
tmp = ''
while 'exit' != tmp:
    tmp = raw_input('Type "exit" to shutdown relay.')
