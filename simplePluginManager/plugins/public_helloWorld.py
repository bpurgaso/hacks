'''
Created on Feb 18, 2013

@author: bpurgaso

Licensed under the APACHE 2.0 license.
http://www.apache.org/licenses/LICENSE-2.0.html
'''

from plugins import plugin


class public_hello_world(plugin):
    '''
    Quick demo class to demo the code
    '''

    def __init__(self):
        '''
        Constructor
        '''
        print "got to init in hello world"

    def helloWorld(self, at):
        print 'Hello world!'

    def getManifest(self):
        return [(1, -1, self.helloWorld), (2, 10, self.helloWorld)]


class decoy(object):
    '''
    Quick demo class to demo the code
    Doesn't extend the correct class, so it won't have getManifest() at all
    '''
    pass


class decoy2(plugin):
    '''
    Quick demo class to demo the code
    extends the correct class but doesn't implement getManifest()
    '''
