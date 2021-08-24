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
                            if(item['name'].indexOf(search)>=0){
                                str +='<li onclick="switchToDetail(this);" class="list-group-item">'+ '<span class="btn btn-xxs btn-square btn-outline-info">' + item['name'] + '</span>' +'|'
                                + '<span class="btn btn-xxs btn-square btn-outline-danger">' + item['expression']+'</span>' +'|'+ '<a href="javascript:void(0)" class="btn btn-xxs light btn-success pull-right"><strong>Check</strong></a>'
                                + '</li>';
                            }
                        });
                        $("#helper_content").append(str);
                    }
                });
            }
        });


    switchToDetail = function(obj){

        var func_info = obj.textContent;
        var func_detail =  func_info.split('|');
        var func_str = func_detail[1];

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
                    $('#helper_desc').html("<span class='text-white'><code class='text-info'><strong>"+ result.name +"</strong></code>><code class='text-success'><strong>"+ result.expression +"</strong></code>" + result.description +"</span>")
                    $('#helper_param').html("<h4 class='text-white'>params format: <em class='text-danger'>" + result.parameter +"</em></h4><h5 class='mb-2'>params description:</h5><pre class='text-light ml-4'>"+ result.param_desc+ "</pre>")
                    $('#helper_outcome').html("<span class='text-white'>return: <code class='text-success'>" + result.return_type +"</code></span>")
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


