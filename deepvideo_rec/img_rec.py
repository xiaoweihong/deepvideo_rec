#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/7/26 下午4:11
# @Author : xiaowei
# @Site : 
# @File : img_rec.py
# @Software: PyCharm

import base64
import json
from tools import image_handler
import argparse
import logging
import sys

logging.basicConfig(
            format='%(asctime)s,%(msecs)05.1f %(filename)s(%(funcName)s):%(lineno)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
from flask import Flask,render_template,request
# url = "http://211.103.220.74:8014/rec/image"


app=Flask(__name__,template_folder="templates",static_url_path="")

app.debug=True

@app.route('/')
def first_flask():
    return render_template("index.html")


@app.route('/rec/local',methods=['POST'])
def rec_local():
    data=request.files["local_image"].read()
    result = {"data": None, "image": None}

    b64 = base64.b64encode(data)

    b64 = b64.decode('utf-8')

    result_data = image_handler.get_request_result(b64, _http_rec_url)
    if result_data:

        result["data"] = result_data

        b64_rec = image_handler.opencv_rec_image(b64, result)

        result["image"] = b64_rec

        return json.dumps(result)
    else:
        logging.error("image rec failure")
        result["data"] = "rec image failure"
        result["image"] = b64
        return json.dumps(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c',
                        dest='config',
                        default="./config.json",
                        help='Path to load config path'
                        )

    args = parser.parse_args()
    _config = args.config
    try:
        with open(_config) as f:
            TYPES_CONFIG = json.load(f)
    except Exception:
        logging.exception("load json failed")
        sys.exit(1)

    _http_host = 'localhost'
    _http_port = 8888
    _http_debug = False
    _http_rec_url="localhost:6505"

    if "http" in TYPES_CONFIG:
        _http=TYPES_CONFIG["http"]
        host=_http.get("host",_http_host)
        port=_http.get("port",_http_port)
    if "log" in TYPES_CONFIG:
        _log=TYPES_CONFIG["log"]
        _http_debug=_log.get("debug",_http_debug)

        if _http_debug:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
    if "rec_config" in TYPES_CONFIG:
        _http_rec_url=TYPES_CONFIG["rec_config"]
        _http_rec_url="http://{}/rec/image".format(_http_rec_url["rec_url"])

    app.run(
        host=host,
        port=port,
        debug=_http_debug
    )