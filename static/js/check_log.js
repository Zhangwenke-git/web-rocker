function check_log_details(id){
        $('#check_log_modal').modal({backdrop: 'static'});
        $('#check_log_modal').modal('show');
        $("#before_change").empty();
        $("#after_change").empty();
        $("#operation").empty();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

        $.ajax({
            type:"POST",
            url:"/table/log/check/",
            data:{"id":id, "csrfmiddlewaretoken":csrftoken},
            DataType:"json",
            success: function(result) {
                $("#before_change").append(result.origin);
                $("#after_change").append(result.detail);
                $("#operation").append(result.action);
            }
        });


}