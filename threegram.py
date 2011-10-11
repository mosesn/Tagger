import math
from pprint import pprint

class Tagger(object):

    def __init__(self):
        self.bigrams = {}
        self.trigrams = {}

    def classify(self, filename):
        fp = open(filename)

        for line in fp:
            lst = line.split()
            class_type = lst[1]
            if class_type == "2-GRAM":
                self.bigrams[(lst[2], lst[3])] = int(lst[0])
            elif class_type == "3-GRAM":
                self.trigrams[(lst[2], lst[3], lst[4])] = int(lst[0])

    def transit(self, first, second, third):
        bigram = (first, second)
        if bigram in self.bigrams:
            trigram = (first, second, third)
            if trigram in trigrams:
                return 1.0 * self.trigrams[trigram] / self.bigrams[bigram]
            else:
                return 0
        else:
            return 0

        fp.close()

    def simple_printer(self, filename):
        fp = open(filename)

        for line in fp:
            lst = line.split()
            num = self.transit(lst[0], lst[1], lst[2])
            if num > 0:
                pprint(math.log(num))
            else:
                pprint(0)
        fp.close()

