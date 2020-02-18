# !/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = "zpgao"

import sys
import pinyin
import jieba.posseg as pseg
import string

# import re

# 这个是存储单词的文档，可以修改
FILE_PATH = "./dics/token_freq_pos%40350k_jieba.txt"

PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）、"


# construct the frequency dict of word in file_path,can be replaced
def construct_dict(file_path):
    word_freq = {}
    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency

    return word_freq


# 3500 chinese character
def load_cn_words_dict(file_path):
    cn_words_dict = ""
    with open(file_path, "r") as f:
        for word in f:
            cn_words_dict += word.strip().decode("utf-8")
    return cn_words_dict


# 一共有四种情况的错误
# 1. 多写了一个字
# 2. 前后颠倒（仅限于相邻的字）
# 3. 写错了一个字（在字典里面找到一样的替换掉）
# 4. 少写了一个字（在字典中找到一个字替换）
def edits1(phrase, cn_words_dict):
    "All edits that are one edit away from `phrase`."
    phrase = phrase.decode("utf-8")
    splits = [(phrase[:i], phrase[i:]) for i in range(len(phrase) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in cn_words_dict]
    inserts = [L + c + R for L, R in splits for c in cn_words_dict]
    return set(deletes + transposes + replaces + inserts)


# 如果组合出来的词语在单词表中就可以返回了
def known(phrases): return set(phrase for phrase in phrases if phrase.encode("utf-8") in phrase_freq)


# find the correct words through pinyin
# 第一个队列里面的是拼音相同的，第二个队列是第一个字拼音相同的，剩下的在第三个队列里面
def get_candidates(error_phrase):
    candidates_1st_order = []
    candidates_2nd_order = []
    candidates_3nd_order = []

    error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/").encode("utf-8")
    cn_words_dict = load_cn_words_dict("./cn_dict.txt")
    candidate_phrases = list(known(edits1(error_phrase, cn_words_dict)))

    for candidate_phrase in candidate_phrases:
        candidate_pinyin = pinyin.get(candidate_phrase, format="strip", delimiter="/").encode("utf-8")
        if candidate_pinyin == error_pinyin:
            candidates_1st_order.append(candidate_phrase)
        elif candidate_pinyin.split("/")[0] == error_pinyin.split("/")[0]:
            candidates_2nd_order.append(candidate_phrase)
        else:
            candidates_3nd_order.append(candidate_phrase)

    return candidates_1st_order, candidates_2nd_order, candidates_3nd_order


def auto_correct(error_phrase):
    c1_order, c2_order, c3_order = get_candidates(error_phrase)

    if c1_order:
        return max(c1_order, key=phrase_freq.get)
    elif c2_order:
        return max(c2_order, key=phrase_freq.get)
    elif c3_order:
        return max(c3_order, key=phrase_freq.get)
    else:
        print('词典中找不到可以改正的词')
        return error_phrase
        # 有错误但是在我们的字典中也找不到合适的


def auto_correct_sentence(error_sentence, verbose=True):
    jieba_cut = pseg.cut(error_sentence, HMM=True)
    # for i in jieba_cut:
    #     print(i.word + ' ' + i.flag)
    # seg_list = "\t".join(jieba_cut).split("\t")

    correct_sentence = ""

    for phrase in jieba_cut:
        # 跳过名字 nr
        if phrase.flag == 'nr' or phrase.flag == 'm':
            print('遇到名字或者数字')
            correct_sentence+=phrase.word
            continue

        correct_phrase = phrase.word
        # check if item is a punctuation
        if phrase.word not in PUNCTUATION_LIST:
            # check if the phrase in our dict, if not then it is a misspelled phrase
            if phrase.word not in phrase_freq.keys():
                correct_phrase = auto_correct(phrase.word)
                if verbose:
                    print(phrase.word, correct_phrase)

        correct_sentence += correct_phrase

    return correct_sentence


phrase_freq = construct_dict(FILE_PATH)


def err_correct(err_sent):
    # err_sent_1 = '机器学习是人工智能领遇最能体现智能的一个分知！'
    # print "Test case 1:"
    # correct_sent = auto_correct_sentence(err_sent_1)
    # print "original sentence:" + err_sent_1 + "\n==>\n" + "corrected sentence:" + correct_sent
    #
    # err_sent_2 = '杭洲是中国的八大古都之一，因风景锈丽，享有"人间天棠"的美誉！'
    # print "Test case 2:"
    # correct_sent = auto_correct_sentence(err_sent_2)
    # print "original sentence:" + err_sent_2 + "\n==>\n" + "corrected sentence:" + correct_sent

    # err_sent_3 = '原告中国农业银行股份有限公司大连商品交易所支行与被告林晶信用卡纠纷一案，本院于2019年7月5日立案后，依法族成合议庭，于2019年11月18日公开开庭进行了审审理。原告的委托诉讼代理人黄丽燕到庭参加了诉讼。被告林晶经本院合法传唤，无正当理由未到庭。本案现已审理终结。'
    correct_sent = auto_correct_sentence(err_sent)
    print("original sentence:" + err_sent + "\n==>\n" + "corrected sentence:" + correct_sent)


if __name__ == "__main__":
    err_sent = '原告中国农业银行股份有限公司大连商品交易所支行与被告林晶信用卡纠纷一案，本院于2019年7月5日立案后，依法族成合议庭，于2019年11月18日公开开庭进行了审审理。原告的委托诉讼代理人黄丽燕到庭参加了诉讼。被告林晶经本院合法传唤，无正当理由未到庭。本案现已审理终结。'
    err_correct(err_sent)
    # cn_words_dict = load_cn_words_dict("./cn_dict.txt")
    # test = edits1('人闵',cn_words_dict)
    # for res in test:
    #     print res.decode('utf-8')
