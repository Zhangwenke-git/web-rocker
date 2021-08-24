//勾选
function SelectAll(ele) {
    if ($(ele).prop("checked")) {//如果勾选框
        $("input[tag='obj_checkbox']").prop("checked", true);//勾选
    } else {
        $("input[tag='obj_checkbox']").prop("checked", false);//不勾选
    }
}

//end SelectAll
function ActionValidation(form_ele) {
    if ($("select[name='action_select']").val() == "-1") {//没选中
        alert("Not yet！");
        return false;
    }
    var selected_objs = [];//要提交到后台的数据
    $("input[tag='obj_checkbox']").each(function () {
        if ($(this).prop("checked")) {////用于chekbox,radio   一个形参,获取值  两个形参 设置值
            selected_objs.push($(this).val());
        }
    });//end each
    if (selected_objs.length == 0) {
        alert("At least select an object！！");
        return false;
    }
    var selected_objs_ele = "<input name='selected_ids' type='hidden' value='" + selected_objs.toString() + "'>";//字符串形式
    $(form_ele).append(selected_objs_ele);
    return true;
}

// # ————————24PerfectCRM实现King_admin自定义操作数据————————
