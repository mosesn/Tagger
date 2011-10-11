def rarify(count_file, input_file, output_file):
    LIMIT = 5

    input_fp = open(input_file)
    count_fp = open(count_file)
    output_fp = open(output_file, "w")

    rare = {}

    for line in count_fp:
        lst = line.split()
        count = int(lst[0])
        count_type = lst[1]
        if count_type == "WORDTAG":
            word = lst[3]
            if word in rare:
                rare[word] += count
            else:
                rare[word] = count

    for line in input_fp:
        lst = line.split()
        if len(lst) > 0:
            word = lst[0]
            part = lst[1]
            if word in rare and rare[word] < LIMIT:
                output_fp.write("{0} {1}\n".format(rare_type(word), part))
            else:
                output_fp.write("{0} {1}\n".format(word, part))
        else:
            output_fp.write("\n")

    input_fp.close()
    output_fp.close()
    count_fp.close()

def rare_type(word):
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
    rarify("ner.counts", "ner_train.dat","ner_train_mine.dat")
