#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# @Author  : LiQingLei
# @File    : str2json.py
# @Time    : 2017/4/25 17:35
# @Last Modified by:   LiQingLei
# @Last Modified time: 2017/4/25 17:35
# @Site    : 
# @desc    :
'''

import json
from django.http import HttpResponse

def render_json(dictionary={}):
    """
    return the json string for response
    @summary: dictionary也可以是string, list数据
    @note:  返回结果是个dict, 请注意默认数据格式:
                                    {'result': '',
                                     'message':''
                                    }
    """
    if type(dictionary) is not dict:
        # 如果参数不是dict,则组合成dict
        dictionary = {
            'result': True,
            'message': dictionary,
        }
    return HttpResponse(json.dumps(dictionary), content_type='application/json')