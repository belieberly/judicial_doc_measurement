from xml.etree import ElementTree as etree
import re
import copy_detect
import json

# 测试样例

def text_style_classification_BERT(filepath):
    return 0.9845636

def copy_detect_index(filepath):
    xml_file = etree.parse(filepath)
    root_node = xml_file.getroot()[0]
    for node in root_node:
        if node.tag == 'AJJBQK':
            for subnode in node:
                if subnode.tag == 'YGSCD':
                    YGSCD_txt = subnode.get('value')
                elif subnode.tag == 'BGBCD':
                    BGBCD_txt = subnode.get('value')
                elif subnode.tag == 'CMSSD':
                    CMSSD_txt = subnode.get('value')

    copy1_index1 = copy_detect.long_detect(YGSCD_txt, CMSSD_txt)
    copy1_index2 = copy_detect.long_detect(BGBCD_txt, CMSSD_txt)

    copy2_index1 = copy_detect.levenshtein(YGSCD_txt, CMSSD_txt)
    copy2_index2 = copy_detect.levenshtein(BGBCD_txt, CMSSD_txt)

    copy_index = (copy1_index1 +copy1_index2 +copy2_index1+copy2_index2) /4.0
    return copy_index

file_path = input('输入为评估文件名称').strip()
filepath = 'D:/NJU/final_project/data/example/' + file_path

subject_index = {'抄袭检测':0,'法条合理性':0,'文本风格度量（基于bert的分类）':0}
subject_index['抄袭检测'] = copy_detect_index(filepath)
subject_index['文本风格度量（基于bert的分类）'] = text_style_classification_BERT(filepath)
outfile = '../../report/test.json'
with open(outfile, 'a+', encoding='utf-8') as f:
    json.dump(subject_index, f, ensure_ascii=False)
