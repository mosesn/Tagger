
def rarify(count_file, input_file, output_file):
    """
    Dumps data into a new output file which can be used to populate a new counts file, now with rares
    """
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
                output_fp.write("{0} {1}\n".format("_RARE_", part))
            else:
                output_fp.write("{0} {1}\n".format(word, part))
        else:
            output_fp.write("\n")

    input_fp.close()
    output_fp.close()
    count_fp.close()

if __name__ == "__main__":
    rarify("ner.counts", "ner_train.dat","ner_train_rare.dat")
