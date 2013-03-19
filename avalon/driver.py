'''
APACHE 2.0 LICENSE
Created on Mar 18, 2013

@author: bpurgaso
'''


from avalon import cache, createGlobalAvalon
from pprint import pprint as pp


@cache(expiry=20)
def helloWorld(msg, msg2=''):
    return str("Hello World! " + msg + " " + msg2)


@cache(prefix='whoops', expiry=20)
def superWorld():
    return [1, 2, 3, 4, 5, 'asxdf']


### Dummy Code ###
print "CREATING AVALON"
createGlobalAvalon()

print "HELLO TEST\n\n"
pp(helloWorld('dfdfzzz', msg2='WzzHTHIS???'))

print "SUPER TEST\n\n"
pp(superWorld())
