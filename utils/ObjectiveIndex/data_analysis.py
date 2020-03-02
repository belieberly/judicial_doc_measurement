
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from xml.etree import ElementTree as etree
import re
import datetime, time
import json
import sys
# sys.path.append(r'')
# import

standard = ['文首', '首部', '事实', '理由', '依据', '主文', '尾部', '落款', '其他', '附件']


def wenshu_analysis(root_node):
    wenshu = {'文首': [], "首部": [], "事实": [], "理由": [], "依据": [], "主文": [], "尾部": [], '落款': [], '其他': [], '附件': []}
    # 第一次循环找到关键字节点
    test = []
    index = [-1 for i in range(10)]
    for i in range(len(root_node)):
        if root_node[i].tag == 'WS':
            wenshu['文首'].append(root_node[i])
            index[0] = i
        elif root_node[i].tag == 'DSR' or root_node[i].tag == 'SSJL':
            wenshu['首部'].append(root_node[i])
            index[1] = i
        elif root_node[i].tag == 'AJJBQK':
            wenshu['事实'].append(root_node[i])
            index[2] = i
        elif root_node[i].tag == 'CPFXGC':
            wenshu['理由'].append(root_node[i])
            index[3] = i
            for subnode in root_node[i]:
                if subnode.tag == 'FLFTYY':
                    wenshu['依据'].append(subnode)
                    index[4] = i
        elif root_node[i].tag == 'PJJG':
            wenshu['主文'].append(root_node[i])
            index[5] = i
            for subnode in root_node[i]:
                if subnode.tag == 'SSFCD':
                    index[6] = i
                    wenshu['尾部'].append(subnode)
        elif root_node[i].tag == 'WW':
            wenshu['落款'].append(root_node[i])
            index[7] = i
        elif root_node[i].tag == 'FJ':
            wenshu['附件'].append(root_node[i])
            index[8] = i
        else:
            test.append(i)
    print('结构事项顺序' + str(index))
    for i in range(len(test)):
        if test[i] > (max(index)):
            wenshu['其他'].append(root_node[i])
        else:
            print('------未知错误')
            print(root_node[i].tag)
    return wenshu, index


def walkData(root_node, level, result_list):
    temp_list = [level, root_node.tag, root_node.attrib]
    result_list.append(temp_list)

    # 遍历每个子节点
    children_node = list(root_node)
    if len(children_node) == 0:
        return result_list
    for child in children_node:
        walkData(child, level + 1, result_list)
    return result_list


def met_CSR(root_node):
    for node in root_node:
        if node.tag == 'DSR':
            CSR_count = []
            for subnode in node:
                if subnode.tag == 'DLR' or subnode.tag == 'QSF' or subnode.tag == 'YSF':
                    result_list = []
                    level = 1
                    result_list = walkData(subnode, level, result_list)
                    CSR_count.append(len(result_list))
    print(CSR_count)
    return CSR_count


# met_CSRXX(root_node,wenshu_corr)


# 事实描述部分细致性
def met_AJJBQK(wenshu):
    root = wenshu['事实'][0]
    result_list = []
    level = 1
    result_list = walkData(root, level, result_list)
    AJJBQK_count = len(result_list)
    print(AJJBQK_count)
    return AJJBQK_count


# 理由部分细致性

def met_CPFXGC(wenshu):
    root = wenshu['理由'][0]
    result_list = []
    level = 1
    result_list = walkData(root, level, result_list)
    CPFXGC_count = len(result_list)
    print(CPFXGC_count)
    return CPFXGC_count

#文书细致性指标分析
path_file = open('G:/judicial_data/民事一审案件.tar/民事一审案件/path_min_pan_filter_len.txt', 'r', encoding='utf-8')

