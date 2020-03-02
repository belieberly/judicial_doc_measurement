# 字符串相似度检测的库
import difflib
import re
import config as cf


def difflib_text():
    query_str = '今天是星期五，我和小王出去买早点的路上遇到了猪皮'
    s1 = '今天是星期六，天气很好，我和小王出去玩'
    s2 = '我和小王出去买早点'
    s3 = '今天是星期五，我和小王出去买早点'
    print(difflib.SequenceMatcher(None, query_str, s1).quick_ratio())
    print(difflib.SequenceMatcher(None, query_str, s2).quick_ratio())
    print(difflib.SequenceMatcher(None, query_str, s3).quick_ratio())


# 编辑距离
# https://blog.csdn.net/u010368839/article/details/78963843?utm_source=blogxgwz7
def levenshtein(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    dif = [[i for i in range(len2 + 1)] for j in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if (str1[i - 1] == str2[j - 1]):
                tmp = 0
            else:
                tmp = 1
            dif[i][j] = min(dif[i - 1][j - 1] + tmp, dif[i][j - 1] + 1, dif[i - 1][j] + 1)
    # print('字符串' + str1 + '与字符串' + str2)
    # print('差异' + str(dif[len1][len2]))
    similarity = 1 - (dif[len1][len2] / max(len1, len2))
    print(similarity)
    return similarity


# str1 = '今天是不是是不是是不是星期五'
# str2 = '今天星期四'
#
# levenshtein(str1,str2)

import heapq

a = [1, 2, 3, 4, 5]
re1 = map(a.index, heapq.nlargest(3, a))  # 求最大的三个索引    nsmallest与nlargest相反，求最小
re2 = heapq.nlargest(3, a)  # 求最大的三个元素
print(list(re1))  # 因为re1由map()生成的不是list，直接print不出来，添加list()就行了


def find_max(number, list_):
    while len(list_) < number:
        number = number - 1
    re1 = map(a.index, heapq.nlargest(number, list_))  # 求最大的三个索引    nsmallest与nlargest相反，求最小
    re2 = heapq.nlargest(number, list_)  # 求最大的三个元素
    return list(re1), re2



#主函数
# str1为原告/被告诉称段，str2为查明事实段
def long_detect(str1, str2):
    pattern = r'，|。|；|：'
    sentence_list1 = re.split(pattern, str1)
    sentence_list2 = re.split(pattern, str2)
    res1 = []
    res2 = []
    sim_list = []
    for sentence in sentence_list2:
        similar_sen = ''
        max_sen = 0
        if len(sentence) < 5:
            continue
        for sen in sentence_list1:
            if len(sen) < 5:
                continue
            sim1 = difflib.SequenceMatcher(None, sen, sentence).quick_ratio()
            sim2 = levenshtein(sen, sentence)
            print(sim1, sim2)
            sim_sen = (sim1 + sim2) / 2
            if sim_sen > max_sen:
                max_sen = sim_sen
                similar_sen = sen
        res1.append(sentence)
        res2.append(similar_sen)
        sim_list.append(max_sen)
    if len(res1) <= 1:
        return False
    res = []
    for i in range(len(sim_list)):
        if sim_list[i] > cf.copy_detect_threshold:
            res.append('<' + res1[i] + '>与<' + res2[i] + '>相似')
    if len(res) == 0:
        return cf.copy_detect_score, ''
    elif len(res) > 4:
        return 0, ','.join(res)
    else:
        return cf.copy_detect_score - cf.copy_detect_fault * len(res), ','.join(res)


if __name__ == '__main__':
    score, str = long_detect('我也不是不想找小伙伴，只是觉得网友都太不可靠了，不知道什么时候就翻脸不认人了', '肖战有什么错呢，他只是一个认真工作，努力上进的人，网友都太不可靠了')
    print(score, str)
