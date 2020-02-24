import requests
import re
import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_HTML(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'GBK'
        # news = re.match()
        return r.text
    except:
        return 'error'


# 获取所有新闻的路径
def get_path():
    page_list = []
    for i in range(2, 100):
        url_catalog = 'http://www.mzyfz.com/cms/fazhixinwen/xinwenzhongxin/fazhijujiao/html/848/list-' + str(
            i) + '.html'
        catalog = get_HTML(url_catalog)
        # print(catalog)
        relink = '<a href="(.*)" target="_blank" title="'
        res = re.findall(relink, catalog)
        print(len(res))
        page_list.extend(res)

    file_page = open('./page.txt', 'w', encoding='utf-8')
    for page in page_list:
        file_page.write(page + '\n')
    file_page.close()
    return page_list


def get_content(count, url):
    txt = get_HTML(url)
    retitle = re.compile(r'<h1 class="lt1">(.*)</h1>')
    title = re.search(retitle, txt).group(1)
    # print(txt)
    recontent = re.compile(r'<div id="maincontent">([\s\S]*?)</div>')
    content = re.search(recontent, txt).group(1)
    refilter = re.compile(r'(<.*>)|(&(.*);)')
    content = re.sub(refilter, '', content)
    print(title)
    # print(content)
    with open('./news/' + str(count) + '.txt', 'w', encoding='utf-8') as news_file:
        news_file.write(title)
        news_file.write(content)


# url = 'http://www.mzyfz.com/cms/fazhixinwen/xinwenzhongxin/fazhijujiao/html/848/2020-02-22/content-1419100.html'
# txt = get_HTML(url)
# print(txt)
# 测试get content
# test_get_content_url = 'http://www.mzyfz.com/cms/fazhixinwen/xinwenzhongxin/fazhijujiao/html/848/2020-02-12/content-1418220.html'
# get_content(0,test_get_content_url)


def get_news(count):
    with open('./news/' + str(count) + '.txt', 'r', encoding='utf-8') as f:
        txt = f.readlines()
        res = []
        for line in txt:
            line = re.sub('\u3000|\t', '', line)
            if line == '\n':
                continue
            else:
                res.append(line)
        print(res)
    with open('../../data/news/' + str(count) + '.txt', 'w', encoding='utf-8') as outfile:
        for line in res:
            outfile.write(line)


#
# # 爬虫
# page_list = get_path()
# count=0
# for page in page_list:
#     get_content(count,page)
#     count+=1


# 过滤处理
# for i in range(6000):
#     get_news(i)

import pandas as pd


def confidenceinterval(data):  # 求置信区间
    StandardDeviation_sum = 0
    # 返回样本数量
    Sizeofdata = len(data)
    data = np.array(data)
    print(data)
    Sumdata = sum(data)
    # 计算平均值
    Meanvalue = Sumdata / Sizeofdata
    # print(Meanvalue)
    # 计算标准差
    for index in data:
        StandardDeviation_sum = StandardDeviation_sum + (index - Meanvalue) ** 2
    StandardDeviation_sum = StandardDeviation_sum / Sizeofdata
    StandardDeviationOfData = StandardDeviation_sum ** 0.5
    # print(StandardDeviationOfData)
    # 计算置信区间
    LowerLimitingValue = Meanvalue - 1.645 * StandardDeviationOfData
    UpperLimitingValue = Meanvalue + 1.645 * StandardDeviationOfData
    print('置信区间---------------')
    print(LowerLimitingValue)
    print(UpperLimitingValue)
    print('置信区间---------------')


def plot_len():
    full_txtf = open('../../data/full_news.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(full_txtf, lineterminator='\n')
    csv_writer.writerow(["标题", "内容"])
    data_file = open('E:/pycharm/style_classification/train.csv', 'w', encoding='utf-8')
    csv_writer1 = csv.writer(data_file, lineterminator='\n')
    csv_writer1.writerow(["分类", "正文"])
    len_ = []
    for count in range(5000):
        with open('../../data/news/' + str(count) + '.txt', 'r', encoding='utf-8') as inputf:
            quanwen = ''
            title = inputf.readline().strip()
            for line in inputf.readlines():
                line = re.sub('\n', '', line)
                quanwen = quanwen + line
            if 100 < len(quanwen) < 1000:
                csv_writer.writerow([title, quanwen])
                csv_writer1.writerow(['news', quanwen])
                len_.append(len(quanwen))
    confidenceinterval(len_)
    # print(len_)

    # fig, axes = plt.subplots(2, 1)
    # fig = plt.figure(figsize=(16, 5))
    # x = [i for i in range(len(len_))]
    # y = sorted(len_)
    # data = pd.Series(y, x)
    # data.plot.bar(ax=axes[0], color='k', alpha=0.7, rot=0)
    # 参数alpha指定了所绘制图形的透明度，rot指定类别标签偏转的角度

    # data.plot.barh(ax=axes[1], color='k', alpha=0.7)
    # Series.plot.barh()的用法与Series.plot.bar()一样，只不过绘制的条形图是水平方向的
    # fig.savefig('p1.png')
    # print(sorted(len_))
    # 直方图
    # plt.hist(len_, bins=30, normed=True, alpha=0.5, histtype='stepfilled', color='steelblue',
    #          edgecolor='none')
    # plt.show()
    # # plt.axis([0,5000,0,0.0008])
    # print(plt.axis())

    # volin图
    dataset = len_
    sns.violinplot(data=dataset)
    plt.xlabel('Judicial News', fontsize=12)
    plt.ylabel('Number of words in text', fontsize=12)
    plt.title("Number of words in Judicial News", fontsize=15)
    plt.show()
    return len_


plot_len()