def met_analysis(path_file):
    met_analysis_dic = {'案件基本情况':[],'裁判分析过程':[],'当事人':[]}
    outfile = open('./met.json','w',encoding='utf-8')
    AJJBQK_count_list = []
    CPFXGC_count_list = []
    DSR_count_list = []
    for filepath in path_file.readlines():
        xml_file = etree.parse('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/'+filepath.strip())
        root_node = xml_file.getroot()[0]
        wenshu_corr = {'文首': [], "首部": [], "事实": [], "理由": [], "依据": [], "主文": [], "尾部": [], '落款': [], '其他': [], '附件': []}
        wenshu, index = wenshu_analysis(root_node)
        if len(wenshu['事实'])!=0:
            AJJBQK_count = met_AJJBQK(wenshu)
            AJJBQK_count_list.append(AJJBQK_count)
        if len(wenshu['理由']) != 0:
            CPFXGC_count = met_CPFXGC(wenshu)
            CPFXGC_count_list.append(CPFXGC_count)
        DSR_count = met_CSR(root_node)
        DSR_count_list.extend(DSR_count)
    met_analysis_dic['案件基本情况'] = AJJBQK_count_list
    met_analysis_dic['裁判分析过程'] = CPFXGC_count_list
    met_analysis_dic['当事人'] = DSR_count_list
    json.dump(met_analysis_dic,outfile,ensure_ascii=False)
    print(AJJBQK_count_list)
    print(CPFXGC_count_list)
    print(DSR_count_list)
    return AJJBQK_count_list,CPFXGC_count_list,DSR_count_list


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
    LowerLimitingValue = Meanvalue - 1* StandardDeviationOfData
    UpperLimitingValue = Meanvalue + 1 * StandardDeviationOfData
    print('置信区间---------------')
    print(LowerLimitingValue)
    print(UpperLimitingValue)
    print('置信区间---------------')



def wenshu_len_analysis():
    path_file = open('G:/judicial_data/民事一审案件.tar/民事一审案件/path_min_pan.txt', 'r', encoding='utf-8')
    len_ = []
    count = 0
    count1=0
    out_path = open('G:/judicial_data/民事一审案件.tar/民事一审案件/path_min_pan_filter_len.txt', 'w', encoding='utf-8')
    for filepath in path_file.readlines():
        count+=1
        print(count)
        if count>=50000:
            break
        xml_file = etree.parse('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/'+filepath.strip())
        root_node = xml_file.getroot()[0]
        flag = 0
        for node in root_node:
            if node.tag=='AJJBQK':
                AJJBQK_txt = node.get('value')
                # print(AJJBQK_txt)
                judicial_len = len(AJJBQK_txt)
                if re.match(r' (原告|.{2,3}诉称).*',AJJBQK_txt):
                    # print(filepath+node.get('value'))
                    flag+=1
            if node.tag=='WS':
                    WS_txt = node.get('value')
                    # print(node.get('value'))
                    if re.match(r'.{0,15}人民法院 民事判决书 （[0-9]{4}）.{0,8}初字第[0-9]{0,6}号',WS_txt):
                        # print(node.get('value'))
                        flag+=1
        if flag==2:
            count1+=1
            out_path.write(filepath)

    print(count1)
    # confidenceinterval(len_)
    # # volin图
    # dataset = len_
    # sns.violinplot(data=dataset)
    # plt.xlabel('Judicial Docs', fontsize=12)
    # plt.ylabel('Number of words in AJJBQK', fontsize=12)
    # plt.title("Number of words in Judicial Documents", fontsize=15)
    # plt.show()
    # return len_

