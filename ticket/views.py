# -*- coding: utf-8 -*-
from django.http import HttpResponse
from common.log import logger
from django.shortcuts import render_to_response
from datetime import datetime
import time
import uuid
import traceback
from ticket.models import WorkOrder,user,organization
from utils.str2json import render_json

def home(request):
    return render_to_response('tickets/index.html')

def searchTicket(request):
    return render_to_response('tickets/search_ticket.html')

def previewTicket(request):
    return render_to_response('tickets/preview_Ticket.html')

def searchKnowledge(request):
    return render_to_response('tickets/search_knowledge.html')

def handlingTicket(request):
   return render_to_response('tickets/handling_ticket.html')

def unHandleTicket(request):
   return render_to_response('tickets/unhandle_ticket.html')

def handledTicket(request):
   return render_to_response('tickets/handled_ticket.html')

'''
根据用户传入的工单的信息，进行工单的创建工作，具体的工单基本信息已经
'''
def create_work_order(request):
    try:
        orderid = str(uuid.uuid1())
        title = request.POST.get('title')
        content = request.POST.get('content')
        createuser = request.POST.get('createuser')
        handler = request.POST.get('handler')
        priority = request.POST.get('priority')
        severity = request.POST.get('severity')
        create_time = datetime.now()
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        orgid = request.POST.get('orgId')
        tag = request.POST.get('tag')
        isKnowledge = request.POST.get('isKnowledge')
        opresult = 0
        status = 0
        print tag
        responseResult = {"code": 200, "id": {}, "msg": "创建工单成功"}
        if title is None or title == '':
            return render_json({"code": 400,"msg": "请求的参数未通过验证[title]"})
        if content is None or content == '':
            return render_json({"code": 400,"msg": "请求的参数未通过验证[content]"})
        if createuser is None or not createuser.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[createuser]"})
        if handler is None or not handler.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[handler]"})
        if priority is None or not priority.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[priority]"})
        if severity is None or not severity.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[severity]"})
        if orgid is None or not orgid.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[orgid]"})
        if tag is None or tag == '':
            return render_json({"code": 400, "msg": "请求的参数未通过验证[tag]"})
        if isKnowledge is None or not isKnowledge == '':
            isKnowledge = 0
        # 开始时间
        if start_time is None or start_time =='':
            starttime = datetime.now()
        else:
            if '&nbsp;'in start_time:
                start_time = start_time.replace('&nbsp;',' ')
            starttime = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        #结束时间
        # 开始时间
        if end_time is None or end_time == '':
            endtime = datetime.now()
        else:
            if '&nbsp;' in end_time:
                end_time = end_time.replace('&nbsp;',' ')
            endtime = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
        workorderid = WorkOrder.objects.saveWorkOrder(orderid,title,content,long(createuser),long(handler),int(priority),int(severity),create_time,starttime,endtime,opresult,status,isKnowledge,orgid,tag)
        print workorderid
        if workorderid is not None:
            responseResult["id"] = workorderid
            print responseResult
            return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "创建工单出错"})



def query_work_order(request):
    try:
        responseResult = {"code": 200, "content": [], "total": 0, "msg": "请求成功"}
        params = {}
        createUserId = request.POST.get('createUserId')
        tag = request.POST.get('tag')
        opResult = request.POST.get('opResult')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        pageno = request.POST.get('pageno')
        pagecount = request.POST.get('pagecount')
        if createUserId is not None and createUserId.isdigit():
            params["createUserId"] = long(createUserId)
        if opResult is not None and opResult.isdigit():
            params["opResult"] = int(opResult)
        if tag is not None and tag.isdigit():
            params["tag"] = int(tag)
        if pageno is not None and pageno.isdigit():
            params["pageno"] = int(pageno)
        if pagecount is not None and pagecount.isdigit():
            params["pagecount"] = int(pagecount)
        # 开始时间
        if start_time is None or start_time =='':
            pass
            # starttime = datetime.now()
        else:
            if '&nbsp;'in start_time:
                start_time = start_time.replace('&nbsp;',' ')
            starttime = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            params["starttime"] = time.mktime(starttime.timetuple())
        #结束时间
        if end_time is None or end_time == '':
            pass
            # endtime = datetime.now()
        else:
            if '&nbsp;' in end_time:
                end_time = end_time.replace('&nbsp;',' ')
            endtime = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            params["endtime"] = time.mktime(endtime.timetuple())
        orders = WorkOrder.objects.queryOrders(params)
        if orders is not None:
            responseResult["content"] = orders
        count = WorkOrder.objects.queryOrderCount(params)
        if count is not None and len(count) > 0:
            responseResult["total"] = count[0]
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询知识库出错"})
    # # 根据查询标签来进行查询，如果查询标签为0表示简单查询，1表示复杂查询
    # querytag = request.POST.get('querytag')
    # if querytag is None or not querytag.isdigit():
    #     return render_json({"code": 400, "msg": "请求的参数未通过验证[severity]"})
    # #页号
    # pageno = request.POST.get('pageno')
    # #单页查询的条数
    # limit = request.POST.get('limit')
    # if int(querytag) == 0:
    #     handler = request.POST.get('handler')
    #     opresult = request.POST.get('opresult')
    #     pass
    # elif int(querytag) ==1:
    #     opresult = request.POST.get('opresult')
    #     keyword = request.POST.get('keyword')
    #     createuser = request.POST.get('createuser')
    #     start_time = request.POST.get('startTime')
    #     end_time = request.POST.get('endTime')
    #     return render_json({"code": 400, "msg": "请求的参数未通过验证[severity]"})
    #     # 根据工单处理状态和操作人进行查询工单的列表信息
    #     # 查询中隐含了一个条件，就是用户所在的组织，每个人只能查自己所在组织的相关工单
    #     # 1、根据调用接口的用户的信息查询其所在组织的信息
    #     pass



