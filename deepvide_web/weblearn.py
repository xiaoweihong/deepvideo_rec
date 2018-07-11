#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/7 下午7:02
# @Author : xiaowei
# @Site : 
# @File : weblearn.py
# @Software: PyCharm
import web
import base64
import requests
import json
render=web.template.render("templates/")


urls=(
    '/','index',
    '/local/','det_local'
)


class index:

    def GET(self,name=None):
        return render.index()

    def POST(self):

        pass


class det_local:

    def GET(self):
        return 123

    def POST(self):
        data=web.input(myfile={})
        result={"data":None,"image":None}
        b64=base64.b64encode(data['local_image'])
        b64=b64.decode('utf-8')
        #print(b64)
        s=get_result(b64)
        result["data"]=s
        result["image"]=b64
        return json.dumps(result)


def get_result(b64):
    url="http://192.168.6.121:6501/rec/image"
    request_string={"Context":{"SessionId":"deepvide_web rec image","Type":1,"Functions":[100,101,102,103,104,105,106,107,108,200,201,202,203,204,300,400]},"Image":{"Data":{"BinData":b64}}}
    jstring=json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    result=requests.post(url,data=jstring,headers=headers).json()
    return result


if __name__=='__main__':
    app = web.application(urls,globals(),autoreload=True)
    app.run()