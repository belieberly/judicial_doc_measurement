# text style classification

import re
from xml.etree import ElementTree as etree


def preprocess_judicial():
    file_list = open('G:/judicial_data/民事一审案件.tar/民事一审案件/path_min_pan_filter_len.txt', 'r', encoding='utf-8')
    file_out = open('../../data/text_style_classification/sentiment.train.0', 'w', encoding='utf-8')
    count = 0
    for line in file_list.readlines():
        xml_file = etree.parse('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/' + line.strip())
        root_node = xml_file.getroot()[0]
        print(count)
        for node in root_node:
            if node.tag == 'AJJBQK':
                AJJBQK_txt = node.get('value')
                pattern = r',|\.|/|;|\'|`|\[|\]|<|>|？|:|“|”|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| ' \
                          r'|…|（|）|《|》 '
                result_list = re.split(pattern, AJJBQK_txt)
                for i in result_list:
                    if len(i) > 10 and not re.search('[0-9]',i):
                        file_out.write(i + '\n')
                        count += 1
        if count > 35000:
            break
    print('我完成啦')
    file_list.close()
    file_out.close()


def preprocess_news():
    file_input = open('../../data/full_news.csv', 'r', encoding='utf-8')
    file_output = open('../../data/text_style_classification/sentiment.train.1', 'w', encoding='utf-8')
    count = 0
    for line in file_input.readlines():
        txt = line.split(',', 2)[1]
        pattern = r',|\.|/|;|\'|`|\[|\]|<|>|？|:|“|”|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| ' \
                  r'|…|（|） '
        result_list = re.split(pattern, txt)
        # print(result_list)
        for i in result_list:
            if len(i) > 10 and len(i) < 30 and not re.search('[0-9]',i):
                file_output.write(i + '\n')
                count += 1
        print(count)
        if count > 35000:
            break
    print('我也完成啦')
if __name__=='__main__':
    preprocess_judicial()
    preprocess_news()