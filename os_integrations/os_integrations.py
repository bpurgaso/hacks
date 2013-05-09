'''
Created on May 9, 2013

@author: bpurgaso
'''

from subprocess import Popen, STDOUT, PIPE
from pprint import pprint as pp
from collections import defaultdict
#vmstat - get free memory


#get any column based system output as dict of lists

#generic, any vertical height
def os_command_to_dict(command, dead_header_height=1):
    dd = defaultdict(list)
    lines = [x.split() for x in shellCall('vmstat')[dead_header_height:]]
    for i in xrange(len(lines[0])):
        for j in lines[1:]:
            dd[str(lines[0][i])].append(j[i])
    return dd


def vmstat(dead_header_height=1):
    d = {}
    lines = [x.split() for x in shellCall('vmstat')[dead_header_height:]]
    for i in xrange(len(lines[0])):
        for j in lines[1:]:
            d[str(lines[0][i])] = j[i]
    print d['free']
    return d


def shellCall(command):
    p = Popen(
        command,
        stderr=STDOUT,
        stdout=PIPE,
        close_fds=True,
        shell=True)
    out, err = p.communicate()  # @UnusedVariable
    return out.splitlines()


#driver code below
vmstat()
