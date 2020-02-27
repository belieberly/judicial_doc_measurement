import os
import traceback

from flask import Flask, render_template, request, Response, jsonify
import logging

from utils.doc_split import text_parse
#
# from utils.AutoChecker import AutoChecker4Chinese


import pymysql

import json

import datetime

# <<<<<<< HEAD
#
# =======
# >>>>>>> 7803732dcc1e567cb089f99bcc5e016b48d577ae
app = Flask(__name__)

DB_IP = "localhost"
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "log_in"


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/demo')
def demo():
    inputf1 = open('./data/example.txt', 'r', encoding='utf-8')
    # inputf2 = open('./data/example.txt', 'r', encoding='utf-8')
    text1 = inputf1.readlines()
    # text2 = inputf2.readlines()
    doc_txt, flag_list = text_parse.split_txt(text1)
    # for content in doc_txt:
    #     AutoChecker4Chinese.err_correct(content)
    return render_template('split_demo.html', doc_txt=doc_txt, flag_list=flag_list)


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
@app.route('/regist/registuser', methods=['GET', 'POST'])
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
    db = pymysql.connect(DB_IP, DB_USER, DB_PASS, DB_NAME)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    if (user_pwd1 != user_pwd2):
        return '两次输入密码不一致'
    # SQL 插入语句
    # sql = "INSERT INTO user(user, pwd, nick_name) VALUES (" + request.args.get('user') + ", " + request.args.get('password') + ")"
    sql = "INSERT INTO user(user_account, pwd, user_org,user_job,user_name, creattime) VALUES ('%s','%s','%s', '%s', '%s', '%s')" % (
        user_account, user_pwd1, user_org, user_job, user_name, dt)
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
    db = pymysql.connect(DB_IP, DB_USER, DB_PASS, DB_NAME)
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
            return render_template('login.html', errMessages="用户名或者密码错误")
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
        return '登陆失败'
    # 关闭数据库连接
    db.close()


UPLOAD_FOLDER = 'upload_files/'
# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = set(
    ['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'ppt', 'pptx', 'doc', 'docx', 'csv', 'sql', 'py',
     'rar','xml'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/main/list',methods=['POST','GET'])
# def list_fun():
#

@app.route('/taskinfo_upload', methods=['Post','GET'])
def taskINfo_upload_fun():
    if request.method == 'POST':
        # 上传文件的键名是file
        print('request.files')
        print(request.files)
        if 'file' not in request.files:

            logging.debugp('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        # 获取文件对象
        file = request.files['file']
        # 若用户没有选择文件就提交，提示‘No selected file’
        if file.filename == '':
            logging.debug('No selected file')
            return jsonify({'code': -1, 'filename':'', 'msg':'No selected file'})
        else:
            print('filename')
            print(file.filename)
            try:
                if file and allowed_file(file.filename):
                    origin_file_name = file.filename
                    logging.debug('filename is %s' % origin_file_name)
                    file_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER)
                    print(file_dir)
                    if os.path.exists(file_dir):
                        logging.debug('%s path exist' % file_dir)
                        print('文件存在')
                        pass
                    else:
                        logging.debug('%s path not exist' % file_dir)
                        print('新建文件')
                        os.makedirs(file_dir)
                    file.save(os.path.join(file_dir, file.filename))
                    print('文件存储')
                    return jsonify({'code': 0, 'filename': origin_file_name, 'msg': 'save successfully'})
                else:
                    logging.debug('%s not allowed' % file.filename)
                    print('文件格式不支持')
                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                logging.debug(e)
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


if __name__ == '__main__':
    app.run()
