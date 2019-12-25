# -*- coding: cp936 -*-
import requests
from bs4 import BeautifulSoup
import base64
import web
import time
import random
global data,user,pwd,code,jpg
headers = {           
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
           }

urls = (
'/blog/\d+', 'blog',
'/(.*)', 'hello'
)

app = web.application(urls, globals())
 
class hello:

    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
    def GET(self, name):
        global v,vg,e
        global s
        s=requests.Session()
        v,vg,e=downlaod_code(s)
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
<form action="/blog/123" method="POST">
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
                                <div class="re_min">
                                    <span class="icon_vf_code"></span>
                                    <input class="input01"  class="login_btn" id="code" name="code" type="text" placeholder="请输入验证码" onkeyup="chkCode(this)"/>
                                    <img src='''+jpg+'''  align="right">
                                    
                                </div>
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

#获得账号 密码 验证码 
class blog:
        def POST(self):
            data = web.input()
            user=data['username']
            pwd=data['password']
            code=data['code']
            user=jiami(user)
            pwd=jiami(pwd)
            code=jiami(code)
             #登陆
            r=login(v,vg,e,s,code,user,pwd)
            k=s.get(url='http://jw.huse.cn/JWXS/xsMenu.aspx',headers=headers)
            soup = BeautifulSoup(k.text,'lxml')
        
            #找id
            try:
                path = soup.find(id='5')['path']
            except BaseException:
                r = BeautifulSoup(r.text,'lxml')
                r=r.find(id='Lerror').string
                return ''' <!DOCTYPE html>
            <html><head>  <meta charset="utf-8">
        <link rel="icon" href="data:;base64,=">
        <title>挂科一时爽 一直挂科一直爽</title>
        </head><body>'''+r+'''</body></html>'''
            url='http://jw.huse.cn/JWXS/'+path
            k=s.get(url=url,headers=headers)
            k = BeautifulSoup(k.text,'lxml')
            k=str(k)
            k=k.replace('''<title>
</title>''','<meta charset="utf-8">')
            k=k.replace('<div id="ok" style="overflow:auto; height:360">',' ')
            return k

def downlaod_code(s):
    global jpg
    jpg=(str)(random.randint(0,9))
    url='http://jw.huse.cn/'
    r=s.get(url=url,headers=headers)
    #验证码获取
    soup = BeautifulSoup(r.text,'lxml')
    image_src='http://jw.huse.cn/other/CheckCode.aspx?datetime=az'
    r_image=s.get(image_src,headers=headers)
    n=random.randint(0,1000)
    n=str(n)
    jpg='static/code'+n+'.jpg'
    with open(jpg,'wb') as fp:
        fp.write(r_image.content) 
    #参数获取
    __VIEWSTATE=soup.find('input',id="__VIEWSTATE")['value']
    __VIEWSTATEGENERATOR=soup.find('input',id="__VIEWSTATEGENERATOR")['value']
    __EVENTVALIDATION=soup.find('input',id='__EVENTVALIDATION')['value']
    return __VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION


    #登录
def login(v,vg,e,s,code,user,pwd):
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
if __name__ == "__main__":
    app.run()

