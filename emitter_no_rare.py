import math

class Emitter(object):

    def __init__(self):
        self.word_to_part = {}
        self.part_count = {}
        self.part_word_pair_count = {}

    def classify(self, filename):
        fp = open(filename)
        for line in fp:
            lst = line.split()

            count_type = lst[1]
            if count_type == "WORDTAG":

                word = lst[3]
                part = lst[2]
                count = int(lst[0])

                if word in self.word_to_part:
                    self.word_to_part[word].append(part)
                else:
                    self.word_to_part[word] = [part]

                if part in self.part_count:
                    self.part_count[part] += count
                else:
                    self.part_count[part] = count

                if (part, word) in self.part_word_pair_count:
                    self.part_word_pair_count[(part, word)] += count
                else:
                    self.part_word_pair_count[(part, word)] = count
        fp.close()

    def emit(self, part, word):
        if part in self.part_count and (part, word) in self.part_word_pair_count:
            return(1.0 * self.part_word_pair_count[(part, word)])/ self.part_count[part]
        else:
            return 0

    def printer(self, read_filename, write_filename):
        fp_write = open(write_filename, "w")
        fp_read = open(read_filename)
        index = -1
        for line in fp_read:
            index += 1

            word = line.strip()

            if word == "":
                fp_write.write("\n")
                continue;

            pair = None

            if word in self.word_to_part:
                lst = [((part, word), self.emit(part, word)) for part in self.word_to_part[word]]

                minim = 100
                pair = None
                for x in lst:
                    if x[1] < minim:
                        minim = x[1]
                        pair = x[0]

                part = pair[0]

            if pair:
                fp_write.write("{0} {1} {2}\n".format(word, part, math.log(self.emit(part, word), 2)))
            else:
                fp_write.write("{0} O {1}\n".format(word, 0))

        fp_write.close()
        fp_read.close()

if __name__ == "__main__":
    emitter = Emitter()
    emitter.classify("ner.counts")
    emitter.printer("ner_dev_fixed.dat", "prediction_no_rare.file")
