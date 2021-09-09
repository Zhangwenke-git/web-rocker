from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# Create your models here.


from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self,user_id, password,email,name):
        if not user_id:
            raise ValueError('Users must have an account id!')
        user = self.model(
            user_id=user_id,
            email = self.normalize_email(email),
            name = name
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id,password,email=None,name=None):
        user = self.create_user(
            user_id=user_id,
            password=password,
            email=email,
            name=name
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser=1
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        blank=True,
        null=True
    )

    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe('''
                                <a href=\"../password/\" class="btn btn-danger btn-sm" role="button">Reset Password</a>
                                '''))

    is_choice = (
        (0, "否"),
        (1, "是"),
    )
    is_superuser = models.SmallIntegerField(choices=is_choice, default=0, verbose_name="超级用户", help_text=mark_safe("""
    
    <div class="alert alert-warning border-0 bg-info alert-dismissible fade show py-2">
        <div class="d-flex align-items-center">
            <div class="font-35 text-dark"><i class='bx bx-info-square'></i>
            </div>
            <div class="ms-3">
                <h6 class="mb-0 text-dark">Info Alerts</h6>
                <div class="text-dark">管理员有所有表操作的权限，慎重勾选！</div>
            </div>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    
    """))
    user_id = models.CharField(max_length=32, unique=True, null=False, blank=False, verbose_name='用户ID')
    USERNAME_FIELD = 'user_id'  # 作为唯一的登录标识

    name = models.CharField(max_length=32,verbose_name='用户名')
    statue_choice = (
        (0, "否"),
        (1, "是"),
    )
    is_active = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="活动状态")
    sex_choice = (
        (0, "男"),
        (1, "女"),
        (2, "未知"),
    )
    sex = models.SmallIntegerField(choices=sex_choice, default=2, verbose_name="性别")

    study_choice = (
        (0, "未知"),
        (1, "高中"),
        (3, "大专"),
        (4, "本科"),
        (5, "研究生"),
        (6, "博士生"),
    )
    study = models.SmallIntegerField(choices=study_choice, default=0, verbose_name="学历")
    role = models.ManyToManyField('Role', blank=True, null=True, verbose_name='角色',help_text=mark_safe('<p class="text-dark small mt-1">Tips:hold down <kbd><kbd>ctrl</kbd></kbd>, to select more than one.</p>'))
    upload = models.ImageField(upload_to='static/picture/photo/',blank=True, null=True, verbose_name='头像')
    birthday = models.DateField(null=True, blank=True,verbose_name='出生年月')
    address = models.CharField(max_length=320, null=True, blank=True, verbose_name='现居地址')
    school = models.CharField(max_length=320, null=True, blank=True, verbose_name='毕业院校')
    skills = models.CharField(max_length=320, null=True, blank=True, verbose_name='技能')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    objects = UserProfileManager()
    REQUIRED_FIELDS = ['email','name',]

    def get_full_name(self):
        return self.name

    def get_account_id(self):
        return self.user_id

    def __str__(self):
        return self.user_id

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        verbose_name_plural = "用户信息表"
        permissions = (

            ('web_table_data', '可以允许访问表中数据'),
            ('web_table_data_batch_operation', '可以批量操作表中数据'),
            ('web_table_update_view', '可以允许访问修改页'),
            ('web_table_update', '可以允许更新数据'),
            ('web_table_add', '可以允许新增数据'),
            ('web_table_add_view', '可以允许访问新增数据页面'),
            ('web_table_delete', '可以允许删除数据'),
            ('web_table_delete_view', '可以允许访问删除数据页面'),
            ('password_reset_get', '可以允许访问修改密码页面'),
            ('password_reset_post', '可以允许访修改密码'),

        )


from django.contrib.auth.models import Group


class Groups(Group):
    description = models.CharField(max_length=320, null=True, blank=True, verbose_name='描述')

    class Meta:
        verbose_name_plural = '权限组'


