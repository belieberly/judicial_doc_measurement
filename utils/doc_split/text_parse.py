import re

inputf1 = open('./data/example.txt', 'r', encoding='utf-8')
inputf2 = open('./data/example.txt', 'r', encoding='utf-8')
text1 = inputf1.readlines()
text2 = inputf2.readlines()


def split_txt(doc_txt: list):
    flag_list = [[] for i in range(len(doc_txt))]
    for i in range(len(doc_txt)):
        doc_txt[i] = doc_txt[i].strip()
        if re.match(r'.*民事判决书$', doc_txt[i]):
            flag_list[i].append('pagename')
        if re.match(r'^发布日期：.*浏览：[0-9]*次$', doc_txt[i]):
            flag_list[i].append('information')
        if re.match(r'.*法院$', doc_txt[i]) and len(doc_txt[i]) < 20:
            flag_list[i].append('title.court_name')
        if re.match(r'^民[\s]?事[\s]?判[\s]?决[\s]?书[\s]?$', doc_txt[i]):
            flag_list[i].append('title.doc_type')
        if re.match(r'（[0-9]{4}）[\w\u4e00-\u9fcc]?[0-9]+[\w\u4e00-\u9fcc]{2}[0-9]+号', doc_txt[i]):
            flag_list[i].append('title.doc_num')
        if re.match(r'^(原告|被告|负责人|委托诉讼代理人|负责人|上诉人|被上诉人)(?!.*本案现已(审理)*(终结)*).*', doc_txt[i]):
            flag_list[i].append('head.basic_situation')
        if re.match(r'原告[\w\u4e00-\u9fcc]+与被告[\w\u4e00-\u9fcc]+.*本院.*本案现已审理终结。$', doc_txt[i]):
            flag_list[i].append('head.summary')
        if re.match(r'^原告[\w\u4e00-\u9fcc]*(诉称|称|请求)*.*被告(?!.*本案现已(审理)*(终结)*).*', doc_txt[i]):
            flag_list[i].append('facts.yuangao')
        if re.match(r'^被告[\w\u4e00-\u9fcc]*(未到庭|未[\w\u4e00-\u9fcc]*提交书面答辩|辩称)', doc_txt[i]):
            flag_list[i].append('facts.beigao')
        if re.search(r'(经[\w\u4e00-\u9fcc]*审理查明|另查明)', doc_txt[i]):
            flag_list[i].append('facts.fayuan')
        if re.match(r'^[\w\u4e00-\u9fcc]{0,5}本院认为', doc_txt[i]):
            flag_list[i].append('analysis')
        if re.search(r'依照.*[第.*条]+.*判决如下.*', doc_txt[i]):
            flag_list[i].append('law_dependence')
        if re.match(r'^上述具有履行内容的条款，均于本判决生效之日起[\w\u4e00-\u9fcc]+内履行', doc_txt[i]):
            flag_list[i].append('verdict')
        if re.match(r'^如果未按本判决指定的期间履行[\w\u4e00-\u9fcc]+义务，应当依照', doc_txt[i]):
            flag_list[i].append('verdict')
        if re.search(r'案件受理费[0-9]+元.*[.*费[0-9]元]*', doc_txt[i]):
            flag_list[i].append('tail.charge')
        if re.match(r'^如不服本判决，可在判决书送达之日起十五日内，向本院递交上诉状，并按[\w\u4e00-\u9fcc]+提出副本，上诉于', doc_txt[i]):
            flag_list[i].append('tail.notification')
        if re.match(r'^(审[\s]?判[\s]?长[\s]?|人民陪审员|书[\s]?记[\s]?员[\s]?|法官助理)', doc_txt[i]):
            flag_list[i].append('inscription.person')
        if re.match(r'^[一二三四五六七八九十〇]{4}年[一二三四五六七八九十〇]{1,2}月[一二三四五六七八九十〇]{1,2}日', doc_txt[i]):
            flag_list[i].append('inscription.record_date')
        if re.match(r'^附.*法律', doc_txt[i]):
            flag_list[i].append('appendix')
    # 增加规则部分 上次同步测试1258
    analysis_pos = 0
    summary_pos = 0
    for j in range(0, len(doc_txt)):
        if 'analysis' in flag_list[j]:
            analysis_pos = j
        if 'head.summary' in flag_list[j]:
            summary_pos = j

    # 处理所有没有标签的数据
    for i in range(len(doc_txt)):
        if len(flag_list[i]) == 0:
            print('没有标签')
            if analysis_pos != 0:
                if 5 < i < analysis_pos and len(flag_list[i - 1]) == 1 and flag_list[i - 1][0] == 'facts.fayuan' and \
                        re.search(r'(查|查明|查证)', doc_txt[i]):
                    print('增加标签facts.fayuan')
                    flag_list[i].append('facts.fayuan')
            if i > 1 and flag_list[i - 1][0] == 'appendix':
                print('增加标签appendix')
                flag_list[i].append('appendix')
        if len(flag_list[i]) > 1:
            print('多标签')
            if 'head.basic_situation' in flag_list[i]:
                tmp_pos = flag_list[i].index('head.basic_situation')
                if i > summary_pos:
                    flag_list[i].pop(tmp_pos)
                    print('删除标签head.basic_situation')
    return doc_txt, flag_list


class DocPart:
    def __init__(self, content_str: str, label: str = "", suggestion: str = "无修改意见"):
        self.label = label
        self.content_str = content_str
        self.suggestion = suggestion


# 为前端准备对象
def doc2list(doc_txt, flag_list):
    doc_part_list = []
    for i in range(len(doc_txt)):
        doc_part_tmp = DocPart(flag_list[i], doc_txt[i])
        doc_part_list.append(doc_part_tmp)
    return doc_part_list


# split_txt(text1)
split_txt(text2)
