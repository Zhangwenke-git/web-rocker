from django.http import JsonResponse
from django.urls import resolve  # resolve解析URL
from django.shortcuts import render, redirect, HttpResponse  # 页面返回
from backend.permission_list import perm_dic  # 权限字典
from utils.pubulic import logger

logger = logger.Logger("permission")

def perm_check(*args, **kwargs):
    request = args[0]


    resolve_url_obj = resolve(request.path)  # 反解URL路径#获取当前的URL# resolve解析URL#生成实例
    current_url_name = resolve_url_obj.url_name  # 当前url的url_name
    logger.debug('The logined user is:{request.user,} and the current url is: {current_url_name}')

    permission_list = request.user.user_permissions.values_list('codename')  # 根据 登陆的ID 获取 拥有的权限列表
    logger.debug('The permission list is: {permission_list}')
    permission_group = request.user.groups.all().values_list('permissions__codename')  # 根据 登陆的ID 获取 拥有的组
    logger.debug(f'The permission group is: {permission_group}')

    match_key = None
    match_results = [False, ]  # 后面会覆盖，加个False是为了让all(match_results)不出错

    for permission_key, permission_val in perm_dic.items():  # 从权限字典中取相关字段 #crm_table_index':['','table_index','GET',[],{},],
        if ((permission_key),) in permission_list or ((permission_key),) in permission_group:  # 权限列表是元组
            per_url_name = permission_val[0]  # URL
            per_method = permission_val[1]  # GET #POST #请求方法
            perm_args = permission_val[2]  # 列表参数
            perm_kwargs = permission_val[3]  # 字典参数
            custom_perm_func = None if len(permission_val) == 4 else permission_val[4]  # url判断 #自定义权限钩子
            # 'crm_can_access_my_clients':['table_list','GET',[],{'perm_check':,'arg':'test'}, custom_perm_logic.only_view_own_customers],
            # print('URL:',per_url_name,'请求方法:',per_method,'列表参数:',perm_args,'字典参数:',perm_kwargs,'自定义权限钩子:',custom_perm_func)


            if per_url_name == current_url_name:  # 权限字典的 URL  ==当前请求的url #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                if per_method == request.method:  # 权限字典的 请求方法 == 当前请求的方法  #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                    args_matched = False  # 参数匹配 #仅供参数
                    for item in perm_args:  # 循环列表参数 #crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                        request_method_func = getattr(request, per_method)  # 反射 #请求方法 #GET #POST
                        if request_method_func.get(item, None):  # 如果request字典中有此参数
                            args_matched = True
                        else:
                            logger.error("The parameter are not matched!")
                            args_matched = False
                            break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                    else:
                        args_matched = True  # 没有执行 break 表示 列表匹配成功 #防止列表没有使用参数时出错

                    # 匹配有特定值的参数
                    kwargs_matched = False
                    for k, v in perm_kwargs.items():  # 循环字典参数#crm_table_index':['URL','请求方法',[列表参数],{字典参数},],
                        request_method_func = getattr(request, per_method)  # 反射 #请求方法 #GET #POST
                        arg_val = request_method_func.get(k, None)  # request字典中有此参数
                        logger.debug(f"perm kwargs check: {arg_val, type(arg_val), v, type(v)}")
                        if arg_val == str(v):  # 匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=的参数
                            kwargs_matched = True
                        else:
                            kwargs_matched = False
                            break  # 有一个参数不能匹配成功，则判定为假，退出该循环。
                    else:
                        kwargs_matched = True

                    # 自定义权限钩子
                    perm_func_matched = False
                    if custom_perm_func:  # 如果有定义
                        if custom_perm_func(request, args, kwargs):  # def only_view_own_customers(request,*args,**kwargs):
                            perm_func_matched = True
                        else:
                            perm_func_matched = False  # 使整条权限失效
                            logger.error(f'Fail to execute self-defined hook: {perm_func_matched}')
                    else:  # 没有定义权限钩子，所以默认通过
                        perm_func_matched = True

                    match_results = [args_matched, kwargs_matched, perm_func_matched]  # 列表
                    logger.debug(f"The matched result is: {match_results}")  # [True, True, True]
                    if all(match_results):  # 都匹配上了 #都返回 True
                        match_key = permission_key  # 给 match_key = None 赋值
                        break  # 跳出大循环

    if all(match_results):  # 如果都匹配成功     #'crm_table_index':['table_index','GET',[],{},],
        app_name, *per_name = match_key.split('_')  # 先给app_name赋一个值，其他的值都给*per_name     'crm_table_index':
        logger.debug(f"The permission name is: {match_key} and permissions are:{match_results}")  # crm_000_only_view_CourseRecord_POST [True, True, True]
        logger.info(f'Splite the permission: f{app_name, *per_name}')  # crm 000 only view CourseRecord POST
        perm_obj = '%s.%s' % (
        app_name, match_key)  # 'crm.table_index' #    url(r'^(\w+)/$', views.table_index, name='table_index'),  # 单个具体app页面
        logger.debug("Create permission: {perm_obj}")  # crm.crm_000_only_view_CourseRecord_POST
        if request.user.has_perm(perm_obj):
            logger.info("The user have the permission!")
            return True
        else:
            logger.info("The user does not have the permission!")
            return False
    else:
        logger.debug(f"Fail to get the user's permission!")


def check_permission(func):

    def inner(*args, **kwargs):
        logger.debug(f'Start to match permission: {type(args)}')
        request = args[0]  # 请求第一个
        if request.user.id == None:
            logger.debug('The user has not login!')
            return redirect('/login/')  # 返回登陆页面
        else:
            if request.user.is_superuser == True:
                logger.info(f"The user is Administrator!")
                return func(*args, **kwargs)  # 直接返回 真
            if not perm_check(*args, **kwargs):  # 如果返回不为真 #没权限
                logger.debug(f'The user have no access:{perm_check(*args, **kwargs)} to get the page!')
                request = args[0]
                check_result = {"auth":False}
                # return JsonResponse(check_result,safe=False)
                return render(request, '403.html')
            logger.debug(f"The user have access: {func(*args, **kwargs)} to get the page!")  # <HttpResponse status_code=00, "text/html; charset=utf-">
            return func(*args, **kwargs)
    return inner  # 返回 真或假

