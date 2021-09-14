"""
1、创建数据库django，并链接数据库，并删除各个应用下migrations中除了__init__.py意外的Py文件
2、python manage.py makemigrations
3、python manage.py migrate
4、

"""

sql = """

USE `django`;

INSERT  INTO `public_role`(`id`,`rolename`,`statue`,`create_time`,`update_time`) VALUES 
(1,'管理员',1,'2021-05-17 10:00:09.000000','2021-06-17 16:09:07.471086'),
(2,'普通用户',1,'2021-06-17 16:09:39.484122','2021-07-02 18:08:26.328793'),
(3,'访客',1,'2021-06-17 17:33:46.936672','2021-06-17 18:26:00.366813');

INSERT  INTO `public_userprofile_role`(`id`,`userprofile_id`,`role_id`) VALUES (1,1,1);

INSERT  INTO `public_firstlayermenu`(`id`,`type`,`name`,`icon`,`url_type`,`url_name`,`order`) VALUES 
(1,1,'公共设置','glyphicon glyphicon-cog',0,'public_overview',1),
(2,1,'配置中心','glyphicon glyphicon-blackboard',0,'public_config',2),
(3,0,'API应用','glyphicon glyphicon-blackboard',0,'api_overview',3),
(4,0,'测试报告','glyphicon glyphicon-blackboard',0,'api_report',4),
(5,0,'数据分析','glyphicon glyphicon-blackboard',0,'api_analytics',5);

INSERT  INTO `public_role_menus`(`id`,`role_id`,`firstlayermenu_id`) VALUES 
(1,1,1),
(3,1,2),
(10,1,3),
(11,1,4),
(12,1,5),
(2,2,2),
(7,2,3),
(8,2,4),
(9,2,5),
(4,3,3),
(5,3,4),
(6,3,5);


INSERT  INTO `public_resource`(`id`,`name`,`link`,`upload`,`type`,`color`,`remark`,`parent_menus_id`) VALUES 
(1,'用户管理','/public/userprofile/','static/picture/icon/用户管理_rU9XS19.svg',1,5,NULL,1),
(2,'权限管理','/public/groups','static/picture/icon/权限管理_uaeXYtp.svg',1,3,NULL,1),
(3,'角色管理','/public/role/','static/picture/icon/角色管理_sw17X9V.svg',1,5,NULL,1),
(4,'一级菜单管理','/public/firstlayermenu/','static/picture/icon/一级菜单管理_ghPUYch.svg',1,2,NULL,1),
(5,'二级菜单管理','/public/submenu/','static/picture/icon/二级菜单管理_y0fptYI.svg',1,1,NULL,1),
(6,'全局检索','/public/retrieval/','static/picture/icon/全文检索_WpU2ID6.svg',1,1,NULL,2),
(7,'业务函数','/public/businessfunc/','static/picture/icon/业务管理_q1d1ojN.svg',1,4,NULL,2),
(8,'图标管理','/public/resource/','static/picture/icon/科组部门管理.svg',1,1,NULL,1),
(9,'项目管理','/api/apiproject/','static/picture/icon/空白带领用核算统计_1_t20awjJ.svg',0,1,NULL,3),
(10,'模板管理','/api/templates/','static/picture/icon/备播带借还.svg',0,3,NULL,3),
(11,'用例集管理','/api/testsuit/','static/picture/icon/光盘库管理.svg',0,4,NULL,3),
(12,'用例管理','/api/testcase/','static/picture/icon/空白介质入库.svg',0,5,NULL,3),
(13,'场景管理','/api/scenario/','static/picture/icon/母版统计_3.svg',0,1,NULL,3),
(14,'字段映射','/public/cn_en_map/','static/picture/icon/日记管理.svg',1,1,NULL,2),
(15,'环境管理','/public/environment/','static/picture/icon/签审人员查询_3.svg',1,1,NULL,1),
(16,'数据库信息','/public/dbinfo/','static/picture/icon/临时芯号申请.svg',1,1,NULL,2),
(17,'Linix日志','/public/logserverinfo/','static/picture/icon/送播送带_1.svg',1,1,NULL,2),
(18,'配置应用','/public/configurations/','static/picture/icon/审批管理_2.svg',1,1,NULL,2),
(19,'SQL信息管理','/api/sql/','',0,3,NULL,3),
(20,'操作日志','/public/steplog','',1,4,'记录每个表的操作日志，如增删改',1);


DELETE FROM `auth_permission` WHERE `name` NOT LIKE '%可以%';
"""