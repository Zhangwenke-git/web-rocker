sql = """

USE `django`;

INSERT  INTO `public_role`(`id`,`rolename`,`statue`,`create_time`,`update_time`) VALUES 
(1,'管理员',1,'2021-05-17 10:00:09.000000','2021-06-17 16:09:07.471086'),
(2,'普通用户',1,'2021-06-17 16:09:39.484122','2021-07-02 18:08:26.328793'),
(3,'访客',1,'2021-06-17 17:33:46.936672','2021-06-17 18:26:00.366813');

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