class Role(models.Model):
    rolename = models.CharField(max_length=64, unique=True, verbose_name='角色名称')
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")
    menus = models.ManyToManyField('FirstLayerMenu', verbose_name='一层菜单', blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.rolename


class FirstLayerMenu(models.Model):
    type_choice = (
        (0, "api"),
        (1, "public"),
    )
    type = models.SmallIntegerField(choices=type_choice, default=1, verbose_name="类型")
    name = models.CharField('一层菜单名', max_length=64)
    icon = models.CharField('图标', default=mark_safe("glyphicon glyphicon-blackboard"), max_length=64)
    url_type_choices = ((0, '相关的名字'), (1, '固定的URL'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0, verbose_name="URL类型")
    url_name = models.CharField(max_length=64, verbose_name='一层菜单路径')
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')
    sub_menus = models.ManyToManyField('SubMenu', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "第一层菜单"


class SubMenu(models.Model):
    '''第二层侧边栏菜单'''
    type_choice = (
        (0, "api"),
        (1, "public"),
    )
    type = models.SmallIntegerField(choices=type_choice, default=1, verbose_name="类型")
    name = models.CharField('二层菜单名', max_length=64)
    url_type_choices = ((0, '相关的名字'), (1, '固定的URL'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0, verbose_name="URL类型")
    url_name = models.CharField(max_length=64, verbose_name='二层菜单路径')
    order = models.SmallIntegerField(default=0, verbose_name='菜单排序')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "第二层菜单"


class BusinessFunc(models.Model):
    name = models.CharField(max_length=64, unique=True,verbose_name='名称')
    expression = models.CharField(max_length=64,unique=True, verbose_name='表达式')

    parameter = models.CharField(max_length=128, verbose_name='入参', blank=True, null=True, help_text=mark_safe("""
        <span style="color:orange;" class="glyphicon glyphicon-question-sign">参数之间用分隔符"|"分离，例如：username|password </span>
    """))

    data_type = (
        (0, "String"),
        (1, "Dict"),
        (2, "List"),
        (3, "Int"),
        (4, "Boolean"),
        (5, "None"),
    )

    param_type = models.PositiveIntegerField(choices=data_type, default=0, verbose_name="类型")
    return_data_type = models.PositiveIntegerField(choices=data_type, default=5, verbose_name="类型")
    param_desc =  models.TextField(max_length=320,blank=True,null=True, verbose_name='参数解释')
    return_type = models.CharField(max_length=120, null=True, verbose_name='返回结果类型')
    description = models.CharField(max_length=128, verbose_name='描述')


    type_choice = (
        (0, "API"),
        (1, "Common"),
    )
    type = models.SmallIntegerField(choices=type_choice, default=1, verbose_name="类型")
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")

    class Meta:
        verbose_name_plural = '业务函数'

    def __str__(self):
        return "%s-%s-%s" % (self.name, self.expression, self.parameter)


class Retrieval(models.Model):
    name = models.CharField(max_length=64, unique=True,verbose_name='名称')
    link = models.CharField(max_length=64, blank=True, null=True, verbose_name='链接', help_text=mark_safe("""
        <span style="color:orange;" class="glyphicon glyphicon-question-sign"> 例如：/login </span>
    """))

    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")

    class Meta:
        verbose_name_plural = '全文检索'

    def __str__(self):
        return "%s" % (self.name)


class Resource(models.Model):
    name = models.CharField(max_length=64, unique=True,verbose_name='名称')
    link = models.CharField(max_length=64, blank=True, null=True, verbose_name='链接', default="#", help_text=mark_safe("""
        <span style="color:orange;" class="glyphicon glyphicon-question-sign"> 例如：/login </span>
    """))
    upload = models.FileField(upload_to='static/picture/icon/', blank=True, null=True, verbose_name='图片路径',
                              help_text=mark_safe(
                                  """<span style="color:orange;" class="glyphicon glyphicon-question-sign">.svg/.png/.jpeg格式 </span>"""))
    type_choice = (
        (0, "api"),
        (1, "public"),
    )
    type = models.SmallIntegerField(choices=type_choice, default=1, verbose_name="类型")

    parent_menus = models.ForeignKey(FirstLayerMenu, verbose_name='所属一级菜单',default=1,on_delete=models.CASCADE)
    color_choice = (
        (0, "default"),
        (1, "primary"),
        (2, "info"),
        (3, "success"),
        (4, "danger"),
        (5, "warning"),
    )
    color = models.SmallIntegerField(choices=color_choice, default=1, verbose_name="颜色")
    remark = models.CharField(max_length=640, blank=True, null=True, verbose_name='描述')

    class Meta:
        verbose_name_plural = '菜单图标管理'

    def __str__(self):
        return "%s|%s" % (self.type, self.name)


class Environment(models.Model):
    envir_id = models.CharField(max_length=64,unique=True, verbose_name='环境ID')
    name = models.CharField(max_length=64, verbose_name='名称')

    class Meta:
        verbose_name_plural = '应用环境'

    def __str__(self):
        return "%s" % (self.envir_id)


class Dbinfo(models.Model):
    name = models.CharField(max_length=128, unique=True,verbose_name='数据库简介')
    db_choice = (
        (0, "Mysql"),
        (1, "Oracle"),
        (2, "Other"),
    )
    dbtype = models.SmallIntegerField(choices=db_choice, default=1, verbose_name="数据库类型")
    dbhost = models.CharField(max_length=64,null=True,blank=True, verbose_name='数据库地址')
    dbport = models.CharField(max_length=64,null=True,blank=True, default=3306,verbose_name='数据区端口号')
    dbname = models.CharField(max_length=64,null=True,blank=True, verbose_name='数据库名称')
    dbuser = models.CharField(max_length=64,null=True,blank=True, verbose_name='数据库账户')
    dbpassword = models.CharField(max_length=64,null=True,blank=True, verbose_name='数据库密码')


    class Meta:
        verbose_name_plural = '数据库信息'

    def __str__(self):
        return "%s-%s" % (self.name, self.dbhost)




class LogServerinfo(models.Model):
    name = models.CharField(max_length=64, unique=True,verbose_name='日志服务器名称')
    logserver = models.CharField(max_length=64, null=True,blank=True,verbose_name='日志服务器地址')
    logport = models.CharField(max_length=64,null=True,blank=True,default=22, verbose_name='日志服务器端口号')
    logname = models.CharField(max_length=64, null=True,blank=True,verbose_name='日志服务器登录用户')
    logpwd = models.CharField(max_length=64, null=True,blank=True,verbose_name='日志服务器登录密码')


    class Meta:
        verbose_name_plural = '日志服务器名称'

    def __str__(self):
        return "%s-%s" % (self.name, self.logserver)



class Configurations(models.Model):

    environment = models.ForeignKey(Environment, verbose_name='测试环境', on_delete=models.CASCADE)
    dbinfo = models.ForeignKey(Dbinfo, verbose_name='默认数据库', on_delete=models.CASCADE)
    log_server_info = models.ForeignKey(LogServerinfo, verbose_name='默认日志服务器', on_delete=models.CASCADE)

    level_choice = (
        (0, "info"),
        (1, "debug"),
        (2, "warning"),
        (3, "error"),
    )
    loglevel = models.SmallIntegerField(choices=level_choice, default=0, verbose_name="日志级别")

    browser_choice = (
        (0, "Chrome"),
        (1, "Firefox"),
        (2, "IE"),
        (3, "Self-defined"),
    )
    browserType = models.SmallIntegerField(choices=browser_choice, default=0, verbose_name="浏览器")
    is_task = models.BooleanField(default=0, verbose_name="是否默认添加定时任务")
    task = models.DateTimeField(max_length=64, default="20:00", verbose_name="默认定时任务时间")
    is_HiddenWindowBeforeStart = models.BooleanField(default=0, verbose_name="是否启动前最小化窗口")
    is_CloseBrowserBeforeStart = models.BooleanField(default=0, verbose_name="是否启动前最关闭浏览器")
    is_CloseBrowserAfterEnd = models.BooleanField(default=0, verbose_name="是否结束后关闭浏览器")
    is_APIcaseFileCreate = models.BooleanField(default=1, verbose_name="是否启动前生成API的py测试文件")
    is_APIcaseFileRemove = models.BooleanField(default=0, verbose_name="是否结束后删除API的py测试文件")
    is_ClearReportLogBeforeStart = models.BooleanField(default=0, verbose_name="是否启动前清理日志和报告")
    test_integert = models.IntegerField(default=0,verbose_name='整数测试')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '测试环境信息'

    def __str__(self):
        return "%s" % (self.environment)


class CN_EN_MAP(models.Model):
    parent = models.CharField(max_length=64, unique=True, verbose_name='字段英文简称')
    cn_name = models.CharField(max_length=128, verbose_name='字段中文简称')
    children = models.CharField(max_length=320, blank=True,null=True,verbose_name='子列表',help_text=mark_safe("""
        <span style="color:gray;font-size:smaller;" class="glyphicon glyphicon-question-sign">填写子列表，譬如主字段为：Username，则此处填写为:UserName;USER;USERNAME;username;UserNm，子元素之间用";"隔开 </span>
    """))
    statue_choice = (
        (0, "作废"),
        (1, "有效"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=1, verbose_name="状态")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '中英文字段映射'

    def __str__(self):
        return "%s-%s-%s" % (self.parent,self.cn_name,self.children)



class StepLog(models.Model):
    user = models.CharField(max_length=16,blank=False,null=False,verbose_name="操作用户")
    action = models.CharField(max_length=8,blank=False,null=False,verbose_name="类型")
    model_name = models.CharField(max_length=32,blank=False,null=False,verbose_name="表信息")
    origin = models.JSONField(null=True,verbose_name="原始数据")
    detail = models.JSONField(null=True,verbose_name="操作详情")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='操作日期')

    class Meta:
        verbose_name_plural = '操作记录表'

    def __str__(self):
        return "%s-%s-%s" % (self.user,self.action,self.model_name)


class TodoList(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    content = models.CharField(max_length=32,blank=False,null=False,verbose_name="代办内容")
    statue_choice = (
        (0, "未完成"),
        (1, "已完成"),
    )
    statue = models.SmallIntegerField(choices=statue_choice, default=0, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')