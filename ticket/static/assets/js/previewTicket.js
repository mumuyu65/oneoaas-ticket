/**
 * Created by yangyangyu on 2017/5/3.
 * previewTicket
 */
var PreviewTicket={
    OrderId:'',
    init:function () {
        PreviewTicket.OrderId=window.localStorage.getItem('orderId');
        PreviewTicket.initInterface();
        PreviewTicket.initContent();
    },
    initInterface:function () {
        var pathname=window.localStorage.getItem('sourcePath');
        switch (pathname){
            case '/':
                $("#ticket_return").html("返回到创建工单");
                break;
            case '/searchTicket/':
                $("#ticket_return").html("返回到查询工单页面");
                break;
            case '/searchKnowledge/':
                $("#ticket_return").html("返回到知识库");
                break;
            default:
                return false;
        }
        $("#ticket_return").click(function () {
            window.location.href=pathname;
        });
    },
    initContent:function () {
        if(PreviewTicket.OrderId){
            $.ajax({
                url:api_config.getOrderInfoById,
                method:'POST',
                dataType:'json',
                data:{orderId:PreviewTicket.OrderId},
                beforeSend:function () {

                },
                success:function (data) {
                    if(data.code == 200){
                        var templateObj=data.content;
                        $("#preview_title").html(templateObj.title);
                        $("#preview_content").html(templateObj.content);
                        
                        //交互操作
                        $("#ticket_knowledge").click(function () {
                            PreviewTicket.knowledge()
                        });  //知识库
                        
                        $("#ticket_close_order").click(function () {
                            PreviewTicket.closeOrder()
                        });  //关闭工单

                        $("#preview_edit").click(function () {
                            $("#preview_title").html(templateObj.title);
                            $(this).css("display","none");
                            $("#preview_session").css("display","none");
                            $("#preview_button").css("display","none");
                            $("#preview_edit_button").css("display","block");
                            PreviewTicket.edit();
                        });  //编辑工单内容和标题
                    }
                },
                error:function () {
                    console.log("error.........");
                }
            })
        }
    },
    knowledge:function () {
        $.ajax({
            url:api_config.joinKnowledge,
            method:"POST",
            data:{orderId:PreviewTicket.OrderId},
            dataType:'json',
            success:function (data) {
               if(data.code == 200){
                   alert(data.msg);
               }
            },
            error:function () {
                console.log("error.........");
            }
        })
    },
    closeOrder:function () {
        $.ajax({
            url:api_config.closeWorkOrder,
            method:"POST",
            data:{orderId:PreviewTicket.OrderId},
            dataType:'json',
            success:function (data) {
                if(data.code == 200){
                    alert(data.msg);
                }
            },
            error:function () {
                console.log("error.........");
            }
        })
    },
    edit:function () {
        tinymce.init({
            selector: '#preview_content',
            height: 400,
            theme: 'modern',
            language:'zh-CN',
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
        $("#preview_cancel").click(function () {
            PreviewTicket.cancel();
        });
        $("#preview_save").click(function () {
            PreviewTicket.save();
        });
    },
    cancel:function () {
        $("#preview_session").css("display","block");
        $("#preview_button").css("display","block");
        $("#preview_edit_button").css("display","none");
        $("#preview_edit").css("display","block");
        tinymce.remove();
    },
    save:function(){
        //save content
        var activeEditor = tinymce.activeEditor;
        var editBody = activeEditor.getBody();
        activeEditor.selection.select(editBody);
        var text = activeEditor.selection.getContent( { 'format' : 'text' } );
        var params={
            orderId:PreviewTicket.OrderId,
            content:text
        };
        $.ajax({
            url:api_config.updateOrderById,
            method:'POST',
            dataType:'json',
            data:params,
            success:function (data) {
                if(data.code == 200){
                    alert(data.msg);
                    PreviewTicket.cancel();
                }
            },
            error:function () {
                console.log("error");
            }
        });
    }
};

$(document).ready(function () {
    PreviewTicket.init();
});
