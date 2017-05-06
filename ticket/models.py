# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import traceback
from django.db import connection, transaction

# Create your models here.
class WorkOrder_Manager(models.Manager):

    def saveWorkOrder(self,orderid,title,content,createuser,handler,priority,severity,create_time,start_time,end_time,opresult,status,isKnowledge,orgId,tag):
        try:
            workorder = WorkOrder(order_id=orderid,title=title,content=content,create_user=createuser,handler=handler,priority=priority,severity=severity,create_time=create_time,start_time=start_time,end_time=end_time,op_result=opresult,status=status,is_knowledge = isKnowledge,org_id=orgId,tag=tag)
            workorder.save()
            return workorder.id
        except Exception, e:
            print e
            traceback.print_exc()

    def queryMyOrders(self,userid,opresult,pageno,limit):
        try:
            start = (pageno-1) * limit
            end = pageno * limit
            queryStr = 'SELECT qw.id,qw.order_id as orderId,qw.title,qw.content,qw.create_user as createUserId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.create_user) AS createUserName,qw.`handler`AS handlerId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.`handler`) AS handlerName,qw.op_result as opResult,qw.`status` FROM ticket_workorder qw WHERE qw.op_result='+ str(opresult) +' and qw.`handler`='+ str(userid) +' LIMIT '+ str(start) +','+ str(end)
            cursor = connection.cursor()
            cursor.execute(queryStr)
            print queryStr
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        except Exception, e:
            print e
            traceback.print_exc()

    def queryMyOrdersCount(self, userid, opresult):
        try:
            queryStr = 'SELECT count(*) FROM ticket_workorder qw WHERE qw.op_result=' + str(opresult) + ' and qw.`handler`=' + str(userid)
            cursor = connection.cursor()
            cursor.execute(queryStr)
            print queryStr
            return cursor.fetchone()
        except Exception, e:
            print e
            traceback.print_exc()

    def queryOrdersById(self,orderId):
        queryStr = 'SELECT qw.id,qw.order_id as orderId,qw.title,qw.content,qw.create_user as createUserId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.create_user) AS createUserName,qw.`handler`AS handlerId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.`handler`) AS handlerName,qw.op_result as opResult,qw.`status` FROM ticket_workorder qw WHERE qw.id = '+ orderId
        cursor = connection.cursor()
        cursor.execute(queryStr)
        print queryStr
        column_names = [d[0] for d in cursor.description]
        return [Row(zip(column_names, row)) for row in cursor]

    def updateOrder(self, orderid, content):
        try:
            obj = WorkOrder.objects.get(id=orderid)
            obj.content = str(content)
            obj.save()
            return obj.id
        except Exception, e:
            print e
            traceback.print_exc()

    def joinKonwledge(self, orderid):
        try:
            obj = WorkOrder.objects.get(id=orderid)
            obj.is_knowledge = 1
            obj.save()
            return obj.id
        except Exception, e:
            print e
            traceback.print_exc()

    def closeWorkOrder(self, orderid):
        try:
            obj = WorkOrder.objects.get(id=orderid)
            obj.status = 1
            obj.save()
            return obj.id
        except Exception, e:
            print e
            traceback.print_exc()

    def queryOrders(self, params):
        try:
            queryStr = 'SELECT qw.id,qw.order_id as orderId,qw.title,qw.content,qw.create_user as createUserId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.create_user) AS createUserName,qw.`handler`AS handlerId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.`handler`) AS handlerName,qw.op_result as opResult,qw.`status` FROM ticket_workorder qw WHERE  1=1 '
            if params.has_key('createUserId'):
                createUserId = params["createUserId"]
                appendstr ='  and qw.create_user = '+ str(createUserId)
                queryStr = queryStr + appendstr
            if params.has_key('tag'):
                tag = params["tag"]
                appendstr = " and qw.tag LIKE '%" + tag + "%' "
                queryStr = queryStr + appendstr
            if params.has_key('opResult'):
                opResult = params["opResult"]
                appendstr = " and qw.op_result = " + str(opResult)
                queryStr = queryStr + appendstr
            if params.has_key('starttime'):
                starttime = params["starttime"]
                appendstr = " and UNIX_TIMESTAMP(qw.end_time) > "+ str(starttime)
                queryStr = queryStr + appendstr
            if params.has_key('endtime'):
                endtime = params["endtime"]
                appendstr = " and UNIX_TIMESTAMP(qw.start_time) < " + str(endtime)
                queryStr = queryStr + appendstr
            if params.has_key('pageno') and params.has_key('pagecount'):
                pageno = params["pageno"]
                pagecount = params["pagecount"]
                start = (pageno - 1) * pagecount
                end = pageno * pagecount
                appendstr = " limit "+ str(start) +","+ str(end)
                queryStr = queryStr + appendstr
            print queryStr
            cursor = connection.cursor()
            cursor.execute(queryStr)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        except Exception, e:
            print e
            traceback.print_exc()


    def queryOrderCount(self, params):
        try:
            queryStr = 'SELECT count(*) FROM ticket_workorder qw WHERE  1=1 '
            if params.has_key('createUserId'):
                createUserId = params["createUserId"]
                appendstr = '  and qw.create_user = ' +  str(createUserId)
                queryStr = queryStr + appendstr
            if params.has_key('tag'):
                tag = params["tag"]
                appendstr = " and qw.tag LIKE '%" + tag + "%' "
                queryStr = queryStr + appendstr
            if params.has_key('opResult'):
                opResult = params["opResult"]
                appendstr = " and qw.op_result = " + str(opResult)
                queryStr = queryStr + appendstr
            if params.has_key('starttime'):
                starttime = params["starttime"]
                appendstr = " and UNIX_TIMESTAMP(qw.end_time) > " + str(starttime)
                queryStr = queryStr + appendstr
            if params.has_key('endtime'):
                endtime = params["endtime"]
                appendstr = " and UNIX_TIMESTAMP(qw.start_time) < " + str(endtime)
                queryStr = queryStr + appendstr
            print queryStr
            cursor = connection.cursor()
            cursor.execute(queryStr)
            return cursor.fetchone()
        except Exception, e:
            print e
            traceback.print_exc()


    def queryknowledge(self, params):
        try:
            queryStr = 'SELECT qw.id,qw.order_id as orderId,qw.title,qw.content,qw.create_user as createUserId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.create_user) AS createUserName,qw.`handler`AS handlerId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.`handler`) AS handlerName,qw.op_result as opResult,qw.`status` FROM ticket_workorder qw WHERE qw.is_knowledge = 1 '
            if params.has_key('createUserId'):
                createUserId = params["createUserId"]
                appendstr ='  and qw.create_user = '+  str(createUserId)
                queryStr = queryStr + appendstr
            if params.has_key('tag'):
                tag = params["tag"]
                appendstr = " and qw.tag LIKE '%" + tag + "%' "
                queryStr = queryStr + appendstr
            if params.has_key('starttime'):
                starttime = params["starttime"]
                appendstr = " and UNIX_TIMESTAMP(qw.end_time) > "+ str(starttime)
                queryStr = queryStr + appendstr
            if params.has_key('endtime'):
                endtime = params["endtime"]
                appendstr = " and UNIX_TIMESTAMP(qw.start_time) < " + str(endtime)
                queryStr = queryStr + appendstr
            if params.has_key('pageno') and params.has_key('pagecount'):
                pageno = params["pageno"]
                pagecount = params["pagecount"]
                start = (pageno - 1) * pagecount
                end = pageno * pagecount
                appendstr = " limit " + str(start) + "," + str(end)
                queryStr = queryStr + appendstr
            print queryStr
            cursor = connection.cursor()
            cursor.execute(queryStr)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        except Exception, e:
            print e
            traceback.print_exc()

    def queryknowledgecount(self, params):
        try:
            queryStr = 'SELECT count(*) FROM ticket_workorder qw WHERE qw.is_knowledge = 1 '
            if params.has_key('createUserId'):
                createUserId = params["createUserId"]
                appendstr = '  and qw.create_user = ' +  str(createUserId)
                queryStr = queryStr + appendstr
            if params.has_key('tag'):
                tag = params["tag"]
                appendstr = " and qw.tag LIKE '%" + tag + "%' "
                queryStr = queryStr + appendstr
            if params.has_key('starttime'):
                starttime = params["starttime"]
                appendstr = " and UNIX_TIMESTAMP(qw.end_time) > " + str(starttime)
                queryStr = queryStr + appendstr
            if params.has_key('endtime'):
                endtime = params["endtime"]
                appendstr = " and UNIX_TIMESTAMP(qw.start_time) < " + str(endtime)
                queryStr = queryStr + appendstr
            print queryStr
            cursor = connection.cursor()
            cursor.execute(queryStr)
            return cursor.fetchone()
        except Exception, e:
            print e
            traceback.print_exc()

    # def queryOrderInfo(self,orderId):
    #     try:
    #         queryStr = 'SELECT qw.order_id as orderId,qw.title,qw.content,qw.create_user as createUserId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.create_user) AS createUserName,qw.`handler`AS handlerId,(SELECT tu.user_name FROM ticket_user tu WHERE tu.id=qw.`handler`) AS handlerName,qw.op_result as opResult,qw.`status` FROM ticket_workorder qw WHERE qw.op_result='+ str(opresult) +' and qw.`handler`='+ str(userid) +' LIMIT '+ str(start) +','+ str(end)
    #         cursor = connection.cursor()
    #         cursor.execute(queryStr)
    #         column_names = [d[0] for d in cursor.description]
    #         return [Row(zip(column_names, row)) for row in cursor]
    #     except Exception, e:
    #         print e
    #         traceback.print_exc()


