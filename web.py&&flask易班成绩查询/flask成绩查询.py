from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import base64
import web
import time
import random
global data,user,pwd,code,jpg,s
app = Flask(__name__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
           }

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        global s
        s = requests.Session()
        v, vg, e = downlaod_code(s)
        return '''<!DOCTYPE html>
        <html>
        	<head>
        		<meta charset="UTF-8">
        		<meta name="viewport" content="initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        		<title>湖南科技学院易班成绩查询网站</title>
        		<link rel="icon" href="data:image/ico;base64,aWNv">
        		<link rel="stylesheet" href="static/css/base.css" />
        	</head>
        	<body>
        <form action="/" method="POST">
        		<div class="bg_bank">
        <div class="re_min_infor">
        	    <div class="re_logo" class=""><img src="static/img/logo.png"></div>
        			    <div class="bg_color">
                                        <div class="re_min">
                                            <span class="icon_phone"></span>
                                            <input class="input01" id="phone" name="username" type="text" placeholder="学号"  /><div id="div1"></div>
                                        </div>
                                        <div class="re_min">
                                            <span class="icon_passwarde"></span>
                                            <input class="input01"  id="password" name="password" type="password" placeholder="密码" />

                                        </div>			
 
                                        <input name="v"  type="text" style="display:none"  value="'''+v+'''"/>
                                        <input name="vg" type="text" style="display:none" value="'''+vg+'''"/>
                                        <input name="e" type="text" style="display:none" value="'''+e+'''"/>
                                    </div>
                                    <div class="re_regist">
                                        <input class="btn_regist" id="login"  type="submit" value="登录">
        	                        </div> 
        		  </div>
        		</div>

        		<script type="text/javascript" src="static/js/jquery-1.11.3.min.js" ></script>
        		<script type="text/javascript" src="static/js/index.js" ></script>
        </form>
        	</body>
        </html>'''
    else:
        q = requests.Session()
        user = request.form.get('username')
        pwd = request.form.get('password')
        code=''
        v = request.form.get('v')
        vg = request.form.get('vg')
        e = request.form.get('e')
        user = jiami(user)
        pwd = jiami(pwd)
        code = jiami(code)
        # 登陆
        r = login1(v, vg, e, q, code, user, pwd)
        k = q.get(url='http://jw.huse.cn/JWXS/xsMenu.aspx', headers=headers)
        soup = BeautifulSoup(k.text, 'lxml')

        # 找id
        try:
            path = soup.find(id='5')['path']
        except BaseException:
            r = BeautifulSoup(r.text, 'lxml')
            r = r.find(id='Lerror').string
            return ''' <!DOCTYPE html>
            <html><head>  <meta charset="utf-8">
        <link rel="icon" href="data:;base64,=">
        <title>挂科一时爽 一直挂科一直爽</title>
        </head><body>''' + r + '''</body></html>'''
        url = 'http://jw.huse.cn/JWXS/' + path
        k = q.get(url=url, headers=headers)
        k = BeautifulSoup(k.text, 'lxml')
        k = str(k)
        k = k.replace('''<title>
</title>''', '<meta charset="utf-8">')
        k = k.replace('<div id="ok" style="overflow:auto; height:360">', ' ')
        return k

def downlaod_code(s):
    global jpg
    jpg=(str)(random.randint(0,9))
    url='http://jw.huse.cn/'
    r=s.get(url=url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    #参数获取
    __VIEWSTATE=soup.find('input',id="__VIEWSTATE")['value']
    __VIEWSTATEGENERATOR=soup.find('input',id="__VIEWSTATEGENERATOR")['value']
    __EVENTVALIDATION=soup.find('input',id='__EVENTVALIDATION')['value']
    return __VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION


    #登录
def login1(v,vg,e,s,code,user,pwd):
    post_url='http://jw.huse.cn'
    formdata={
        '__VIEWSTATE':v,
        '__VIEWSTATEGENERATOR':vg,
        '__EVENTVALIDATION':e,
        'cmdok':'',
        'PWD':pwd,
        'Account':user,
        'CheckCode':code,
        }
    r=s.post(url=post_url,headers=headers,data=formdata)
    return r

    #加密传输
def jiami(code):
        code=code.encode('utf-8')
        code=base64.b32encode(code)
        code=code.decode('utf-8')
        code=code.replace("=", "")
        return code

if __name__=='__main__':
    app.run(debug=app.config['DEBUG'], threaded=True)
