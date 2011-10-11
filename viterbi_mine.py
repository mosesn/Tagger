import math
import time
from pprint import pprint

class Viterbi(object):
    """
    The class for handling the viterbi implementation
    """
    def __init__(self):
        self.word_to_part = {}
        self.part_count = {}
        self.part_word_pair_count = {}
        self.bigrams = {}
        self.trigrams = {}
        self.cur_best = {}

    def classify(self, filename):
        """
        Classifies the trigrams, bigrams, and word/part of speech pairs in a counts file
        """
        fp = open(filename)

        for line in fp:
            lst = line.split()
            count = int(lst[0])
            count_type = lst[1]
            if count_type == "2-GRAM":
                self.bigrams[(lst[2], lst[3])] = count
            elif count_type == "3-GRAM":
                self.trigrams[(lst[2], lst[3], lst[4])] = count

            elif count_type == "WORDTAG":
                word = lst[3]
                part = lst[2]

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


    def transit(self, first, second, third):
        """
        Gives a probability based on three parts of speech
        """
        bigram = (first, second)
        if bigram in self.bigrams:
            trigram = (first, second, third)
            if trigram in self.trigrams:
                return self.trigrams[trigram] * 1.0 / self.bigrams[bigram]
            else:
                return 0
        else:
            return 0

        fp.close()

    def emit(self, part, word):
        """
        Gives a probability based on a part of speech, word pair
        """
        if part in self.part_count and (part, word) in self.part_word_pair_count:
            return(1.0 * self.part_word_pair_count[(part, word)])/ self.part_count[part]
        else:
            return 0

    def handle_sentence(self, sentence, fp_write):
        """
        Viterbi's needs an entire sentence, and then needs to write to
        a file based on what it figures out in that sentence.
        """
        old_dict = {("*", "*"): (1.0,[])}
        for word in sentence:
            cur_dict = {}

            if word in self.word_to_part:
                search_word = word
            else:
                search_word = rare_type(word)

            for part in self.word_to_part[search_word]:
                for (two_ago, one_ago), (value, lst) in old_dict.items():
                    key = (one_ago, part)
                    cur_value = value * self.emit(part, search_word) * self.transit(two_ago, one_ago, part)
                    if key in cur_dict:
                        best_value = cur_dict[key][0]
                        if cur_value > best_value:
                            cur_dict[key] = (cur_value, lst + [(part, cur_value)])
                    else:
                        cur_dict[key] = (cur_value, lst + [(part, cur_value)])
            old_dict = cur_dict

        max_value = 0
        max_lst = None
        for key, (value, lst) in old_dict.items():
            if value > max_value:
                max_value = value
                max_lst = lst

        for word, (part, value) in zip(sentence, max_lst):
            if not word == "STOP":
                fp_write.write(word + " " + part + " " + str(math.log(value)) + "\n")
            else:
                fp_write.write("\n")

    def printer(self, read_filename, write_filename):
        """
        The actual heavy lifting method, needs to be told which file to read and which to write to
        """
        fp_write = open(write_filename, "w")
        fp_read = open(read_filename)


        sentence = []
        for line in fp_read:
            word = line.strip()

            if word == "":
                self.handle_sentence(sentence + ["STOP"], fp_write)
                sentence = []
            else:
                sentence.append(word)

        fp_write.close()
        fp_read.close()

def rare_type(word):
    """
    Figures out which rare type a rare word is
    """
    if is_number(word):
        return "_NUM_"
    elif is_all_caps(word):
        return "_CAPS_"
    elif is_first_cap(word):
        return "_FIRST_"
    elif has_number(word):
        return "_NUMBERY_"
    elif is_hyphenated(word):
        return "_HYPHENATED_"
    else:
        return "_RARE_"

#found this code snippet here:
#http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python
def is_number(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def has_number(num):
    for letter in num:
        if letter.isdigit():
            return True
    return False

def is_first_cap(word):
    if word[0].isupper():
        return True
    return False

def is_all_caps(word):
    for letter in word:
        if letter.islower():
            return False
    return True

def is_hyphenated(word):
    for letter in word:
        if letter == "-":
            return True
    return False

if __name__ == "__main__":
    init = time.time()
    viterbi = Viterbi()
    viterbi.classify("ner.counts_mine")
    viterbi.printer("ner_dev_fixed.dat", "my_prediction.file")
    end = time.time()
    print(init)
    print(end)
