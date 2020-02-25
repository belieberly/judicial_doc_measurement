#字符串相似度检测的库
import difflib

def difflib_text():
    query_str = '今天是星期五，我和小王出去买早点的路上遇到了猪皮'
    s1 = '今天是星期六，天气很好，我和小王出去玩'
    s2 = '我和小王出去买早点'
    s3 = '今天是星期五，我和小王出去买早点'
    print(difflib.SequenceMatcher(None, query_str, s1).quick_ratio())
    print(difflib.SequenceMatcher(None, query_str, s2).quick_ratio())
    print(difflib.SequenceMatcher(None, query_str, s3).quick_ratio())

#编辑距离
#https://blog.csdn.net/u010368839/article/details/78963843?utm_source=blogxgwz7
def levenshtein(str1,str2):
    len1 = len(str1)
    len2 = len(str2)
    dif = [[i for i in range(len2+1)] for j in range(len1+1)]
    for i in range(1,len1+1):
        for j in range(1,len2+1):
            if(str1[i-1]==str2[j-1]):
                tmp = 0
            else:
                tmp = 1
            dif[i][j] = min(dif[i-1][j-1]+tmp,dif[i][j-1]+1,dif[i-1][j]+1)
    print('字符串'+str1+'与字符串'+str2)
    print('差异'+str(dif[len1][len2]))
    similarity = 1-(dif[len1][len2]/max(len1,len2))
    print(similarity)

str1 = '今天是不是是不是是不是星期五'
str2 = '今天星期四'

levenshtein(str1,str2)
