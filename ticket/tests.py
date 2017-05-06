# -*- coding: utf-8 -*-
from django.test import TestCase
import uuid
import unittest
from mako.template import Template
from djangomako.shortcuts import render_to_response
from utils.str2json import render_json
from models import WorkOrder,WorkOrder_Manager

# Create your tests here.
class tests(unittest.TestCase):
    def testuuid(self):
        print str(uuid.uuid1())

    def testmako(self):
        mytemplate = Template("hello, ${name}!")
        print mytemplate.render(name="sand")


    def testhello(self):
        print render_to_response('hello.html', {'name': 'sand'})


    def testStr2Json(self):
        print render_json('{"code": 400,"msg": "请求的参数未通过验证[title]"}')


    def testquery(self):
        print WorkOrder_Manager.queryWorkOrder(self,30,0,1,20)