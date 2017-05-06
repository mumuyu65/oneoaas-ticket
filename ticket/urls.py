# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.conf import settings

urlpatterns = patterns('ticket.views',
    (r'^$', 'home'),
    (r'^searchTicket/$', 'searchTicket'),
    (r'^previewTicket/$', 'previewTicket'),
    (r'^searchKnowledge/$', 'searchKnowledge'),
    (r'^handlingTicket/$', 'handlingTicket'),
    (r'^unHandleTicket/$', 'unHandleTicket'),
    (r'^handledTicket/$', 'handledTicket'),
    (r'^api/createWorkOrder', 'create_work_order'),
    (r'^api/queryWorkOrder', 'query_work_order'),
    (r'^api/queryOrders', 'query_my_order'),
    (r'^api/queryUser', 'query_user'),
    (r'^api/queryOrg', 'query_org'),
    (r'^api/getOrderInfoById', 'get_order_info'),
    (r'^api/updateOrderById', 'update_order'),
    (r'^api/joinKnowledge', 'join_knowledge'),
    (r'^api/closeWorkOrder', 'close_work_order'),
    (r'^api/queryKnowledge', 'query_knowledge'),
)

urlpatterns += patterns('',
    url(r'static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
