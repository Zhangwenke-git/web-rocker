//设置iframe自适应高度和宽度
		function iFrameHeight() {
			var ifm= document.getElementById("html_display1");
			var subWeb = document.frames ? document.frames["html_display1"].document : ifm.contentDocument;
			if(ifm != null && subWeb != null) {
			   ifm.height = subWeb.body.scrollHeight+20;
			   ifm.width = subWeb.body.scrollWidth;
			}
		}



//弹出数据库连接地址
		$(function () {
			$("#dbconnect").click(function (e) {
				$('#dbconnect_modal').modal({backdrop: 'static'});
				$('#dbconnect_modal').modal('show');

			});
			$("#database1_clear").click(function (e) {
				$(':input', '#dbconnect_form')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#data_display").empty();
			});
			$("#database2_clear").click(function (e) {
				$(':input', '#dbconnect_form1')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#data_display1").empty();
			});
			$("#database3_clear").click(function (e) {
				$(':input', '#dbconnect_form2')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#data_display2").empty();
			});


			//提交连接数据库模态框中的数据TAB1
			$('#dbconnect_form_btn').on('click', function () {

				$("#dbconnect_table").empty();
				var $btn = $(this).button('loading');
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#dbconnect_form').serialize();
				$("#data_display").empty();

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/dbconnect/1/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					// beforeSend:function(){
					// 	loading("正在请求，请稍后...")
					// },
					success: function (res) {
						$("#data_display").empty();
						if (res.success){
							var column_str = '<thead><tr>';
							$.each(res.result.column, function (colIndex, col) {
								column_str += '<th>' + col +'</th>'
							});
							column_str +='</tr></thead>';
							$("#data_display").append(column_str);

							var data_str = '<tbody>';
							$.each(res.result.data, function (dataIndex, data) {
								var tr_str = '<tr>';
								$.each(data, function (itemIndex, item) {
									tr_str += '<td>'+item +'</td>';
								});
								tr_str+='/tr';
								data_str += tr_str;

							});
							data_str +='</tbody>';
							$("#data_display").append(data_str);
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;
							swal({
                                text:error,
                                type:'error'
                            });
						}

					},
					error: function (jqXHR,textStatus,errorThrown) {
							var error = '错误码：'+textStatus+'，'+'原因：'+errorThrown;

							swal({
                                text:error,
                                type:'error'
                            });
					}
				});
				return false;
			});


			//提交连接数据库模态框中的数据TAB2
			$('#dbconnect_form_btn1').on('click', function () {
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#dbconnect_form1').serialize();
				$("#data_display1").empty();
				var $btn = $(this).button('loading');
				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/dbconnect/2/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {
						if (res.code==200){
							$("#data_display1").empty();
							var data_str = res.data;
							$('#data_display1').append(syntaxHighlight(data_str));

							$btn.button('reset');
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;
							swal({
                                text:error,
                                type:'error'
                            });
							$btn.button('reset');
						}
					},
					error: function (xhr) {
						
						$btn.button('reset');
					}
				});
				return false;
			});

			//提交连接数据库模态框中的数据TAB3
			$('#dbconnect_form_btn2').on('click', function () {
				$("#dbconnect_table2").empty();
				var $btn = $(this).button('loading');
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#dbconnect_form2').serialize();
				$("#data_display2").empty();

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/dbconnect/3/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {

						if (res.code==200){
							$("#data_display2").empty();
							var data_str = res.data;
							$('#data_display2').append(syntaxHighlight(data_str));
							$btn.button('reset');
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;
							swal({
                                text:error,
                                type:'error'
                            });
							$btn.button('reset');
						}

					},
					error: function (xhr) {
						
						$btn.button('reset');
					}
				});
				return false;
			});
		});


//弹出linux日志
        $(function () {
			$("#log_manager").click(function (e) {
				$('#log_manager_modal').modal({backdrop: 'static'});
				$('#log_manager_modal').modal('show');
			});

			$("#log1_clear").click(function (e) {
				$(':input', '#log_form1')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#logcontent").empty();
			});
			//提交日志服务器模态框中的数据TAB1
			$('#log_form_btn').on('click', function () {
				$("#logcontent").empty();
				var $btn = $(this).button('loading');
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#log_form1').serialize();
				$("#logcontent").empty();

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/log/1/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {
						if (res.code==200){
							$("#logcontent").empty();
							var data_str = res.data;
							$("#logcontent").append(data_str);
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;
							swal({
                                text:error,
                                type:'error'
                            });
							$btn.button('reset');
						}

					},
					error: function (xhr) {

						$btn.button('reset');
					}
				});
				return false;
			});
		});



