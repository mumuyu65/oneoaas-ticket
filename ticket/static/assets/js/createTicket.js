/**
 * Created by yangyangyu on 2017/4/28.
 * 创建工单
 */
var CreateTicket={
    orderId:'',
    init:function () {
       CreateTicket.tinymce(); //初始化工单填充信息
       CreateTicket.selectQueryOrg();  //所属团队
       CreateTicket.selectQueryUser(); //所属人员
       CreateTicket.selectTime(); //时间轴插件
        //cancel
        $("#ticket_cancel").click(function () {
            CreateTicket.Cancel();
        });
        //save and preview
        $("#ticket_save").click(function () {
            CreateTicket.Save();
        });
    },
    params:{
        title:'',  //工单标题
        content:'',  //工单内容
        tag:'',  //标签
        orgId:'',   //所属团队
        handler:'',  //所属人员
        createuser:'',   //创建人
        severity:'',    //紧急度
        priority:'',  //优先级
        startTime:'',
        endTime:''
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
        drops:'up',
        timePicker:true
    },
    selectQueryOrg:function () {
        $.ajax({
            type:"GET",
            url:api_config.queryOrg,
            success:function(data){
                if(data.code == 200){
                    var len = data.content.length;
                    $("#ticket_queryOrg").html('');
                    for(var i =0 ; i< len; i++){
                        var queryOrg_option = $('<option value="'+data.content[i].id+'">'+data.content[i].orgName+'</option>');
                        $("#ticket_queryOrg").append(queryOrg_option);
                    }
                }
            },
            error:function (data) {
               console.log("出错原因是:"+data);
            }
        });
    },
    selectQueryUser:function(){
        $.ajax({
            type:"GET",
            url:api_config.queryUser,
            success:function(data){
                if(data.code == 200){
                    var len = data.content.length;
                    $("#ticket_queryUser").html('');
                    for(var i =0 ; i< len; i++){
                        var queryUser_option = $('<option value="'+data.content[i].id+'">'+data.content[i].userName +'</option>');
                        $("#ticket_queryUser").append(queryUser_option);
                    }
                }
            },
            error:function (data) {
                console.log("出错原因是:"+data);
            }
        });
    },
    selectTime:function(){
        $("#Timer").daterangepicker(CreateTicket.options,
            function(start, end, label) {
                var stime=start.format('YYYY-MM-DD HH:mm'),
                    etime=end.format('YYYY-MM-DD HH:mm');
                CreateTicket.params.startTime=stime;
                CreateTicket.params.endTime=etime;
                $("#Timer input").val(stime + " -- "+etime);
            });
    },
    tinymce:function () {
        tinymce.init({
            selector: 'textarea',
            height: 400,
            theme: 'modern',
            plugins: [
                'advlist autolink lists link image charmap print preview hr anchor pagebreak',
                'searchreplace wordcount visualblocks visualchars code fullscreen',
                'insertdatetime media nonbreaking save table contextmenu directionality',
                'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'
            ],
            toolbar1: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
            toolbar2: 'print preview media | forecolor backcolor emoticons | codesample',
            image_advtab: true,
            templates: [
                { title: 'Test template 1', content: 'Test 1' },
                { title: 'Test template 2', content: 'Test 2' }
            ],
        });
    },
    Cancel:function () {
        CreateTicket.params={
            title:'',  //工单标题
            content:'',  //工单内容
            tag:'',  //标签
            orgId:'',   //所属团队
            handler:'',  //所属人员
            severity:'',    //紧急度
            priority:'',  //优先级
            startTime:'',
            endTime:''
        };


    },
    Preview:function () {
        window.location.href = '/previewTicket/';
        window.localStorage.setItem('orderId',CreateTicket.orderId);
        window.localStorage.setItem("sourcePath",window.location.pathname);
    },
    Save:function () {
        //title
        CreateTicket.params.title=$("#ticket_title").val();

        //save content
        var activeEditor = tinymce.activeEditor;
        var editBody = activeEditor.getBody();
        activeEditor.selection.select(editBody);
        var text = activeEditor.selection.getContent( { 'format' : 'text' } );
        CreateTicket.params.content=text;
        // save tag
        CreateTicket.params.tag= $("#ticket_tag").val();

        //save orgId
        CreateTicket.params.orgId=$("#ticket_queryOrg").find("option:selected").val();

        //save handler
        CreateTicket.params.createuser=CreateTicket.params.handler=$("#ticket_queryUser").find("option:selected").val();

        //save severity
        CreateTicket.params.severity = $("#ticket_severity").find("option:selected").val();

        //save priority
        CreateTicket.params.priority = $("#ticket_priority").find("option:selected").val();

        $.ajax({
            type:"POST",
            dataType:'json',
            data:CreateTicket.params,
            url:api_config.createWorkOrder,
            success:function(data){
               if(data.code  == 200){
                   CreateTicket.orderId=data.id;
                   CreateTicket.Preview();
               }
            },
            error:function (data) {
                console.log("出错原因是:"+data);
            }
            }
        )
    },
};

$(document).ready(function () {
    CreateTicket.init();
});

