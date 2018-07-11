#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/11 下午2:10
# @Author : xiaowei
# @Site : 
# @File : s.py
# @Software: PyCharm
import cv2 as cv
import numpy as np
import requests
import urllib
import json

request_url="http://192.168.6.27:6501/rec/image"

pic_url="http://192.168.6.121:8501/api/file/1,0421d01dc98117"

def url_to_image(url):
    resp=urllib.request.urlopen(url)
    image=np.asarray(bytearray(resp.read()),dtype="uint8")
    image=cv.imdecode(image,cv.IMREAD_COLOR)
    return image

request_string={"Context":{"SessionId":"deepvide_web rec image","Type":1,"Functions":[100,101,102,103,104,105,106,107,108,200,201,202,203,204,300,400]},"Image":{"Data":{"URI":pic_url}}}


data=json.dumps(request_string)

response=requests.post(request_url,data=data).json()

if "Vehicles" not in response["Result"]:
    print("没有识别到机动车")
    exit(400)

vehicles_list=response["Result"]["Vehicles"]

## 本地读取图片
#img=cv.imread("car.jpeg",cv.IMREAD_UNCHANGED)

## 网络读取图片
img=url_to_image(pic_url)

print("识别到{}辆车".format(len(vehicles_list)))

for vehicle in vehicles_list:
    #print(vehicle)
    vehicle_x=vehicle["Img"]["Cutboard"]["X"]
    vehicle_y=vehicle["Img"]["Cutboard"]["Y"]
    vehicle_width=vehicle["Img"]["Cutboard"]["Width"]
    vehicle_height=vehicle["Img"]["Cutboard"]["Height"]
    cv.rectangle(img,(vehicle_x,vehicle_y),(vehicle_x+vehicle_width,vehicle_y+vehicle_height),(255,0,0),2,4,0)

cv.imdecode()
# print(url_to_image(pic_url))