class WorkOrder(models.Model):
    order_id = models.CharField(u"工单id", max_length=100,unique=True)
    title = models.CharField(u"工单标题", max_length=128, )
    content = models.CharField(u"工单内容",max_length=5000)
    create_user = models.BigIntegerField(u"创建人")
    handler = models.BigIntegerField(u"处理人")
    priority = models.IntegerField(u"优先级",help_text=u'1-5，五个级别')
    severity = models.IntegerField(u"紧急程度",help_text=u'1-7，七个级别与zabbix后期对应')
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)
    start_time = models.DateTimeField(u"开始时间", default=timezone.now)
    end_time = models.DateTimeField(u"结束时间", default=timezone.now)
    op_result = models.IntegerField(u"处理结果",help_text=u"0为待处理，1为处理中,2为已处理",default=0)
    status = models.IntegerField(u"工单状态", help_text=u"0为开启，1为关闭",default=0)
    is_knowledge = models.IntegerField(u"是否加入知识库",help_text=u'0为未加入，1为已加入',default=0)
    org_id = models.BigIntegerField(u"所属组织")
    tag = models.CharField(u"标签", max_length=100)

    objects = WorkOrder_Manager()

    def __unicode__(self):
        return self.order_id


class user_Manager(models.Manager):
    def saveUser(self,userName,createTime,orgId):
        try:
            newuser = user(user_name=userName,create_time=createTime,org_id=orgId)
            newuser.save()
            return newuser.id
        except Exception, e:
            print e
            traceback.print_exc()

    def querySimpleUsers(self):
        try:
            queryStr = 'SELECT id,user_name AS userName,org_id AS grgId FROM ticket_user;'
            cursor = connection.cursor()
            cursor.execute(queryStr)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        except Exception, e:
            print e
            traceback.print_exc()

class user(models.Model):
    user_name = models.CharField(u"用户名称", max_length=100)
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)
    org_id = models.BigIntegerField(u"所属组织")
    objects = user_Manager()

    def __unicode__(self):
        return self.id


class organization_Manager(models.Manager):
    def saveUser(self,orgName,createTime):
        try:
            neworg = organization(org_name=orgName,create_time=createTime)
            neworg.save()
            return neworg.id
        except Exception, e:
            print e
            traceback.print_exc()

    def querySimpleOrg(self):
        try:
            queryStr = 'SELECT id,org_name AS orgName FROM ticket_organization;'
            cursor = connection.cursor()
            cursor.execute(queryStr)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        except Exception, e:
            print e
            traceback.print_exc()

class organization(models.Model):
    org_name = models.CharField(u"组织名称", max_length=100)
    create_time = models.DateTimeField(u"创建时间", default=timezone.now)

    objects = organization_Manager()

    def __unicode__(self):
        return self.id




class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)