"""
1、首先在mysql中创建名为：django的数据库
2、python manage.py makemigrations   生成表结构
3、python manage.py migrate   同步表数据
4、创建root用户，超级管理员  python manage.py createsuperuser,并填写相关信息
5、数据库修改root用户权限,将is_super修改为1,这时候root用户才会有表格的增删改查的权限
6、在数据库中插入角色，插入角色与用户关联
7、在数据库中插入一级菜单，插入菜单和角色的关联
8、在数据库中插入图标，插入一级菜单和图标链接的关联
9、python manage.py runserver 8081即可，如果调试禁止的模式下，请用python manage.py runserver 8081 --insecure

"""
# 初始化资源SQL
sql = """
USE `django`;

INSERT  INTO `public_role`(`id`,`rolename`,`statue`,`create_time`,`update_time`) VALUES 
(1,'管理员',1,'2021-05-17 10:00:09.000000','2021-06-17 16:09:07.471086'),

INSERT  INTO `public_userprofile_role`(`id`,`userprofile_id`,`role_id`) VALUES (1,1,1);

INSERT  INTO `public_firstlayermenu`(`id`,`type`,`name`,`icon`,`url_type`,`url_name`,`order`) VALUES (1,1,'公共设置','glyphicon glyphicon-cog',0,'public_overview',1);

INSERT  INTO `public_role_menus`(`id`,`role_id`,`firstlayermenu_id`) VALUES (1,1,1);

INSERT  INTO `public_resource`(`id`,`name`,`link`,`upload`,`type`,`color`,`remark`,`parent_menus_id`) VALUES 
(1,'用户管理','/public/userprofile/','static/picture/icon/用户管理_rU9XS19.svg',2,5,NULL,1),
(2,'权限管理','/public/groups','static/picture/icon/权限管理_uaeXYtp.svg',2,3,NULL,1),
(3,'角色管理','/public/role/','static/picture/icon/角色管理_sw17X9V.svg',2,5,NULL,1),
(4,'一级菜单管理','/public/firstlayermenu/','static/picture/icon/一级菜单管理_ghPUYch.svg',2,2,NULL,1),
(5,'二级菜单管理','/public/submenu/','static/picture/icon/二级菜单管理_y0fptYI.svg',2,1,NULL,1);

"""

def init():
    pass