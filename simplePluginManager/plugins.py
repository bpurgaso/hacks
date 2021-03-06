'''
Created on Feb 18, 2013

@author: bpurgaso

Licensed under the APACHE 2.0 license.
http://www.apache.org/licenses/LICENSE-2.0.html
'''

import sys
from os import listdir
from inspect import isclass
from inspect import getmembers
from collections import defaultdict


class pluginManager(object):
    '''
    importable pluginManager object to load very simple plugins
    Designed with inTune in mind.
    '''
    def __init__(self, handle, pluginDirPath='./plugins/', verbose=False):
        self.handle = handle
        self.pluginDirPath = pluginDirPath
        self.verbose = verbose
        sys.path.insert(0, self.pluginDirPath)
        self.classList, self.registeredPlugins = self.loadPlugins()

    def reloadPlugins(self):
        self.classList, self.registeredPlugins = self.loadPlugins()

    def loadPlugins(self):
        registeredPlugins = defaultdict(lambda: defaultdict(list))
        for i in listdir(self.pluginDirPath):
            if i.endswith('.py'):
                print "checking %s" % i
                module = __import__(i[:-3])
                classList = []
                for name, obj in getmembers(module):
                    if isclass(obj):
                        try:
                            a = obj()
                            for k in a.getManifest():
                                print 'appending, ', k[2]
                                registeredPlugins[k[0]][k[1]].append(k[2])
                            classList.append(obj)
                        except Exception, err:
                            if self.verbose:
                                print Exception, err
        return (classList, registeredPlugins)

    def getClassList(self):
        return self.classList

    def executePlugins(self, stage):
        if self.verbose:
            print 'executing stage ', stage
        priorities = self.registeredPlugins[stage].keys()
        priorities.sort()

        for i in priorities:
            for func in self.registeredPlugins[stage][i]:
                func(self.handle)


class plugin(object):

    @property
    def getManifest(self):
        '''
        getManifest() is responsible for reporting a function or functions
        that are to be executed, and at what stage their execution should
        occur.

        Every function that is to be registed with getManifest must take
        exactly one param, a handle to the object that created the
        pluginManager.
        '''
        raise NotImplementedError('Missing getManifest() implementation in '\
                                  '%s!' % self.__class__.__name__)

    def __init__(self):
        '''
        The modules will be imported and classes listed in the manifest will
        be instantiated.  Though an init is not required, it is recommend
        to explicitly pass if unneeded.
        '''
        pass

'''
Dummy code to demo the pluginManager
'''
if __name__ == '__main__':
    pm = pluginManager(None, verbose=True)
    pm.loadPlugins()
    print '\n\n'
    print "classList:  ", pm.classList
    print '--  registered functions  --'
    for i in pm.registeredPlugins.keys():
        for j in pm.registeredPlugins[i].keys():
            print i, j, pm.registeredPlugins[i][j]

    for i in range(0, 5):
        pm.executePlugins(i)
