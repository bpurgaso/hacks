'''
APACHE 2.0 LICENSE
Created on Mar 17, 2013

This is a quit concept I had for transparent caching of slow method calls
in python.  I'll work out the actual implementation details on Monday and
update this codebase with functional code shortly.

@author: bpurgaso
'''


from couchbase.client import Couchbase
import simplejson as json
from pprint import pprint as pp


class Avalon(object):
    '''
    Avalon is the object responsible for interacting with the cache
    transparently.
    '''

    def __init__(self,
                 couch='127.0.0.1:8091',
                 uname='username',
                 bucket='bucket',
                 password='password'):
        '''
        Constructor
        '''
        self.__couchbase = Couchbase(couch, uname, password)
        self.__bucket = self.__couchbase[bucket]

    def set(self, key, value, expiry=0):
        print "expiry:  ", expiry
        return self.__bucket.set(str(key), expiry, 0, json.dumps(value))

    def get(self, key):
        print "KEY: ", key
        try:
            tmp = self.__bucket.get(str(key))
            pp(tmp)
            t = json.loads(tmp[2])
            if t is not None:
                print 'CACHE HIT:  {0}'.format(key)
                return json.loads(tmp[2])
        except:
            pass
        return ()


def createGlobalAvalon():
    global AVALON
    AVALON = Avalon()


def cache(prefix='', expiry=0):  # duration support not implemented yet
    '''
    @param duration: Number of seconds to store in cache, 0 is permanently
    '''
    def function1(f):

        def function2(*args, **kwargs):
            global AVALON
            h = prefix + str(hash(str(args) + str(kwargs)))
            print "GET STARTING with hash:  ", h
            t = AVALON.get(h)
            print "GET OK, ", t
            if len(t) > 0:
                return t  # VERIFY THIS LINE
            else:
                tmp = f(*args, **kwargs)
                print AVALON.set(h, tmp, expiry=expiry)
            return tmp

        return function2

    return function1
