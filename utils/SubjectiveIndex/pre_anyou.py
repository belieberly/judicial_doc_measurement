# 生成案由xml结构

import re
import xml.etree.ElementTree as ET

input_f = open('../../data/raw_AY.txt', 'r', encoding='utf-8')
AY_dict = {}
first_index = []
second_index = []
third_index = []
fourth_index = []
lines = input_f.readlines()
print(len(lines))
for i in range(len(lines)):
    if re.match(r'第.部分.*', lines[i]):
        first_index.append(i)
    if re.match(r'[一|二|三|四|五|六|七|八|九|十]{1,2}、.*', lines[i]):
        second_index.append(i)
    if re.match(r'[1234567890]{1,3}、.*', lines[i]):
        third_index.append(i)
    if re.match(r'（[1234567890]{1,2}）.*', lines[i]):
        fourth_index.append(i)
print(first_index)

print(second_index)
print(third_index)
print(fourth_index)

root = ET.Element('AY')
root.attrib['title'] = '案由列表'
root.attrib['level'] = '0'

for i in first_index:
    label = lines[i].split('部分 ')[1].strip()
    tmp = ET.SubElement(root, 'first-label')
    tmp.attrib['label'] = label
    tmp.attrib['level'] = '1'

first_index.append(853)
second_index.append(853)
third_index.append(853)
fourth_index.append(853)
count = 0
while count < 10:
    root_node = root[count]
    start = first_index[count]
    end = first_index[count + 1]
    print('start:' + str(start), 'end:' + str(end))
    for i in range(start, end):
        if re.match(r'[一|二|三|四|五|六|七|八|九|十]{1,2}、.*', lines[i]):
            label = lines[i].split('、', 2)[1].strip()
            tmp_node = ET.SubElement(root_node, 'second_label')
            tmp_node.attrib['label'] = label
            tmp_node.attrib['level'] = '2'
            end1 = min(end,second_index[second_index.index(i)+1])
            for j in range(i,end1):
                if re.match(r'[1234567890]{1,3}、.*', lines[j]):
                    tmp_subnode = ET.SubElement(tmp_node, 'third_label')
                    sublabel = lines[j].split('、', 2)[1].strip()
                    tmp_subnode.attrib['label'] = sublabel
                    tmp_subnode.attrib['level'] = '3'
                    end2 = min(end1,third_index[third_index.index(j)+1])
                    for m in range(j, end2):
                        if re.match(r'（[1234567890]{1,2}）.*', lines[m]):
                            tmp_ssubnode = ET.SubElement(tmp_subnode, 'fourth_label')
                            ssublabel = lines[m].split('）', 2)[1].strip()
                            tmp_ssubnode.attrib['label'] = ssublabel
                            tmp_ssubnode.attrib['level'] = '4'
    count += 1
print(len(second_index))




# 先构造一个 ElementTree 以便使用其 write 方法
tree = ET.ElementTree(root)
tree.write('a.xml', encoding='UTF-8')
# xml_str = ET.tostring(root, encoding='utf-8')
# print(xml_str)
# input_f.close()
