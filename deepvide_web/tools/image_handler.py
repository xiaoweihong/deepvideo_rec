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



def get_request_result(image_b64,rec_url):

    request_string = {"Context": {"SessionId": "deepvide_web rec image", "Type": 1,
                                  "Functions": [100, 101, 102, 103, 104, 105, 106, 107, 108, 200, 201, 202, 203, 204,
                                                300, 400]}, "Image": {"Data": {"BinData": image_b64}}}
    jstring = json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
    result = requests.post(rec_url, data=jstring, headers=headers).json()
    return result


def opencv_rec_image(b64data,data_result):

    imgData = base64.b64decode(b64data)
    nparr = np.fromstring(imgData, np.uint8)

    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)

    if "Vehicles" not in data_result["data"]["Result"]:
        print("没有识别到机动车")
        return None

    vehicles_list = data_result["data"]["Result"]["Vehicles"]

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
    image_base64_str = str(base64.b64encode(image).decode("utf-8"))
    #print(s)
    return image_base64_str