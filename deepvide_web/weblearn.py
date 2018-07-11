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
import cv2 as cv
import numpy as np
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
        print(b64)
        s=get_result(b64)
        print(s)
        result["data"]=s
        b64_rec=opencv_rec_image(b64,result)
        result["image"]=b64_rec
        print(result,type(result))
        return json.dumps(result)


def get_result(b64):
    url="http://39.106.146.155:6501/rec/image"
    request_string={"Context":{"SessionId":"deepvide_web rec image","Type":1,"Functions":[100,101,102,103,104,105,106,107,108,200,201,202,203,204,300,400]},"Image":{"Data":{"BinData":b64}}}
    jstring=json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    result=requests.post(url,data=jstring,headers=headers).json()
    return result

def opencv_rec_image(b64data,result):
    imgData = base64.b64decode(b64data)
    nparr = np.fromstring(imgData, np.uint8)
    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)
    if "Vehicles" not in result["data"]["Result"]:
        print("没有识别到机动车")
        exit(400)

    vehicles_list = result["data"]["Result"]["Vehicles"]
    print("识别到{}辆车".format(len(vehicles_list)))

    for vehicle in vehicles_list:
        print(vehicle)
        vehicle_x = vehicle["Img"]["Cutboard"]["X"]
        vehicle_y = vehicle["Img"]["Cutboard"]["Y"]
        vehicle_width = vehicle["Img"]["Cutboard"]["Width"]
        vehicle_height = vehicle["Img"]["Cutboard"]["Height"]
        cv.rectangle(img_np, (vehicle_x, vehicle_y), (vehicle_x + vehicle_width, vehicle_y + vehicle_height), (255, 0, 0),
                     2, 4, 0)
    image = cv.imencode('.jpg', img_np)[1]
    s = str(base64.b64encode(image).decode("utf-8"))
    #print(s)
    return s


if __name__=='__main__':
    app = web.application(urls,globals(),autoreload=True)
    app.run()