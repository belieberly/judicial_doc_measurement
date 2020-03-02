#客观度量指标
objective_index = {'细致性': {'参诉人信息细致性': 'met_CSR', '事实部分细致性': 'met_AJJBQK', '理由部分细致性': 'met_CPFXGC'},
                   '延迟性': {'案件信息延迟性': 'del_date', '裁判文书延迟性': 'del_date'},
                   '真实性': {'案由信息类别规范性': 'aut_AY', '裁判依据引用规范性': 'aut_CPYJ'},
                   '完整性': {'判决内容说明完整性': 'com_PJNR', '诉费承担说明完整性': 'com_SFCD'},
                   '一致性': {'数字使用一致性': 'con_num_*', '标点符号使用一致性': 'con_pun_*'},
                   '易读性': {'事实描述部分简明性': 'rea_SSMS', '争议焦点条理性': 'rea_ZYJD'},
                   '准确性': {'构成事项准确性': 'acc_GCSX', '审理经过': 'acc_SLJG', '参诉人信息': 'acc_DSR'}}
#主观度量指标
subjective_index = {'语言风格':{'语言风格辨析':'','情感倾向性':'','语言重构检测':''},
                    '法条合理性':{'基于相似案例':'','基于预测模型':''}}

#细致性阈值
met_CSR_threshold = 7
met_AJJBQK_threshold = 5
met_CPFXGC_threshold = 8
#细致性每项得分
met_subscore = 5

#错误检测分项总分
copy_detect_score = 20
# 错误检测相似度阈值
copy_detect_threshold = 0.7
#错误检测每句扣分
copy_detect_fault = 5


#文书信息延迟性得分
del_date_score = 10
del_date_subsocre1=5
del_date_subscore2 = 3
del_date_subscore3 = 1

#案件信息延迟性阈值
del_date_AJXX_threshold1 = 1000
del_date_AJXX_threshold2 = 3000

#文书信息延迟性阈值
del_date_WSXX_threshold1= 100
del_date_WSXX_threshold2= 200


#案由信息类别规范性
aut_AY_score = 5

#裁判依据引用规范性
aut_CPYJ_score = 5

#标点符号使用一致性
con_pun_score = 10

#数字使用一致性
con_num_score = 10

#判决内容说明完整性
com_PJNR_score = 5

#诉费承担说明完整性
com_SFCD_score = 5


