import jieba
import re

#去除描述信息中无用的被告，原告，姓名和日期等信息

jieba.setLogLevel('WARN')


class normalizer:
    def __init__(self, stopword_filepath):
        '''
        :param stopword_filepath: 停用词表路径
        :return:
        '''
        self.raw_json_list = []
        self.cut_list = []

        self.data_out = None
        self.stopword_filepath = stopword_filepath

        self.time_sub_pattern = [
                        r'([\d一二三四五六七八九十零]+年|[\d一二三四五六七八九十]+月|周+[\d一二三四五六日末]|[\d一二三四五六七八九十零]+(日|号)|[\d一二三四五六七八九十零]+时|\d+分)+',
        ]
        self.time_sub_replacer = [
            '',
        ]

        self.person_sub_pattern = [
            r'被告人(.)某',
            r'原告(.)称',
            r'证人(.)某',
            r'(.)某',
        ]
        self.person_sub_replacer = [
            '',
            '',
            '',
            '',
        ]

        self.money_sub_pattern = [
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右)*十(余|多|几)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右|几)*百(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右|几)*千(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右|几)*万(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右)*十(余|多)*万(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右)*百(余|多)*万(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(余|多|左右)*千(余|多)*万(余|多)*元(人民币)*',
            r'(人民币)*[几一二两三四五六七八九]*(\d+(\.)?\d*)*(十|百|千)*(余|多|左右)*亿(余|多)*元(人民币)*',
        ]
        self.money_sub_replacer = [
            'm1', #<1000
            'm1',
            'm1',
            'm2',  #<10000
            'm3',  #<100000
            'm4',  #<1000000
            'm5',  #<10000000
            'm6',
            'm7',
        ]

        # self.penalty_sub_pattern = [
        #
        # ]
        # self.penalty_sub_replacer = [
        #
        # ]

        self.stopwordlist = self.read_data_to_list(self.stopword_filepath)

    def read_data_to_list(self, filepath):
        rslt_list = []

        with open(filepath, 'r', encoding='utf8') as fin:
            line = fin.readline()
            while line:
                line = line.strip()
                if line != "":
                    rslt_list.append(line)
                line = fin.readline()

        return rslt_list

    def seg_one_text(self, one_text, filterd_word_len):
        rslt_list = []
        text = one_text
        text = text.replace("\r", "")
        text = text.replace("\n", "")
        for i in range(len(self.time_sub_pattern)):
            text = re.sub(self.time_sub_pattern[i], self.time_sub_replacer[i], text)
        for j in range(len(self.person_sub_pattern)):
            text = re.sub(self.person_sub_pattern[j], self.person_sub_replacer[j], text)
        for k in range(len(self.money_sub_pattern)):
            text = re.sub(self.money_sub_pattern[k], self.money_sub_replacer[k], text)

        tmp_cut_list = [word for word in jieba.lcut(text) if len(word) >= filterd_word_len]
        ###test
        # print(tmp_cut_list)
        for word in tmp_cut_list:

            if word in self.stopwordlist:
                continue
            if re.match(r'^\d+(\.)?\d*$', word) is not None:
                number = float(word)
                if (number < 1000 and number >= 0):
                    rslt_list.append('m1')
                elif (number < 10000 and number >= 1000):
                    rslt_list.append('m2')
                elif (number < 100000 and number >= 10000):
                    rslt_list.append('m3')
                elif (number < 1000000 and number >= 100000):
                    rslt_list.append('m4')
                elif (number < 10000000 and number >= 1000000):
                    rslt_list.append('m5')
                elif (number < 100000000):
                    rslt_list.append('m6')
                elif (number >= 100000000):
                    rslt_list.append('m7')
                continue

            # re.match(r'^(.*?)(县|市|乡|镇|州|村|区|省)$', word)
            elif (re.match(r'^(.*?)(县)$', word) is not None):
                # rslt_list.append('县')
                continue
            elif (re.match(r'^(.*?)(市)$', word) is not None):
                # rslt_list.append('市')
                continue
            elif (re.match(r'^(.*?)(乡)$', word) is not None):
                # rslt_list.append('乡')
                continue
            elif (re.match(r'^(.*?)(镇)$', word) is not None):
                # rslt_list.append('镇')
                continue
            elif (re.match(r'^(.*?)(州)$', word) is not None):
                # rslt_list.append('州')
                continue
            elif (re.match(r'^(.*?)(村)$', word) is not None):
                # rslt_list.append('村')
                continue
            elif (re.match(r'^(.*?)(区)$', word) is not None):
                # rslt_list.append('区')
                continue
            elif (re.match(r'^(.*?)(省)$', word) is not None):
                # rslt_list.append('省')
                continue
            if word != '':
                rslt_list.append(word)
        return rslt_list
