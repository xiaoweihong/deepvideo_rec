#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/11 下午11:33
# @Author : xiaowei
# @Site : 
# @File : image_handler.py
# @Software: PyCharm

import base64
import requests
import json
import cv2 as cv
import numpy as np
import logging
from PIL import Image
from io import BytesIO

logging.basicConfig(
            format='%(asctime)s,%(msecs)05.1f %(filename)s(%(funcName)s):%(lineno)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)


def get_request_result(image_b64,rec_url):

    request_string = {"Context": {"SessionId": "deepvide_web rec image", "Type": 1,
                                  "Functions": [100, 101, 102, 103, 104, 105, 106, 107, 108, 200, 201, 202, 203, 204,
                                                300, 400]}, "Image": {"Data": {"BinData": image_b64}}}
    jstring = json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4'
                      ' Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) '
                      'Chrome/18.0.1025.166 Mobile Safari/535.19'}
    result = requests.post(rec_url, data=jstring, headers=headers).json()
    #logging.debug(result)
    return result


def opencv_rec_image(b64data,data_result):

    rec_result={
        "image_base64_str":None,
        "rec_result":{
            "vehicles":None,
            "pedestrianp":None,
            "nonmotorvehicles":None
        }
    }

    object_color = {
        "vehicles": (255, 0, 0),
        "pedestrianp": (0, 255, 0),
        "nonmotorvehicles": (0, 0, 255),
    }

    imgData = base64.b64decode(b64data)
    nparr = np.fromstring(imgData, np.uint8)

    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)

    vehicles_list = get_object_list("Vehicles",data_result)

    pedestrianp_list=get_object_list("Pedestrian",data_result)

    nonnotorvehicles_list=get_object_list("NonMotorVehicles",data_result)
    image = cv.imencode('.jpg', img_np)[1]
    rec_result["image_base64_str"] = str(base64.b64encode(image).decode("utf-8"))
    if vehicles_list is not None:
        logging.debug("识别到{}辆车".format(len(vehicles_list)))
        rec_result["rec_result"]["vehicles"]=len(vehicles_list)
        rec_result["image_base64_str"]=rec_image(vehicles_list,img_np,object_color["vehicles"])

    if pedestrianp_list is not None:
        logging.debug("识别到{}个行人".format(len(pedestrianp_list)))
        rec_result["rec_result"]["pedestrianp"] = len(pedestrianp_list)
        rec_result["image_base64_str"] = rec_image(pedestrianp_list, img_np,object_color["pedestrianp"])

    if nonnotorvehicles_list is not None:
        logging.debug("识别到{}个非机动车".format(len(nonnotorvehicles_list)))
        rec_result["rec_result"]["nonmotorvehicles"] = len(nonnotorvehicles_list)
        rec_result["image_base64_str"] = rec_image(nonnotorvehicles_list, img_np,object_color["nonmotorvehicles"])

    return rec_result


def get_object_list(object,data_result):
    object_dict={
        "Vehicles":"机动车",
        "Pedestrian":"行人",
        "NonMotorVehicles":"非机动车"
    }
    if object in data_result["data"]["Result"]:
        object_list=data_result["data"]["Result"][object]
        return object_list

    else:
        logging.debug("没有检测到{}目标".format(object_dict[object]))


def rec_image(object_list,img_np,color):

    object_dict = {
        "Vehicles": "机动车",
        "Pedestrian": "行人",
        "NonMotorVehicles": "非机动车"
    }

    font=cv.FONT_ITALIC

    if object_list is not None:
        count=0
        for object in object_list:
            object_x = object["Img"]["Cutboard"]["X"]
            object_y = object["Img"]["Cutboard"]["Y"]
            object_width = object["Img"]["Cutboard"]["Width"]
            object_height = object["Img"]["Cutboard"]["Height"]
            count+=1
            cv.rectangle(img_np, (object_x, object_y), (object_x + object_width, object_y + object_height),
                         color,
                     2, 4, 0)
            cv.putText(img_np, 'object{}'.format(count), (object_x, object_y), font, 0.5, (255, 255, 40), 1)
        image = cv.imencode('.jpg', img_np)[1]
        image_base64_str = str(base64.b64encode(image).decode("utf-8"))
        return image_base64_str


def get_pic_base64(url):

    print(url)
    pic_content=requests.request(url=url,method="GET").content

    # image=Image.open(BytesIO(pic_content))

    pic_base64=base64.b64encode(BytesIO(pic_content).read())


    return pic_base64
    # b64_pic=base64.encode(pic_content)
    # logging.debug(b64_pic)