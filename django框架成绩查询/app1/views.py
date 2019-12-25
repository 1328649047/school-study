from django.shortcuts import render
from django.http import HttpResponse
from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
import base64
import time
import random
global data,user,pwd,code,jpg,v,vg,e
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
           }
# Create your views here.

def hello(request):
    if request.method=='GET':
        global v,vg,e
        v, vg, e = downlaod_code()
        return  render(request, "login.html")
    if request.method=='POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        code = ''
        user = jiami(user)
        pwd = jiami(pwd)
        code = jiami(code)
        # 登陆
        k = login1(v, vg, e, code, user, pwd)
        return HttpResponse(k)
def downlaod_code():
    jpg=(str)(random.randint(0,9))
    url='http://jw.huse.cn/'
    r=requests.get(url=url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    #参数获取
    __VIEWSTATE=soup.find('input',id="__VIEWSTATE")['value']
    __VIEWSTATEGENERATOR=soup.find('input',id="__VIEWSTATEGENERATOR")['value']
    __EVENTVALIDATION=soup.find('input',id='__EVENTVALIDATION')['value']
    return __VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION


    #登录
def login1(v,vg,e,code,user,pwd):
    q = requests.Session()
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
    r=q.post(url=post_url,headers=headers,data=formdata)
    k = q.get(url='http://jw.huse.cn/JWXS/xsMenu.aspx', headers=headers)
    soup = BeautifulSoup(k.text, 'lxml')
    # 找id
    try:
        path = soup.find(id='5')['path']
    except BaseException:
        erro = BeautifulSoup(r.text, 'lxml')
        msg = erro.find(id='Lerror').string
        return HttpResponse(''' <!DOCTYPE html>
                        <html><head>  <meta charset="utf-8">
                    <link rel="icon" href="data:;base64,=">
                    <title>挂科一时爽 一直挂科一直爽</title>
                    </head><body>''' + msg + '''</body></html>''')
    url = 'http://jw.huse.cn/JWXS/' + path
    k = q.get(url=url, headers=headers)
    k = BeautifulSoup(k.text, 'lxml')
    k = str(k)
    k = k.replace('''<title>
            </title>''', '<meta charset="utf-8">')
    k = k.replace('<div id="ok" style="overflow:auto; height:360">', ' ')
    return k

    #加密传输
def jiami(code):
        code=code.encode('utf-8')
        code=base64.b32encode(code)
        code=code.decode('utf-8')
        code=code.replace("=", "")
        return code
