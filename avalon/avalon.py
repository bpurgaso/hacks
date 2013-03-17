'''
APACHE 2.0 LICENSE
Created on Mar 17, 2013

This is a quit concept I had for transparent caching of slow method calls
in python.  I'll work out the actual implementation details on Monday and
update this codebase with functional code shortly.

@author: bpurgaso
'''


from couchbase.client import Couchbase
import json


class Avalon(object):
    '''
    Avalon is the object responsible for interacting with the cache
    transparently.
    '''

    def __init__(self,
                 couch='127.0.0.1:8091',
                 bucket='Avalon',
                 password='KingArthur'):
        '''
        Constructor
        '''
        self.__couchbase = Couchbase(couch, bucket, password)
        self.__bucket = self.__couchbase[bucket]
        pass

    def set(self, key, value):
        self.__bucket.set(key, 0, 0, json.dumps(value))

    def get(self, key):
        return self.__bucket.get(key)


def createGlobalAvalon():
    global avalon
    avalon = Avalon()


def cache(duration=0):  # duration support not implemented yet
    '''
    @param duration: Number of seconds to store in cache, 0 is permanently
    '''
    def function1(f):

        def function2(*args, **kwargs):
            global avalon
            h = hash(str(args) + str(kwargs))
            t = avalon.get(h)
            if len(t) > 0:
                return t[0]  # VERIFY THIS LINE
            else:
                tmp = f(*args, **kwargs)
                avalon.set(h, tmp)
            return tmp

        return function2

    return function1


@cache(duration=0)
def helloWorld(msg, msg2=''):
    print "Hello World! " + msg + " " + msg2

### Dummy Code ###
createGlobalAvalon()
helloWorld('hiya', msg2='asdfa')
