
function BeforeFormSubmit(form_ele) {

 console.log(form_ele);
 //$('form input[disabled]').prop("disabled", false);//�޸�Ϊ���ύ
 $("form").find("[disabled]").removeAttr("disabled");//�޸�Ϊ    ���ύ

 $('select[m2m_right="yes"] option').prop('selected', true);

 return true;
}


function MoveEleTo(from_ele, target_ele_id) {
 //move options from from_ele to target ele
 var field_name = $(from_ele).parent().attr("field_name");//��option��
 if (target_ele_id.endsWith('_from')) {//�ж��Ƿ�
     var new_target_id = "id_" + field_name + "_to";
 } else {
     var new_target_id = "id_" + field_name + "_from";
 }
 //����һ���±�ǩ
 var opt_ele = "<option value='" + $(from_ele).val() + "'ondblclick=MoveEleTo(this,'" + new_target_id + "')>" + $(from_ele).text() + "</option>";
 $("#" + target_ele_id).append(opt_ele);//��ӵ���һ��ѡ��
 $(from_ele).remove();//�Ƴ�ѡ�е�

}

