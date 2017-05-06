/**
 * Created by yangyangyu on 2017/5/6.
 * 未处理工单
 */
var UnhandleTicket={
    init:function () {
        UnhandleTicket.Table();
    },
    params:{
        userid:1,
        handler:1,
        opresult:0,
        pageno:1,
        pagecount:100,
    },
    Table:function () {
        var $table = $('#unhandle_ticket_result');
        var tableOptions={
            data: [],
            pagination: true,                   //是否显示分页（*）
            sidePagination: "client",
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize:20,                       //每页的记录行数（*）
            pageList: [10, 15, 20 ],        //可供选择的每页的行数（*）
            locale: "zh_CN",
            cache: true,
            striped: true,
            minimumCountColumns: 2,
            columns: [
                {
                    field: 'orderId',
                    title: '',
                    formatter: function(value, row, index){
                        return '';
                    },
                },
                {
                    field: 'id',
                    title: '工单序号'
                },
                {
                    field: 'title',
                    title: '工单标题',
                    formatter: function(value, row, index){
                        return '<a id="title_editor" style="text-decoration:underline;cursor:pointer;color:#20A0FF;">' + value + '</a>'
                    },
                    events: {
                        'click #title_editor': function (e, value, row, index) {
                            window.localStorage.setItem("sourcePath",window.location.pathname);
                            window.localStorage.setItem("orderId",row.id);
                            window.location.href = '/previewTicket/';
                        }
                    }
                },
                {
                    field: 'content',
                    title: '工单内容'
                },
                {
                    field: 'createUserName',
                    title: '创建人'
                },
                {
                    field: 'handlerName',
                    title: '处理人'
                },
                {
                    field: 'opResult',
                    title: '处理结果',
                    formatter: function(value, row, index){
                        switch (value){
                            case 0: return '待处理'; break;
                            case 1: return '处理中'; break;
                            case 2: return '已关闭'; break;
                            default:
                                return ;
                        }
                    },
                },

                {
                    field: 'status',
                    title: '状态',
                    formatter: function(value, row, index){
                        switch (value){
                            case 0: return '开启中'; break;
                            case 1: return '关闭'; break;
                            default:
                                return ;
                        }

                    },
                },
                {
                    field: 'createUserId',
                    title: '创建人ID',
                },
                {
                    field: 'handlerId',
                    title: '处理人ID',
                }
            ]
        };
        $table.bootstrapTable(tableOptions);
        $.ajax({
            url:api_config.queryOrders,
            method:'POST',
            dataType: 'json',
            data:UnhandleTicket.params,
            beforeSend: function () {
                $('#unhandle_ticket_result').append('<div class="loader"><div class="loader-inner ball-pulse"><div></div><div></div><div></div></div></div>');
            },
            success:function (d) {
                console.log(d);
                tableOptions.data=d.content;
                $table.bootstrapTable('destroy').bootstrapTable(tableOptions);
                $table.bootstrapTable('hideColumn', 'createUserId');
                $table.bootstrapTable('hideColumn', 'handlerId');
            },
            error:function () {
                console.log("error.......");
            }
        });
    },
};

$(document).ready(function () {
    UnhandleTicket.init();
});
