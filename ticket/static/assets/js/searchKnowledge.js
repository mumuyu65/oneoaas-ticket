/**
 * Created by yangyangyu on 2017/5/6.
 * 知识库
 */
var SearchKnowledge={
    init:function () {
        SearchKnowledge.selectTime();

        SearchKnowledge.Table();

        $("#search_knowledge_condition").click(function () {
            SearchKnowledge.search();
        });

        $("#search_knowledge_cancel").click(function (){
            SearchKnowledge.reset();
        });
    },
    params:{
        createUserId:1,
        tag:'',
        startTime:'',
        endTime:'',
        pageno:1,
        pagecount:100,
    },
    options:{
        locale:{
            format: 'YYYY-MM-DD HH:mm',
            separator: ' - ',
            applyLabel: '应用',
            cancelLabel: '取消',
            fromLabel: '从',
            toLabel: '到',
            customRangeLabel: '自定义',
            daysOfWeek: ['日', '一', '二', '三', '四', '五','六'],
            monthNames: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            firstDay: 1
        },
        autoApply:true,
        alwaysShowCalendars:true,
        linkedCalendars:true,
        autoUpdateInput:true,
        showCustomRangeLabel:true,
        timePicker24Hour:true,
        ranges:{
            '最近1小时': [moment().subtract(1,"hours"), moment()],
            '最近12小时': [moment().subtract(12,"hours"), moment()],
            '最近1天': [moment().subtract(24,"hours"), moment()],
            '最近7天': [moment().subtract(6, 'days'), moment()],
            '最近30天': [moment().subtract(29, 'days'), moment()]
        },
        opens:'center',
        drops:'down',
        timePicker:true
    },
    selectTime:function(){
        $("#Timer").daterangepicker(SearchKnowledge.options,
            function(start, end, label) {
                var stime=start.format('YYYY-MM-DD HH:mm'),
                    etime=end.format('YYYY-MM-DD HH:mm');
                $("#Timer input").val(stime + " -- "+etime);
                SearchKnowledge.params.startTime=stime;
                SearchKnowledge.params.endTime=etime;
            });
    },
    Table:function () {
        var $table = $('#search_knowledge_result');
        var tableOptions={
            data: [],
            pagination: true,                   //是否显示分页（*）
            sidePagination: "client",
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize:15,                       //每页的记录行数（*）
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
                    title: '知识库序号',
                    formatter: function(value, row, index){
                        return '#'+value;
                    },
                },
                {
                    field: 'title',
                    title: '知识库标题',
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
                    title: '知识库内容'
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
                },

                {
                    field: 'status',
                    title: '状态',
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
            url:api_config.queryKnowledge,
            method:'POST',
            dataType: 'json',
            data:SearchKnowledge.params,
            beforeSend: function () {
                $('#search_knowledge_result').append('<div class="loader"><div class="loader-inner ball-pulse"><div></div><div></div><div></div></div></div>');
            },
            success:function (d) {
                tableOptions.data=d.content;
                $table.bootstrapTable('destroy').bootstrapTable(tableOptions);
                $table.bootstrapTable('hideColumn', 'handlerName');
                $table.bootstrapTable('hideColumn', 'opResult');
                $table.bootstrapTable('hideColumn', 'status');
                $table.bootstrapTable('hideColumn', 'createUserId');
                $table.bootstrapTable('hideColumn', 'handlerId');
            },
            error:function () {
                console.log("error.......");
            }
        });
    },
    search:function () {
        SearchKnowledge.params.tag=$("#search_knowledge_keyword").val();
        SearchKnowledge.Table();
    },
    reset:function () {
        $("#search_knowledge_keyword").val("");
        $("#Timer input").val('');
        SearchKnowledge.params={
            createUserId:1,
            tag:'',
            startTime:'',
            endTime:'',
        };
    }
};


$(document).ready(function () {
    SearchKnowledge.init();
});
