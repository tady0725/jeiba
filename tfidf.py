# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 09:46:00 2021

@author: Administrator
"""

import time
import jieba
import json
import math
s = time.time()
jieba.load_userdict("lexicon_dict.txt")

model = []
IDF = {}
with open("Gossiping-QA-Dataset.txt", "r", encoding="UTF-8") as f:
    num_of_documents = 0
    for line in f:
        num_of_documents += 1
        if num_of_documents == 1 or num_of_documents % 10000 == 0:
            print("num_of_documents:", "%010d" % num_of_documents)
        document = {}
        line = line[:-1].replace(" ", "")
        QA = line.split("\t")
        Q = QA[0]
        A = QA[1]

        ID = "{0:06d}" . format(num_of_documents)
        document["ID"] = ID
        document["Question"] = Q
        document["Answer"] = A

        QS = jieba.lcut(Q)
        num_of_words = len(QS)
        TF = {}
        document["Question"] = ""
        for word in QS:
            document["Question"] += word + " "
            if word not in TF:
                TF[word] = 0
            TF[word] += 1
        document["Question"] = document["Question"][:-1]

        for word in TF:
            TF[word] = round(TF[word] / num_of_words, 6)
            if word not in IDF:
                IDF[word] = 0
            IDF[word] += 1

        document["TF"] = TF
        document["TF-IDF"] = TF.copy()
        document["Inner_Production"] = 0
        model.append(document)
        # if num_of_documents == 10000:
        #     break
    print("num_of_documents:", "%010d" % num_of_documents)

for word in IDF:
    IDF[word] = round(math.log10(num_of_documents / IDF[word]), 6)

for index in range(0, num_of_documents):
    Inner_Production = 0
    for word in model[index]["TF-IDF"]:
        TFIDF = round(model[index]["TF-IDF"][word] * IDF[word], 6)
        model[index]["TF-IDF"][word] = TFIDF
        Inner_Production += TFIDF ** 2
    model[index]["Inner_Production"] = Inner_Production ** 0.5


with open("TF-IDF.json", "w", encoding="UTF-8") as jsonfile:
    json.dump(model, jsonfile, separators=(
        ",", ": "), indent=4, ensure_ascii=False)

with open("IDF.json", "w", encoding="UTF-8") as jsonfile:
    json.dump(IDF, jsonfile, separators=(
        ",", ": "), indent=4, ensure_ascii=False)

e = time.time()

print("共花費秒數:", round(e-s, 6))
