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
import base64

#request_url="http://192.168.6.27:6501/rec/image"
request_url="http://39.106.146.155:6501/rec/image"

#pic_url="http://192.168.6.121:8501/api/file/1,0421d01dc98117"

def url_to_image(url):
    resp=urllib.request.urlopen(url)
    image=np.asarray(bytearray(resp.read()),dtype="uint8")
    image=cv.imdecode(image,cv.IMREAD_COLOR)
    return image

#request_string={"Context":{"SessionId":"deepvide_web rec image","Type":1,"Functions":[100,101,102,103,104,105,106,107,108,200,201,202,203,204,300,400]},"Image":{"Data":{"URI":pic_url}}}
result={'Context': {'SessionId': 'deepvide_web rec image', 'Status': '200', 'Message': 'SUCCESS', 'RequestTs': {'Seconds': 1531308665, 'NanoSecs': 655027000}, 'ResponseTs': {'Seconds': 1531308665, 'NanoSecs': 833172000}}, 'Result': {'InnerStatus': '', 'InnerMessage': '', 'Image': {'Data': {'Id': '', 'Width': 1920, 'Height': 1080, 'URI': 'http://192.168.2.121:8501/api/file/5,0e7dd470c8aa8f', 'BinData': ''}, 'WitnessMetaData': {'Timestamp': 0, 'Duration': 0, 'SensorId': 0, 'SensorName': '', 'SensorUrl': '', 'RepoId': 0, 'RepoInfo': '', 'ObjType': 0, 'SensorIdStr': ''}}, 'Vehicles': [{'Id': 1, 'Img': {'Cutboard': {'X': 605, 'Y': 281, 'Width': 157, 'Height': 122, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9997650980949402}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 2, 'Img': {'Cutboard': {'X': 522, 'Y': 266, 'Width': 128, 'Height': 92, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9979997277259827}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 3, 'Img': {'Cutboard': {'X': 730, 'Y': 215, 'Width': 101, 'Height': 98, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9977697134017944}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 4, 'Img': {'Cutboard': {'X': 1190, 'Y': 202, 'Width': 92, 'Height': 72, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9959690570831299}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 5, 'Img': {'Cutboard': {'X': 851, 'Y': 198, 'Width': 89, 'Height': 74, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.995844304561615}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 6, 'Img': {'Cutboard': {'X': 996, 'Y': 160, 'Width': 85, 'Height': 66, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.991972804069519}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 7, 'Img': {'Cutboard': {'X': 3, 'Y': 500, 'Width': 118, 'Height': 181, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9904689192771912}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 8, 'Img': {'Cutboard': {'X': 1148, 'Y': 172, 'Width': 84, 'Height': 61, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.963351309299469}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 9, 'Img': {'Cutboard': {'X': 905, 'Y': 159, 'Width': 65, 'Height': 63, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.9332230091094971}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}, {'Id': 12, 'Img': {'Cutboard': {'X': 561, 'Y': 273, 'Width': 142, 'Height': 109, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.8200077414512634}}, 'Features': '', 'ModelType': {'StyleId': -1, 'Style': 'unknown', 'StyleConfidence': 0.0, 'BrandId': -1, 'Brand': 'unknown', 'BrandConfidence': 0.0, 'SubBrandId': -1, 'SubBrand': 'unknown', 'SubBrandConfidence': 0.0, 'ModelYearId': -1, 'ModelYear': 'unknown', 'ModelYearConfidence': 0.0, 'PoseId': -1, 'Pose': 'unknown', 'PoseConfidence': 0.0}}], 'NonMotorVehicles': [{'Id': 10, 'Img': {'Cutboard': {'X': 244, 'Y': 333, 'Width': 54, 'Height': 96, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.8373237252235413}}, 'Passengers': [{'Id': 0, 'Driver': True, 'Img': {'Cutboard': {'X': 0, 'Y': 0, 'Width': 54, 'Height': 96, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.0}}, 'PhoneFlag': -1, 'BeltFlag': -1, 'PhoneConfidence': 0.0, 'BeltConfidence': 0.0, 'FacecoverFlag': -1, 'FacecoverConfidence': 0.0}], 'Features': ''}, {'Id': 11, 'Img': {'Cutboard': {'X': 434, 'Y': 274, 'Width': 51, 'Height': 96, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.8362162709236145}}, 'Passengers': [{'Id': 0, 'Driver': True, 'Img': {'Cutboard': {'X': 0, 'Y': 0, 'Width': 51, 'Height': 96, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.0}}, 'PhoneFlag': -1, 'BeltFlag': -1, 'PhoneConfidence': 0.0, 'BeltConfidence': 0.0, 'FacecoverFlag': -1, 'FacecoverConfidence': 0.0}], 'Features': ''}, {'Id': 13, 'Img': {'Cutboard': {'X': 315, 'Y': 294, 'Width': 49, 'Height': 98, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.8122215867042542}}, 'Passengers': [{'Id': 0, 'Driver': True, 'Img': {'Cutboard': {'X': 0, 'Y': 0, 'Width': 49, 'Height': 98, 'ResWidth': 0, 'ResHeight': 0, 'Confidence': 0.0}}, 'PhoneFlag': -1, 'BeltFlag': -1, 'PhoneConfidence': 0.0, 'BeltConfidence': 0.0, 'FacecoverFlag': -1, 'FacecoverConfidence': 0.0}], 'Features': ''}]}}


#data=json.dumps(request_string)
#data=json.dumps(result)

#response=requests.post(request_url,data=data).json()

if "Vehicles" not in result["Result"]:
    print("没有识别到机动车")
    exit(400)

vehicles_list=result["Result"]["Vehicles"]

## 本地读取图片
img=cv.imread("car.jpeg",cv.IMREAD_UNCHANGED)

## 网络读取图片
#img=url_to_image(pic_url)

print("识别到{}辆车".format(len(vehicles_list)))

for vehicle in vehicles_list:
    #print(vehicle)
    vehicle_x=vehicle["Img"]["Cutboard"]["X"]
    vehicle_y=vehicle["Img"]["Cutboard"]["Y"]
    vehicle_width=vehicle["Img"]["Cutboard"]["Width"]
    vehicle_height=vehicle["Img"]["Cutboard"]["Height"]
    cv.rectangle(img,(vehicle_x,vehicle_y),(vehicle_x+vehicle_width,vehicle_y+vehicle_height),(255,0,0),2,4,0)

image=cv.imencode('.jpg', img)[1]
s=str(base64.b64encode(image))
print(s)
# print(url_to_image(pic_url))
