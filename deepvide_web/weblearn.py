#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/7 下午7:02
# @Author : xiaowei
# @Site : 
# @File : weblearn.py
# @Software: PyCharm
import web
import base64
import json
from tools import image_handler

# url = "http://192.168.2.117:6501/rec/image"
url = "http://211.103.220.74:8014/rec/image"

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

        result_data=image_handler.get_request_result(b64,url)


        result["data"]=result_data

        b64_rec=image_handler.opencv_rec_image(b64,result)

        result["image"]=b64_rec

        return json.dumps(result)




if __name__=='__main__':
    app = web.application(urls,globals(),autoreload=True)
    app.run()