# wenshu_len_analysis()
def wenshu_date(path_file):
    province_list = {'北京市': 0, '广东省': 0, '山东省': 0, '江苏省': 0, '河南省': 0, '上海市': 0, '河北省': 0, '浙江省': 0, '陕西省': 0,
                     '湖南省': 0, '重庆市': 0, '福建省': 0, '天津市': 0, '云南省': 0, '四川省': 0, '广西壮族自治区': 0, '安徽省': 0, '海南省': 0,
                     '江西省': 0, '湖北省': 0, '山西省': 0, '辽宁省': 0, '黑龙江': 0, '内蒙古自治区': 0, '贵州省': 0, '甘肃省': 0, '青海省': 0,
                     '新疆维吾尔自治区': 0, '西藏区': 0, '吉林省': 0, '宁夏回族自治区': 0}
    date_list={}
    for filepath in path_file.readlines():
        xml_file = etree.parse('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/'+filepath.strip())
        root_node = xml_file.getroot()[0]
        flag = 0
        for node in root_node:
            if node.tag=='WS':
                WS_txt = node.get('value')
                print(WS_txt)
                if re.match(r'.{0,1}(北京市|广东省|山东省|江苏省|河南省|上海市|河北省|浙江省|陕西省|湖南省|重庆市|福建省|天津市|云南省|四川省|广西壮族自治区|安徽省|海南省|江西省|'
                                    r'湖北省|山西省|辽宁省|黑龙江|内蒙古自治区|贵州省|甘肃省|青海省|新疆维吾尔自治区|西藏区|吉林省|宁夏回族自治区).{1,10}人民法院 民事判决书 '
                            r'（([0-9]{4})）.{0,8}初字第[0-9]{0,6}号', WS_txt):
                    #获取地点
                    date = re.match(r'.{0,1}(北京市|广东省|山东省|江苏省|河南省|上海市|河北省|浙江省|陕西省|湖南省|重庆市|福建省|天津市|云南省|四川省|广西壮族自治区|安徽省|海南省|江西省|'
                                    r'湖北省|山西省|辽宁省|黑龙江|内蒙古自治区|贵州省|甘肃省|青海省|新疆维吾尔自治区|西藏区|吉林省|宁夏回族自治区).{1,10}人民法院 民事判决书 （([0-9]{4})）.{0,8}初字第[0-9]{0,6}号', WS_txt).group(1)
                    province_list[date]+=1
                    #获取时间
                    place = re.match(r'.{0,1}(北京市|广东省|山东省|江苏省|河南省|上海市|河北省|浙江省|陕西省|湖南省|重庆市|福建省|天津市|云南省|四川省|广西壮族自治区|安徽省|海南省|江西省|'
                                    r'湖北省|山西省|辽宁省|黑龙江|内蒙古自治区|贵州省|甘肃省|青海省|新疆维吾尔自治区|西藏区|吉林省|宁夏回族自治区).{1,10}人民法院 民事判决书 （([0-9]{4})）.{0,8}初字第[0-9]{0,6}号', WS_txt).group(2)
                    if date_list.get(place):
                        date_list[place]+=1
                    else:
                        date_list[place]=1
                    print(date)
    out_file = open('./province.json','w',encoding = 'utf-8')
    json.dump(province_list,out_file,ensure_ascii=False)
    out_file2 = open('./date.json','w',encoding = 'utf-8')
    json.dump(date_list,out_file2,ensure_ascii=False)



# wenshu_date()
def plot_show(json_path,x_label,y_label,title):
    file = open(json_path,'r',encoding = 'utf-8')
    dic = json.load(file)
    x =[]
    y = []
    for i in dic:
        print(i)
        x.append(i)
        y.append(dic[i])
    print(x)
    print(y)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题-设置字体为黑体
    plt.rcParams['axes.unicode_minus'] = False
    fig1 = sns.barplot(x, y)
    # plt.xticks(x, x, rotation=30)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.title(title, fontsize=15)
    plt.savefig('./'+title+'.png')
    plt.show()

def plot_show_volin(json_path,Chinese_name,English_name):
    file = open(json_path,'r',encoding = 'utf-8')
    dic = json.load(file)
    len_ = dic[Chinese_name]
    confidenceinterval(len_)
    # volin图
    dataset = len_
    dataset.sort()
    dataset_ = dataset[0:int(0.90*len(dataset))]
    print(len(dataset))

    confidenceinterval(dataset)
    sns.violinplot(data=dataset)
    plt.xlabel('Judicial Docs', fontsize=12)
    plt.ylabel(English_name, fontsize=12)
    plt.title("Volin Charts of "+English_name, fontsize=15)
    plt.savefig('./'+Chinese_name+'1.png')
    plt.show()
    confidenceinterval(dataset_)
    sns.violinplot(data=dataset_)
    plt.xlabel('Judicial Docs', fontsize=12)
    plt.ylabel(English_name, fontsize=12)
    plt.title("Volin Charts of " + English_name, fontsize=15)
    plt.savefig('./' + Chinese_name + '2.png')
    plt.show()
    sns.kdeplot(dataset_,shade=True, color="orange", label="AJJBQK")
    plt.title('Density Plot of '+English_name, fontsize=15)
    plt.legend()
    plt.savefig('./' + Chinese_name + '3.png')
    plt.show()
    return len_


# 日期转换函数,返回datetime类型
def date_change(date_txt):
    if re.match(r'[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日',date_txt):
        fmt = '%Y年%m月%d日'
        time_tuple = time.strptime(date_txt, fmt)
        year, month, day = time_tuple[:3]
        a_date = datetime.date(year, month, day)
        return a_date
    else:
        return False


