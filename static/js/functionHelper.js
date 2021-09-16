$(function () {
    $("#func_helper_btn").click(function (e) {
        $('#func_helper_modal').modal({backdrop: 'static'});
        $('#func_helper_modal').modal('show');
    });


    $("#helper_keyword").keyup(function(){
            var search = $(this).val();
            var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
            if(search=="" || search==null){
                $("#helper_content").empty();
            }else{
                $.ajax({
                    type:"POST",
                    url:"/public/functions/search/",
                    data:{"search":search, "csrfmiddlewaretoken":csrftoken},
                    DataType:"json",
                    success: function(result_list) {
                        $("#helper_content").empty();
                        var str = "";
                        $.each(result_list,function(itemIndex,item){
                            str +='<a class="dropdown-item" href="javascript:;"><div class="d-flex align-items-center text-secondary"><div class="notify bg-light-primary text-primary"><i class="lni lni-direction"></i></div><div class="flex-grow-1"><h6 class="msg-name" onclick="switchToDetail(this);">'+item.expression+'<span class="msg-time float-end "><p class="badge bg-light text-dark">查看详情</p></span></h6><p class="msg-info">'+item.name+'</p></div></div></a>'
                        });
                        $("#helper_content").append(str);
                    }
                });
            }
        });


    switchToDetail = function(obj){

        var func_info = obj.textContent;
        var func_str = func_info.slice(0,-4);

        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if(func_str=="" || func_str==null){
            $("#helper_content").empty();
        }else{
            $.ajax({
                type:"POST",
                url:"/public/functions/"+func_str+"/",
                data:{"func_str":func_str, "csrfmiddlewaretoken":csrftoken},
                DataType:"json",
                success: function(result) {

                    $("#helper_content").empty();
                    $('#helper_desc').html("<h6><code><strong>"+ result.name +"</strong></code>><code><strong>"+ result.expression +"</strong></code>>" + result.description +"</h6>")
                    $('#helper_param').html("<h6>参数格式: <em class='text-info'>" + result.parameter +"</em></h6><h6 class='mb-2'>参数描述: </h6><pre class='text-secondary ml-4'>"+ result.param_desc+ "</pre>")
                    $('#helper_outcome').html("<h6>返回: <code class='text-warning'>" + result.return_type +"</code></span>")
                }
            });
        }
    };
    $("#helper_clear").click(function(){
        $("#helper_content").empty();
        $("#helper_desc").empty();
        $("#helper_param").empty();
        $("#helper_outcome").empty();
    });
});


