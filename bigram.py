import math
import time

begin_time = time.time()
# 一元
unigram = {}
# 二元
bigram = {}

total_of_words = 0
num_of_lines = 0
f = open("GigaWord_text_lm", "r", encoding="UTF-8")
for line in f:
    num_of_lines += 1
    if num_of_lines == 1 or num_of_lines % 10000 == 0:
        print("num of lines:", "%010d" % num_of_lines)
    line = line[:-1]
    line = "<s> " + line + " </s>"
    ws = line.split(" ")

    for w in ws:
        total_of_words += 1
        if w in unigram:
            unigram[w] += 1
        else:
            unigram[w] = 1

    for i in range(0, len(ws) - 1):
        bi = ws[i] + " " + ws[i + 1]
        if bi in bigram:
            bigram[bi] += 1
        else:
            bigram[bi] = 1
    # if num_of_lines == 10000:
    #    break
f.close()
print("num of lines:", "%010d" % num_of_lines)

f = open("unigram.txt", "w", encoding="UTF-8")
for w in unigram:
    f.write(str("%010.6f" % round(math.log10(
        unigram[w] / total_of_words), 6)) + "\t" + w + "\n")
f.close()

f = open("bigram.txt", "w", encoding="UTF-8")
for w in bigram:
    uni = w.split(" ")
    f.write(str("%010.6f" % round(math.log10(
        bigram[w] / unigram[uni[0]]), 6)) + "\t" + w + "\n")
f.close()
end_time = time.time()
print("time:", "%010d" % (end_time - begin_time), "s")
a = round(((end_time - begin_time)/60), 2)
aa = round(((end_time - begin_time) % 60), 2)
print("time:" + str(a) + "m" + str(aa) + "s")
