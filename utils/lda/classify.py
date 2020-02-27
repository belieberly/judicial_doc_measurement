from gensim import corpora, models
import json
from tqdm import tqdm

lda = models.LdaModel.load('./lda_model/mylda_v2')
dict_1 = corpora.Dictionary.load('./lda_model/dict_v2')
tfidf = models.TfidfModel.load("./lda_model/my_model.tfidf")
dict_corpora = corpora.mmcorpus.MmCorpus('ths_corpora.mm')
corpus_tfidf = tfidf[dict_corpora]

dict = {}
for num in range(78):
    dict[num] = []

doc_num = 1

with tqdm(corpus_tfidf) as pbar:
    for doc in pbar:
        vector = lda[doc]
        topic = sorted(vector, key=lambda item: -item[1])[0]
        pbar.set_description("Processing %d" % doc_num)
        dict[topic[0]].append(doc_num)
        doc_num += 1
with open("./lda-docs-data.json", "w")as f:
    print(dict)
    f.write(json.dumps(dict))
    print('lda-docs-data写入成功')

