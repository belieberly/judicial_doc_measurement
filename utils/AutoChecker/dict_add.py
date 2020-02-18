
# 加入司法领域词典
def dic_add(add_file_path, target_file_path):
    with open(add_file_path, 'r') as add_file:
        with open(target_file_path, 'a+') as target_file:
            # target_file.read()
            for line in add_file.readlines():
                target_file.write(line.strip() + ' ' + str(50) + ' ' + 'n' + '\n')



dic_add('./dics/judicial_words.txt', '../../venv/Lib/site-packages/jieba/dict.txt')