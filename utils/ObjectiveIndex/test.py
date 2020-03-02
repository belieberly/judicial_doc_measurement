if __name__=='__main__':
    file = open('G:/judicial_data/民事一审案件.tar/民事一审案件/msys_all/100024.xml','r',encoding = 'utf-8')
    for line in file.readlines():
        print(line)