'''
列表信息中已经完全返回每一个工单的详细信息，所以在查询单个工单详情时不用再发送请求获取
'''
def get_order_info(request):
    try:
        responseResult = {"code": 200,"msg": "获取工单详情成功"}
        orderId = request.POST.get('orderId')
        if orderId is None:
            return render_json({"code": 400, "msg": "请求的参数未通过验证[orderId]"})
        orders = WorkOrder.objects.queryOrdersById(orderId)
        if orders is not None and len(orders):
            responseResult["content"] = orders[0]
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询工单详情出错"})



'''
根据工单id更新工单信息
'''
def update_order(request):
    try:
        responseResult = {"code": 200, "msg": "更新成功"}
        orderId = request.POST.get('orderId')
        content = request.POST.get('content')
        if orderId is None:
            return render_json({"code": 400, "msg": "请求的参数未通过验证[orderId]"})
        if content is None or content == '':
            return render_json({"code": 400, "msg": "请求的参数未通过验证[content]"})
        WorkOrder.objects.updateOrder(orderId,content)
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "更新工单出错"})



'''
将工单加入知识库
'''
def join_knowledge(request):
    try:
        responseResult = {"code": 200, "msg": "加入知识库成功"}
        orderId = request.POST.get('orderId')
        if orderId is None:
            return render_json({"code": 400, "msg": "请求的参数未通过验证[orderId]"})
        WorkOrder.objects.joinKonwledge(orderId)
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "加入知识库出错"})



'''
将工单加入知识库
'''
def close_work_order(request):
    try:
        responseResult = {"code": 200, "msg": "关闭工单成功"}
        orderId = request.POST.get('orderId')
        if orderId is None:
            return render_json({"code": 400, "msg": "请求的参数未通过验证[orderId]"})
        WorkOrder.objects.closeWorkOrder(orderId)
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "关闭工单出错"})



'''
查询知识库信息
'''
def query_knowledge(request):
    try:
        responseResult = {"code": 200, "content": [], "total": 0, "msg": "请求成功"}
        params = {}
        createUserId = request.POST.get('createUserId')
        tag = request.POST.get('tag')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        pageno = request.POST.get('pageno')
        pagecount = request.POST.get('pagecount')
        if createUserId is not None and createUserId.isdigit():
            params["createUserId"] = long(createUserId)
        if tag is not None and tag.isdigit():
            params["tag"] = int(tag)
        if pageno is not None and pageno.isdigit():
            params["pageno"] = int(pageno)
        if pagecount is not None and pagecount.isdigit():
            params["pagecount"] = int(pagecount)
        # 开始时间
        if start_time is None or start_time =='':
            pass
            # starttime = datetime.now()
        else:
            if '&nbsp;'in start_time:
                start_time = start_time.replace('&nbsp;',' ')
            starttime = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            params["starttime"] = time.mktime(starttime.timetuple())
        #结束时间
        if end_time is None or end_time == '':
            pass
            # endtime = datetime.now()
        else:
            if '&nbsp;' in end_time:
                end_time = end_time.replace('&nbsp;',' ')
            endtime = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
            params["endtime"] = time.mktime(endtime.timetuple())
        orders = WorkOrder.objects.queryknowledge(params)
        if orders is not None:
            responseResult["content"] = orders
        count = WorkOrder.objects.queryknowledgecount(params)
        if count is not None and len(count) > 0:
            responseResult["total"] = count[0]
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询知识库出错"})



'''
获取需要我处理的工单信息
'''
def query_my_order(request):
    try:
        responseResult = {"code": 200, "content": [], "total": 0, "msg": "请求成功"}
        userid = request.POST.get('userid')
        handler = request.POST.get('handler')
        opresult = request.POST.get('opresult')
        pageno = request.POST.get('pageno')
        pagecount = request.POST.get('pagecount')
        if handler is None or not handler.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[handler]"})
        if opresult is None or not opresult.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[opresult]"})
        if pageno is None or not pageno.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[pageno]"})
        if pagecount is None or not pagecount.isdigit():
            return render_json({"code": 400,"msg": "请求的参数未通过验证[pagecount]"})
        handler =int(handler)
        opresult =int(opresult)
        pageno =int(pageno)
        pagecount =int(pagecount)
        orders = WorkOrder.objects.queryMyOrders(handler,opresult,pageno,pagecount)
        if orders is not None:
            responseResult["content"] = orders
        count = WorkOrder.objects.queryMyOrdersCount(handler, opresult)
        if count is not None and len(count) > 0:
            responseResult["total"] = count[0]
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询工单出错"})



'''
获取所有的用户信息
'''
def query_user(request):
    try:
        responseResult = {"code": 200, "content": [], "msg": "请求成功"}
        users = user.objects.querySimpleUsers()
        print users
        if users is not None:
            responseResult["content"] = users
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询用户信息出错"})



'''
获取所有的组织信息
'''
def query_org(request):
    try:
        responseResult = {"code": 200, "content": [], "msg": "请求成功"}
        organizations = organization.objects.querySimpleOrg()
        print organizations
        if organizations is not None:
            responseResult["content"] = organizations
        return render_json(responseResult)
    except Exception, e:
        print e
        traceback.print_exc()
        return render_json({"code": 400, "msg": "查询组织信息出错"})





