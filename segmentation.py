
def load_dict(filename):
    dict_word = []
    f = open(filename, "r", encoding="UTF-8")
    for line in f:
        temp = line.split(" ")
        dict_word.append(temp[0])
    f.close()
    return dict_word


def ws2is(sentence):
    ws = sentence.split(" ")
    indexsequence = []

    ind = 0
    for w in ws:
        indexsequence.append(str(ind) + "," + str(ind + len(w) - 1))
        ind += len(w)
    return indexsequence


def fmm(sentence, dictionary):
    new_sentence = ""
    while (sentence != ""):
        isindict = False
        for i in range(0, len(sentence)):
            if sentence[0:(len(sentence) - i)] in dictionary:
                isindict = True
                new_sentence += sentence[0:(len(sentence) - i)]
                sentence = sentence[(len(sentence) - i):len(sentence)]
                break
        if not isindict:
            new_sentence += sentence[0:1]
            sentence = sentence[1:len(sentence)]
        new_sentence += " "
    new_sentence = new_sentence[:-1]
    return new_sentence


dict_word = load_dict("lexicon1_raw_nosil.txt")

total_of_A = 0
total_of_B = 0
total_of_AB = 0

f = open("GigaWord_text_lm", "r", encoding="UTF-8")
for line in f:
    old_sentence = line[:-1]
    A = ws2is(old_sentence)
    sentence = old_sentence.replace(" ", "")
    new_sentence = fmm(sentence, dict_word)
    B = ws2is(new_sentence)
    num_of_A = len(A)
    num_of_B = len(B)
    num_of_AB = 0
    for s in B:
        if s in A:
            num_of_AB += 1
    total_of_A += num_of_A
    total_of_B += num_of_B
    total_of_AB += num_of_AB

    P = round((total_of_AB / total_of_B) * 100, 2)
    R = round((total_of_AB / total_of_A) * 100, 2)
    print("P:", P, "R:", R)
    """
    print(old_sentence)
    print(A)
    print(new_sentence)
    print(B)
    print("**********")
    """
f.close()