# 案件信息延迟性，案件发生到立案日期
# 受理日期到结案日期
def del_date(root_node):
    date_dic = {'案件发生时间':'','案件受理时间':'','案件结案时间':''}
    date_list = []
    for node in root_node:
        if node.tag == 'SSJL':
            for subnode in node:
                if subnode.tag == 'SLRQ':
                    SLRQ_txt = subnode.get('value')
                    if date_change(SLRQ_txt):
                        date_dic['案件受理时间']=date_change(SLRQ_txt)
                    break
        if node.tag == 'WW':
            for subnode in node:
                if subnode.tag == 'CPSJ':
                    for subsubnode in subnode:
                        if subsubnode.tag == 'CUS_JANYR':
                            JARQ_txt = subnode.get('value')
                            if date_change(JARQ_txt):
                                date_dic['案件结案时间']=date_change(JARQ_txt)
                    break
        if node.tag == 'CUS_SJ':
            for subnode in node:
                if subnode.tag == 'CUS_JTSJ':
                    tmp_date_txt = subnode.get('value')
                    if date_change(tmp_date_txt):
                        date_list.append(date_change(tmp_date_txt))
    if len(date_list)!=0:
        date_dic['案件发生时间']= min(date_list)

    return date_dic

def date_analysis():
    dic = {'案件信息延迟性':[],'裁判文书延迟性':[]}
    outfile = open('./date.json', 'w', encoding='utf-8')
    del1_list = []
    del2_list = []
    count = 0
    for filepath in path_file.readlines():
        count+=1
        print(count)
        xml_file = etree.parse('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/' + filepath.strip())
        root_node = xml_file.getroot()[0]
        date_dic = del_date(root_node)
        if date_dic['案件受理时间']!='' and date_dic['案件发生时间']!='':
            Expenses_days=(date_dic['案件受理时间']-date_dic['案件发生时间'])
            del1 = Expenses_days.days
            if(1<del1<10000):
                # print(del1,filepath)
                del1_list.append(del1)
        if date_dic['案件结案时间']!='' and date_dic['案件受理时间']!='':
            Expenses_days_=(date_dic['案件结案时间']-date_dic['案件受理时间'])
            del2 = Expenses_days_.days
            if(1<del2<10000):
                # print(del2,filepath)
                del2_list.append(del2)
    dic['案件信息延迟性'] = del1_list
    dic['裁判文书延迟性'] = del2_list
    print(len(dic['案件信息延迟性']),len(dic['裁判文书延迟性']))
    json.dump(dic,outfile,ensure_ascii=False)
    return

def rea_SSMS(wenshu):
    # 案件基本情况
    AJJBQK = wenshu['事实'][0]
    AJJBQK_txt = AJJBQK.get('value')
    AJJBQK_len = len(AJJBQK_txt)
    YGSCD_len, BGBCD_len, CMSSD_len, ZJD_len = 0, 0, 0, 0
    for node in AJJBQK:
        # 原告诉称段
        if node.tag == 'YGSCD':
            YGSCD_txt = node.get('value')
            YGSCD_len = len(YGSCD_txt)
        # 被告辩称段
        elif node.tag == 'BGBCD':
            BGBCD_txt = node.get('value')
            BGBCD_len = len(BGBCD_txt)
        # 查明事实段
        elif node.tag == 'CMSSD':
            CMSSD_txt = node.get('value')
            CMSSD_len = len(CMSSD_txt)
        # 证据段
        elif node.tag == 'ZJD':
            ZJD_txt = node.get('value')
            ZJD_len = len(ZJD_txt)
    print(AJJBQK_len, YGSCD_len, BGBCD_len, CMSSD_len, ZJD_len)
    return  AJJBQK_len, YGSCD_len, BGBCD_len, CMSSD_len, ZJD_len


if __name__=='__main__':
    # plot_show('./date.json','年份','文书数量','裁判文书的时间分布频数图')
    # plot_show('./province.json','省份','文书数量','裁判文书的地域分布频数图')
    # met_analysis(path_file)

    # plot_show_volin('./met.json','案件基本情况','Meticulous of AJJBQK')
    # plot_show_volin('./met.json', '裁判分析过程', 'Meticulous of CPFXGC')
    # plot_show_volin('./met.json', '当事人', 'Meticulous of DSR')

    # date_analysis()
    plot_show_volin('./date.json','案件信息延迟性','Delay of AJXX')
    # plot_show_volin('./date.json', '裁判文书延迟性', 'Delay of CPWS')