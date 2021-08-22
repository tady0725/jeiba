# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 12:51:49 2021

@author: Administrator
"""

import time
import jieba
import json
import math

print("model讀取中....")
begin_time = time.time()
with open("TF-IDF.json", "r", encoding="UTF-8") as jsonfile:
    model = json.load(jsonfile)
with open("IDF.json", "r", encoding="UTF-8") as jsonfile:
    IDF = json.load(jsonfile)
end_time = time.time()
print("model讀入時間", round(end_time - begin_time, 6), "秒")

jieba.load_userdict("lexicon_dict.txt")

while True:
    # 使用者輸入
    query = input("請輸入查詢問句(若要結束請輸入exit):")
    if query == "exit":
        break

    query = query.replace(" ", "")
    QS = jieba.lcut(query)
    num_of_words = len(QS)
    TF = {}
    for word in QS:
        if word not in TF:
            TF[word] = 0
        TF[word] += 1
    B = 0
    for word in TF:
        TF[word] = round(TF[word] / num_of_words, 6)
        if word in IDF:
            TFIDF = round((TF[word] * IDF[word]), 6)
            B += TFIDF ** 2
    B = B ** 0.5

    num_of_documents = len(model)
    max_sim = 0
    max_doc = 0
    for i in range(0, num_of_documents):
        A = model[i]["Inner_Production"]
        AdotB = 0
        for word in TF:
            if word in model[i]["TF-IDF"]:
                AdotB += TF[word] * IDF[word] * model[i]["TF-IDF"][word]
        if AdotB > 0:
            sim = AdotB / (A * B)
            if sim > max_sim:
                max_sim = sim
                max_doc = i
    print("System:", model[max_doc]["Answer"])
