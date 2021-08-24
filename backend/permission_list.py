from backend import permission_hook

perm_dic = {

   # 'web_table_list': ['crm', 'GET', [], {}, permission_hook.my_own_data,],  # 可以查看CRM APP里所有数据库表
   #  'api_table_list': ['api', 'GET', [], {}, ],  # 可以查看API APP里所有数据库表
   #  'public_table_list': ['public', 'GET', [], {}, ],  # 可以查看CRM APP里所有数据库表
    'web_table_data': ['table_data_list', 'GET', [], {}, ],  # 可以查看每张表里所有的数据
    'web_table_data_batch_operation': ['table_data_list', 'POST', [], {},],  # 可以查看每张表里所有的数据

    'web_table_update': ['table_data_update', 'POST', [], {}],  # 可以对表里的每条数据进行修改
    'web_table_update_view': ['table_data_update', 'GET', [], {}],  # 可以访问表里每条数据的修改页

    'web_table_add': ['table_data_add', 'POST', [], {}],  # 添加数据
    'web_table_add_view': ['table_data_add', 'GET', [], {}],  # 访问添加数据页面

    'web_table_delete': ['table_data_delete', 'POST', [], {}],  # 删除数据
    'web_table_delete_view': ['table_data_delete', 'GET', [], {}],  # 访问删除数据页面


    'password_reset_post':['password_reset','PSOT',[],{}],
    'password_reset_get':['password_reset','GET',[],{}],

}