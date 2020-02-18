import traceback

from flask import Flask, render_template, request, Response

from utils.doc_split import text_parse
#
# from utils.AutoChecker import AutoChecker4Chinese

import pymysql

import json

import datetime



app = Flask(__name__)



@app.route('/')
def login():
    return render_template('login.html')


@app.route('/demo')
def demo():
    inputf1 = open('./data/example.txt', 'r', encoding='utf-8')
    # inputf2 = open('./data/example.txt', 'r', encoding='utf-8')
    text1 = inputf1.readlines()
    # text2 = inputf2.readlines()
    doc_txt,flag_list = text_parse.split_txt(text1)
    # for content in doc_txt:
    #     AutoChecker4Chinese.err_correct(content)
    return render_template('split_demo.html', doc_txt = doc_txt, flag_list = flag_list)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/regist')
def click_regist():
    return render_template('regist.html')



def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
    # 把用户名和密码注册到数据库中
    user_account = request.args.get('user')
    user_pwd1 = request.args.get('password1')
    user_pwd2 = request.args.get('password2')
    user_org = request.args.get('organization')
    user_job = request.args.get('job')
    user_name = request.args.get('name')
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "ilynsm77", "log_in")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if(user_pwd1!=user_pwd2):
        return '两次输入密码不一致'
    # SQL 插入语句
    # sql = "INSERT INTO user(user, pwd, nick_name) VALUES (" + request.args.get('user') + ", " + request.args.get('password') + ")"
    sql = "INSERT INTO user(user_account, pwd, user_org,user_job,user_name, creattime) VALUES ('%s','%s','%s', '%s', '%s', '%s')" % (
        user_account, user_pwd1, user_org,user_job,user_name, dt)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        return render_template('login.html')
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()


# 获取登录参数及处理
@app.route('/login')
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "ilynsm77", "log_in")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    user_account = request.args.get('user')
    user_pwd = request.args.get('password')

    sql = "select * from user where user_account='%s' and pwd='%s'" % (user_account, user_pwd)
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results) == 1:
            data = {}
            data["code"] = '登录成功'
            print(data['code'])
            # for row in results:
            #     data["id"] = row[0]
            #     data["pwd"] = row[1]
            #     data["name"] = row[2]
            #     data["time"] = row[3]
            # return json.dumps(data)
            return render_template('index.html')
        else:
            return render_template('login.html',errMessages="用户名或者密码错误")
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        return '登陆失败'
    # 关闭数据库连接
    db.close()



if __name__ == '__main__':
    app.run()
