'''
Created on Jan 29, 2013

@author: bpurgaso
'''
from collections import defaultdict


class DiceCheck(object):
    def __init__(self):
        self.sides = self.getIntFromUser(
            'Please enter the number of sides for the die to be tested.')
        self.iterationMultiplier = 1

    def testDie(self):
        iterations = self.sides * self.iterationMultiplier
        count = 0
        results = defaultdict(int)

        while count < iterations:
            results[self.getRollFromUser(count, iterations)] += 1
            count += 1

        return results

    def evaluateBalance(self, results):
        iterations = sum(results.values())
        for i in range(self.sides):
            print "D%s, face %s:  %s, %s%%" % (self.sides,
                i + 1, results[i + 1],
                (float(results[i + 1]) / float(iterations)) * 100)

    def getRollFromUser(self, count, iterations):
        while True:
            tmp = self.getIntFromUser(
                'Please roll the d%s and enter the value. (%s/%s)' %
                (self.sides, count + 1, iterations))
            if tmp > 0 and tmp <= self.sides:
                return tmp
            print "Your entry wasn't between 1 and %s, try again." % self.sides

    def getIntFromUser(self, msg):
        while True:
            try:
                tmp = int(raw_input(msg + '\n'))
                return tmp
            except:
                print "Entry didn't convert to an int successfully, try again."

if __name__ == '__main__':
    dc = DiceCheck()
    dc.evaluateBalance(dc.testDie())
