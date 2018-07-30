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
from tools import ft2




def get_request_result(image_b64,rec_url):

    request_string = {"Context": {"SessionId": "deepvide_web rec image", "Type": 1,
                                  "Functions": [100, 101, 102, 103, 104, 105, 106, 107, 108, 200, 201, 202, 203, 204,
                                                300, 400]}, "Image": {"Data": {"BinData": image_b64}}}
    jstring = json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    try:
        result = requests.post(rec_url, data=jstring, headers=headers,timeout=5).json()
        logging.debug(result)
        return result
    except requests.ConnectTimeout:
        logging.error("request rec url timeout.")
    except Exception as e:
        logging.error(e)


def opencv_rec_image(b64data,data_result):
    object_color = {
        "vehicles": (255, 0, 0),
        "pedestrian": (0, 255, 0),
        "nonmotorvehicles": (0, 0, 255),
    }

    imgData = base64.b64decode(b64data)
    nparr = np.fromstring(imgData, np.uint8)

    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)


    vehicles_list = get_object_list("Vehicles",data_result)

    pedestrianp_list=get_object_list("Pedestrian",data_result)

    nonnotorvehicles_list=get_object_list("NonMotorVehicles",data_result)
    image = cv.imencode('.jpg', img_np)[1]
    image_base64_str = str(base64.b64encode(image).decode("utf-8"))
    if vehicles_list is not None:
        logging.info("识别到{}辆车".format(len(vehicles_list)))
        image_base64_str=rec_image(vehicles_list,img_np,object_color["vehicles"])

    if pedestrianp_list is not None:
        logging.info("识别到{}个行人".format(len(pedestrianp_list)))
        image_base64_str = rec_image(pedestrianp_list, img_np,object_color["pedestrian"])

    if nonnotorvehicles_list is not None:
        logging.info("识别到{}个非机动车".format(len(nonnotorvehicles_list)))
        image_base64_str = rec_image(nonnotorvehicles_list, img_np,object_color["nonmotorvehicles"])

    return image_base64_str


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
    ft = ft2.put_chinese_text('simsun.ttf')
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
