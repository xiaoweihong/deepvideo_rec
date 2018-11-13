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

def get_request_result(image_b64,rec_url,_face):
    request_string = {"Context": {"SessionId": "deepvide_web rec image", "Type": 1,
                                  "Functions":
                                      [100,
                                       101,
                                       102,
                                       103,
                                       104,
                                       105,
                                       106,
                                       107,
                                       108,
                                       109,
                                       200,
                                       110,
                                       111,
                                       112,
                                       200,
                                       201,
                                       202,
                                       203,
                                       204,
                                       205,
                                       300,
                                       301,
                                       400,
                                       401,
                                       402]}, "Image": {"Data": {"BinData": image_b64}}}
    if  _face:
        request_string["Context"]["Type"]=3

    jstring = json.dumps(request_string)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4'
                      ' Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) '
                      'Chrome/18.0.1025.166 Mobile Safari/535.19'}
    result = requests.post(rec_url, data=jstring, headers=headers).json()
    return result


def opencv_rec_image(b64data,data_result):

    rec_result={
        "image_base64_str":None,
        "rec_result":{
            "vehicles":None,
            "pedestrianp":None,
            "nonmotorvehicles":None,
            "faces":None
        }
    }

    object_color = {
        "vehicles": (255, 0, 0),
        "pedestrianp": (0, 255, 0),
        "nonmotorvehicles": (0, 255, 255),
        "faces": (0, 0, 255)
    }

    imgData = base64.b64decode(b64data)
    nparr = np.fromstring(imgData, np.uint8)

    img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)

    vehicles_list = get_object_list("Vehicles",data_result)

    pedestrianp_list=get_object_list("Pedestrian",data_result)

    nonnotorvehicles_list=get_object_list("NonMotorVehicles",data_result)

    faces_list=get_object_list("Faces",data_result)


    image = cv.imencode('.jpg', img_np)[1]
    rec_result["image_base64_str"] = str(base64.b64encode(image).decode("utf-8"))
    p_count = 0
    v_count = 0
    f_count = 0
    face_total=0
    nonv_count=0

    if vehicles_list is not None:
        logging.debug("识别到{}辆车".format(len(vehicles_list)))
        for vehicle in vehicles_list:
            if "Passengers" in vehicle:
                for p in vehicle["Passengers"]:
                    if "Face" in p:
                        v_count+=1

        rec_result["rec_result"]["vehicles"]=len(vehicles_list)
        rec_result["image_base64_str"]=rec_image(vehicles_list,img_np,object_color["vehicles"])

    if pedestrianp_list is not None  :
        logging.info("识别到{}个行人".format(len(pedestrianp_list)))

        for pedestrianp in pedestrianp_list:
            if "Face" in pedestrianp:
                p_count+=1
        rec_result["rec_result"]["pedestrianp"] = len(pedestrianp_list)
        rec_result["image_base64_str"] = rec_image(pedestrianp_list, img_np,object_color["pedestrianp"])

    if nonnotorvehicles_list is not None:
        logging.info("识别到{}个非机动车".format(len(nonnotorvehicles_list)))

        for nonnotorvehicle in nonnotorvehicles_list:
            if "Passengers" in nonnotorvehicle:
                for p in nonnotorvehicle["Passengers"]:
                    if "Face" in p:
                        nonv_count+=1

        rec_result["rec_result"]["nonmotorvehicles"] = len(nonnotorvehicles_list)
        rec_result["image_base64_str"] = rec_image(nonnotorvehicles_list, img_np,object_color["nonmotorvehicles"])

    if faces_list is not None:
        # logging.info("识别到{}个人脸".format(len(faces_list)))
        f_count=len(faces_list)
        rec_result["image_base64_str"] = rec_image(faces_list,img_np,object_color["faces"])
    face_total=f_count+p_count+v_count+nonv_count
    rec_result["rec_result"]["faces"] = face_total
    logging.info("识别到{}个人脸".format(face_total))

    return rec_result


def get_object_list(object,data_result):
    object_dict={
        "Vehicles":"机动车",
        "Pedestrian":"行人",
        "NonMotorVehicles":"非机动车",
        "Faces":"人脸"
    }

    if object in data_result["data"]["Result"]:
        object_list=data_result["data"]["Result"][object]
        return object_list

    else:
        logging.info("没有检测到{}目标".format(object_dict[object]))


def rec_image(object_list,img_np,color):

    font=cv.FONT_ITALIC

    if object_list is not None:
        count=0
        for object in object_list:
            object_x = object["Img"]["Cutboard"]["X"]
            object_y = object["Img"]["Cutboard"]["Y"]

            ##行人上的脸
            if "Face" in object:
                face_x=object["Face"]["Img"]["Cutboard"]["X"]
                face_y=object["Face"]["Img"]["Cutboard"]["Y"]
                face_w=object["Face"]["Img"]["Cutboard"]["Width"]
                face_h=object["Face"]["Img"]["Cutboard"]["Height"]
                cv.rectangle(img_np, (object_x+face_x, object_y+face_y), (object_x+face_x+face_w, object_y+face_y+face_h),
                             (0,0,255),
                             2, 4, 0)

            ##机动车和非机动车上的脸
            if "Passengers" in object:
                for o in object["Passengers"]:
                    if "Face" in o:
                        face_x = o["Face"]["Img"]["Cutboard"]["X"]
                        face_y = o["Face"]["Img"]["Cutboard"]["Y"]
                        face_w = o["Face"]["Img"]["Cutboard"]["Width"]
                        face_h = o["Face"]["Img"]["Cutboard"]["Height"]
                        cv.rectangle(img_np, (object_x + face_x, object_y + face_y),
                                     (object_x + face_x + face_w, object_y + face_y + face_h),
                                     (0, 0, 255),
                                     2, 4, 0)

            object_width = object["Img"]["Cutboard"]["Width"]
            object_height = object["Img"]["Cutboard"]["Height"]
            count+=1
            cv.rectangle(img_np, (object_x, object_y), (object_x + object_width, object_y + object_height),
                         color,2, 4, 0)
            cv.putText(img_np, 'object{}'.format(count), (object_x, object_y), font, 0.5, (255, 255, 40), 1)

        image = cv.imencode('.jpg', img_np)[1]
        image_base64_str = str(base64.b64encode(image).decode("utf-8"))
        return image_base64_str


def get_pic_base64(url):

    logging.info("请求的图片地址:{}".format(url))

    pic_content=requests.request(url=url,method="GET").content

    # image=Image.open(BytesIO(pic_content))

    pic_base64=base64.b64encode(BytesIO(pic_content).read())


    return pic_base64