//数据对面模块
        $(function () {
			$("#compare").click(function (e) {
				$('#data_compare_modal').modal({backdrop: 'static'});
				$('#data_compare_modal').modal('show');
			});
			//点击清除按钮，清除所有已填写数据
			$("#comapre1_clear").click(function (e) {
				$(':input', '#compare_form1')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#html_display1").removeAttr("src");
			});

			//提交数据对比模态框中的数据TAB1
			$('#compare_form1').on('submit', function () {
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#compare_form1').serialize();
				$("#html_display1").removeAttr("src");

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/compare/1/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {
						if (res.code == 200){
							$("#html_display1").removeAttr("src");
							var data_str = res.data;
							$("#html_display1").attr("src",data_str)
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;
							swal({
                                text:error,
                                type:'error'
                            });
						}

					},
					error: function (xhr) {

					}
				});
				return false;
			});
		});



//快速请求模块
		$(function () {
			//弹出快速请求的模态框
			$("#request_test").click(function (e) {
				$('#requestPage').modal({backdrop: 'static'});
				$('#requestPage').modal('show');

				$("#request_url").empty();
				$("#request_headers").empty();
				$("#request_method").empty();
				$("#request_body").empty();
				$("#request_type").empty();
				$("#response_statue").empty();
				$("#response_body").empty();
				$("#response_duration").empty();
				$("#response_headers").empty();
				$(':input', '#form_request')
					.not(':button, :submit, :reset, :hidden')
					.val('')

			});

			//提交快速请求模态框中的数据并返回
			$('#form_request').on('submit', function () {
					$("#request_url").empty();
					$("#request_headers").empty();
					$("#request_method").empty();
					$("#request_body").empty();
					$("#request_type").empty();
					$("#response_statue").empty();
					$("#response_body").empty();
					$("#response_duration").empty();
					$("#response_headers").empty();
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#form_request').serialize();

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/request/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {
						// var str = '<ul style="color:gray;" class="list-unstyled">'
						// 	+ '<li>Code: ' + '<strong style="color:red;">' + res.code + '</strong>' + '</li>'
						// 	+ '<li>Duration: ' + '<strong style="color:green;">' + res.duration + '</strong>' + '</li>'
						// 	+ '<li>Result: ' + '<pre style="height:370px;">' + res.response_body + '</pre>' + '</li>'
						// 	+ '</ul>';
						//
						// $("#response").append(str);

						$("#request_url").html(res.url);
						$("#request_method").html(res.method);

						var str_request_headers = '<pre>' + res.request_headers + '</pre>';
						$("#request_headers").append(str_request_headers);

						var str_request_body = '<pre>' + res.request_body + '</pre>';
						$("#request_body").append(str_request_body);

						$("#request_type").html(res.params_type);
						$("#response_statue").html(res.code);

						var str_response_body = '<pre style="height:370px;">' + res.response_body + '</pre>';
						$("#response_body").append(str_response_body);

						$("#response_duration").html(res.duration);

						var str_response_headers = '<pre>' + res.response_headers + '</pre>';
						$("#response_headers").append(str_response_headers);


					},
					error: function (xhr) {

					}
				});
				return false;
			});
		});



//json格式化
		$(function () {
			$("#json_format_btn").click(function (e) {
				$('#json_format_modal').modal({backdrop: 'static'});
				$('#json_format_modal').modal('show');
			});

			$("#json_clear").click(function (e) {
				$(':input', '#json_form')
					.not(':button, :submit, :reset, :hidden')
					.val('')
					.removeAttr('checked')
					.removeAttr('selected');
				$("#json_content").empty();
			});

			//提交JSON格式化模态框中的数据
			$('#json_form').on('submit', function () {
				var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
				var args = $('#json_form').serialize();
				$("#json_content").empty();

				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/public/json/format/",
					data: {"args": args, "csrfmiddlewaretoken": csrftoken},
					contentType: 'application/x-www-form-urlencoded',
					success: function (res) {
						if (res.code==200){
							$("#json_content").empty();
							var data_str = res.data;
							$('#json_content').append(syntaxHighlight(data_str));
						}else{
							var error = '错误码：'+res.code+'，'+'原因：'+res.message;

							swal({
                                text:error,
                                type:'error'
                            });
						}

					},
					error: function (xhr) {

					}
				});
				return false;
			});
		});


//Json格式数据高亮显示
		function syntaxHighlight(json) {
		if (typeof json != 'string') {
			json = JSON.stringify(json, undefined, 2);
		}
		json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function(match) {
			var cls = 'number';
			if (/^"/.test(match)) {
				if (/:$/.test(match)) {
					cls = 'key';
				} else {
					cls = 'string';
				}
			} else if (/true|false/.test(match)) {
				cls = 'boolean';
			} else if (/null/.test(match)) {
				cls = 'null';
			}
			return '<span class="' + cls + '">' + match + '</span>';
		});
	}




//函数助手
