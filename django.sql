/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 8.0.23 : Database - django
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`django` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `django`;

/*Table structure for table `api_apiproject` */

DROP TABLE IF EXISTS `api_apiproject`;

CREATE TABLE `api_apiproject` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `description` varchar(320) DEFAULT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_apiproject` */

insert  into `api_apiproject`(`id`,`name`,`description`,`statue`,`create_time`,`update_time`) values 
(4,'SPCG-UUMS-AUTH','中台技术UUMS用户认证',1,'2021-05-29 16:52:38.217723','2021-05-29 17:08:09.473950'),
(5,'CFETS-ODM-XBOND','交易中心ODM债券交易系统',1,'2021-05-29 17:06:41.749606','2021-05-29 17:07:01.691480');

/*Table structure for table `api_book` */

DROP TABLE IF EXISTS `api_book`;

CREATE TABLE `api_book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_book` */

/*Table structure for table `api_book_pub` */

DROP TABLE IF EXISTS `api_book_pub`;

CREATE TABLE `api_book_pub` (
  `id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `publisher_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_book_pub_book_id_publisher_id_44a4002c_uniq` (`book_id`,`publisher_id`),
  KEY `api_book_pub_publisher_id_3e5d98df_fk_api_publisher_id` (`publisher_id`),
  CONSTRAINT `api_book_pub_book_id_3eafc3cd_fk_api_book_id` FOREIGN KEY (`book_id`) REFERENCES `api_book` (`id`),
  CONSTRAINT `api_book_pub_publisher_id_3e5d98df_fk_api_publisher_id` FOREIGN KEY (`publisher_id`) REFERENCES `api_publisher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_book_pub` */

/*Table structure for table `api_cn_en_map` */

DROP TABLE IF EXISTS `api_cn_en_map`;

CREATE TABLE `api_cn_en_map` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent` varchar(64) NOT NULL,
  `cn_name` varchar(128) NOT NULL,
  `children` varchar(320) DEFAULT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `parent` (`parent`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_cn_en_map` */

insert  into `api_cn_en_map`(`id`,`parent`,`cn_name`,`children`,`statue`,`create_time`,`update_time`) values 
(1,'username','用户名','userNm;User;USERNAME;Username',1,'2021-05-30 10:08:13.774191','2021-05-30 10:08:38.150645');

/*Table structure for table `api_publisher` */

DROP TABLE IF EXISTS `api_publisher`;

CREATE TABLE `api_publisher` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_publisher` */

/*Table structure for table `api_rollingpic` */

DROP TABLE IF EXISTS `api_rollingpic`;

CREATE TABLE `api_rollingpic` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pictureName` varchar(32) NOT NULL,
  `path` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_rollingpic` */

/*Table structure for table `api_scenario` */

DROP TABLE IF EXISTS `api_scenario`;

CREATE TABLE `api_scenario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scenario` varchar(64) NOT NULL,
  `parameter` longtext NOT NULL,
  `validator` varchar(100) NOT NULL,
  `priority` smallint NOT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `test_case_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `scenario` (`scenario`),
  KEY `api_scenario_test_case_id_286bbcd4_fk_api_testcase_id` (`test_case_id`),
  CONSTRAINT `api_scenario_test_case_id_286bbcd4_fk_api_testcase_id` FOREIGN KEY (`test_case_id`) REFERENCES `api_testcase` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_scenario` */

insert  into `api_scenario`(`id`,`scenario`,`parameter`,`validator`,`priority`,`statue`,`create_time`,`update_time`,`test_case_id`) values 
(2,'用户名正确-密码正确','撒打算','200',0,1,'2021-05-29 17:31:50.216576','2021-05-29 17:31:50.216576',2),
(3,'用户密码均正确','阿萨德ad','200',0,1,'2021-05-29 17:41:47.440720','2021-05-29 17:41:47.440720',3),
(4,'用户密码均错误','打的打的','200',0,1,'2021-05-29 17:42:08.409007','2021-05-29 17:42:08.409007',2),
(5,'T+1-限价订单-全额清算','大神','200',0,1,'2021-05-29 17:43:27.569618','2021-05-29 17:43:27.569618',4);

/*Table structure for table `api_templates` */

DROP TABLE IF EXISTS `api_templates`;

CREATE TABLE `api_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `url` varchar(128) NOT NULL,
  `method` smallint NOT NULL,
  `header` varchar(640) DEFAULT NULL,
  `data` longtext NOT NULL,
  `process_name` varchar(32) DEFAULT NULL,
  `linux_order_str` varchar(100) DEFAULT NULL,
  `table_name` varchar(32) DEFAULT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_templates` */

insert  into `api_templates`(`id`,`name`,`url`,`method`,`header`,`data`,`process_name`,`linux_order_str`,`table_name`,`statue`,`create_time`,`update_time`) values 
(1,'现券XBOND订单提交','https://www.cnblogs.com/aaronthon/ajax/GetPostStat',1,'{\"content-type\": \"application/json\", \"Authorization\":\"9480295ab2e2eddb8\"}','武切维奇','tbs-dp-css','grep \'%s\' /home/tbs/app/tbs-dp-css/logs/css-debug.log','tbs_ordr_dtl',1,'2021-05-17 11:24:42.981697','2021-05-21 11:29:00.577169'),
(2,'用户登录','https://www.cnblogs.com/aaronthon/ajax/GetPostStat',1,'{\"content-type\": \"application/json\", \"Authorization\":\"9480295ab2e2eddb8\"}','打撒所多','大','大','tbs_ordr_dtl',1,'2021-05-24 09:09:15.292419','2021-05-24 09:09:15.292419'),
(3,'用户注册','https://www.cnblogs.com/aaronthon/ajax/GetPostStat',1,'{\"content-type\": \"application/json\", \"Authorization\":\"7777777779480295ab2e2eddb8\"}','企鹅窝群','tbs-dp-css','grep \'%s\' /home/tbs/app/tbs-dp-css/logs/css-debug.log','tbs_ordr_dtl',1,'2021-05-24 09:09:40.112405','2021-05-24 09:09:40.112405'),
(4,'UUMS登录','https://www.cnblogs.com/aaronthon/ajax/GetPostStat',1,'{\"content-type\": \"application/json\", \"Authorization\":\"9480295ab2e2eddb8\"}','sad撒多','tbs-dp-css','grep \'%s\' /home/tbs/app/tbs-dp-css/logs/css-debug.log','tbs_ordr_dtl',1,'2021-05-24 09:15:07.993162','2021-05-24 09:15:07.993162'),
(5,'KMS登录','https://www.cnblogs.com/aaronthon/ajax/GetPostStat',1,'{\"content-type\": \"application/json\", \"Authorization\":\"9480295ab2e2eddb8\"}','阿萨德','tbs-dp-css','grep \'%s\' /home/tbs/app/tbs-dp-css/logs/css-debug.log','tbs_ordr_dtl',1,'2021-05-24 09:15:31.850581','2021-05-29 17:39:28.160543');

/*Table structure for table `api_testcase` */

DROP TABLE IF EXISTS `api_testcase`;

CREATE TABLE `api_testcase` (
  `id` int NOT NULL AUTO_INCREMENT,
  `case` varchar(64) NOT NULL,
  `case_title` varchar(100) NOT NULL,
  `case_description` varchar(320) DEFAULT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `templates_id` int NOT NULL,
  `test_suit_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `case` (`case`),
  UNIQUE KEY `templates_id` (`templates_id`),
  KEY `api_testcase_test_suit_id_126ce3c7_fk_api_testsuit_id` (`test_suit_id`),
  CONSTRAINT `api_testcase_templates_id_ad9ca6fa_fk_api_templates_id` FOREIGN KEY (`templates_id`) REFERENCES `api_templates` (`id`),
  CONSTRAINT `api_testcase_test_suit_id_126ce3c7_fk_api_testsuit_id` FOREIGN KEY (`test_suit_id`) REFERENCES `api_testsuit` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_testcase` */

insert  into `api_testcase`(`id`,`case`,`case_title`,`case_description`,`statue`,`create_time`,`update_time`,`templates_id`,`test_suit_id`) values 
(2,'kms_login','KMS登录','KMS登录',1,'2021-05-29 17:09:35.801091','2021-05-29 17:09:35.801091',5,5),
(3,'uums_login','UUMS登录','UUMS登录',1,'2021-05-29 17:10:19.951481','2021-05-29 17:10:19.951481',4,4),
(4,'xbond_cbt','XBOND订单提交','XBOND订单提交',1,'2021-05-29 17:11:04.651030','2021-05-29 17:11:04.651030',1,4);

/*Table structure for table `api_testsuit` */

DROP TABLE IF EXISTS `api_testsuit`;

CREATE TABLE `api_testsuit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `module` varchar(64) NOT NULL,
  `class_title` varchar(32) DEFAULT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `module` (`module`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_testsuit` */

insert  into `api_testsuit`(`id`,`module`,`class_title`,`statue`,`create_time`,`update_time`) values 
(4,'LoginSuit','登录用例集合',1,'2021-05-29 17:03:57.653036','2021-05-29 17:03:57.653036'),
(5,'KmsAuth','KMS认证',1,'2021-05-29 17:05:20.346390','2021-05-29 17:05:20.346390'),
(6,'XBOND','XBOND交易系统',1,'2021-05-29 17:11:45.842055','2021-05-29 17:11:45.842055');

/*Table structure for table `api_testsuit_project` */

DROP TABLE IF EXISTS `api_testsuit_project`;

CREATE TABLE `api_testsuit_project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `testsuit_id` int NOT NULL,
  `apiproject_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_testsuit_project_testsuit_id_apiproject_id_f5328aa9_uniq` (`testsuit_id`,`apiproject_id`),
  KEY `api_testsuit_project_apiproject_id_8e5bdd3c_fk_api_apiproject_id` (`apiproject_id`),
  CONSTRAINT `api_testsuit_project_apiproject_id_8e5bdd3c_fk_api_apiproject_id` FOREIGN KEY (`apiproject_id`) REFERENCES `api_apiproject` (`id`),
  CONSTRAINT `api_testsuit_project_testsuit_id_0131050d_fk_api_testsuit_id` FOREIGN KEY (`testsuit_id`) REFERENCES `api_testsuit` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_testsuit_project` */

insert  into `api_testsuit_project`(`id`,`testsuit_id`,`apiproject_id`) values 
(1,4,4),
(2,5,4),
(3,6,5);

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group` */

insert  into `auth_group`(`id`,`name`) values 
(3,'全表只读权限'),
(1,'全表的增删改查'),
(4,'全表的增改查'),
(2,'管理员');

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add content type',4,'add_contenttype'),
(14,'Can change content type',4,'change_contenttype'),
(15,'Can delete content type',4,'delete_contenttype'),
(16,'Can view content type',4,'view_contenttype'),
(17,'Can add session',5,'add_session'),
(18,'Can change session',5,'change_session'),
(19,'Can delete session',5,'delete_session'),
(20,'Can view session',5,'view_session'),
(21,'Can add api project',6,'add_apiproject'),
(22,'Can change api project',6,'change_apiproject'),
(23,'Can delete api project',6,'delete_apiproject'),
(24,'Can view api project',6,'view_apiproject'),
(25,'Can add c n_e n_map',7,'add_cn_en_map'),
(26,'Can change c n_e n_map',7,'change_cn_en_map'),
(27,'Can delete c n_e n_map',7,'delete_cn_en_map'),
(28,'Can view c n_e n_map',7,'view_cn_en_map'),
(29,'Can add publisher',8,'add_publisher'),
(30,'Can change publisher',8,'change_publisher'),
(31,'Can delete publisher',8,'delete_publisher'),
(32,'Can view publisher',8,'view_publisher'),
(33,'Can add rolling pic',9,'add_rollingpic'),
(34,'Can change rolling pic',9,'change_rollingpic'),
(35,'Can delete rolling pic',9,'delete_rollingpic'),
(36,'Can view rolling pic',9,'view_rollingpic'),
(37,'Can add templates',10,'add_templates'),
(38,'Can change templates',10,'change_templates'),
(39,'Can delete templates',10,'delete_templates'),
(40,'Can view templates',10,'view_templates'),
(41,'Can add test suit',11,'add_testsuit'),
(42,'Can change test suit',11,'change_testsuit'),
(43,'Can delete test suit',11,'delete_testsuit'),
(44,'Can view test suit',11,'view_testsuit'),
(45,'Can add test case',12,'add_testcase'),
(46,'Can change test case',12,'change_testcase'),
(47,'Can delete test case',12,'delete_testcase'),
(48,'Can view test case',12,'view_testcase'),
(49,'Can add scenario',13,'add_scenario'),
(50,'Can change scenario',13,'change_scenario'),
(51,'Can delete scenario',13,'delete_scenario'),
(52,'Can view scenario',13,'view_scenario'),
(53,'Can add book',14,'add_book'),
(54,'Can change book',14,'change_book'),
(55,'Can delete book',14,'delete_book'),
(56,'Can view book',14,'view_book'),
(57,'Can add business func',15,'add_businessfunc'),
(58,'Can change business func',15,'change_businessfunc'),
(59,'Can delete business func',15,'delete_businessfunc'),
(60,'Can view business func',15,'view_businessfunc'),
(61,'Can add first layer menu',16,'add_firstlayermenu'),
(62,'Can change first layer menu',16,'change_firstlayermenu'),
(63,'Can delete first layer menu',16,'delete_firstlayermenu'),
(64,'Can view first layer menu',16,'view_firstlayermenu'),
(65,'Can add groups',17,'add_groups'),
(66,'Can change groups',17,'change_groups'),
(67,'Can delete groups',17,'delete_groups'),
(68,'Can view groups',17,'view_groups'),
(69,'Can add icon',18,'add_icon'),
(70,'Can change icon',18,'change_icon'),
(71,'Can delete icon',18,'delete_icon'),
(72,'Can view icon',18,'view_icon'),
(73,'Can add retrieval',19,'add_retrieval'),
(74,'Can change retrieval',19,'change_retrieval'),
(75,'Can delete retrieval',19,'delete_retrieval'),
(76,'Can view retrieval',19,'view_retrieval'),
(77,'Can add sub menu',20,'add_submenu'),
(78,'Can change sub menu',20,'change_submenu'),
(79,'Can delete sub menu',20,'delete_submenu'),
(80,'Can view sub menu',20,'view_submenu'),
(81,'Can add role',21,'add_role'),
(82,'Can change role',21,'change_role'),
(83,'Can delete role',21,'delete_role'),
(84,'Can view role',21,'view_role'),
(85,'Can add user profile',22,'add_userprofile'),
(86,'Can change user profile',22,'change_userprofile'),
(87,'Can delete user profile',22,'delete_userprofile'),
(88,'Can view user profile',22,'view_userprofile'),
(89,'可以允许访问表中数据',22,'web_table_data'),
(90,'可以批量操作表中数据',22,'web_table_data_batch_operation'),
(91,'可以允许访问修改页',22,'web_table_update_view'),
(92,'可以允许更新数据',22,'web_table_update'),
(93,'可以允许新增数据',22,'web_table_add'),
(94,'可以允许访问新增数据页面',22,'web_table_add_view'),
(95,'可以允许删除数据',22,'web_table_delete'),
(96,'可以允许访问删除数据页面',22,'web_table_delete_view');

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_public_userprofile_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_public_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `public_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(6,'api','apiproject'),
(14,'api','book'),
(7,'api','cn_en_map'),
(8,'api','publisher'),
(9,'api','rollingpic'),
(13,'api','scenario'),
(10,'api','templates'),
(12,'api','testcase'),
(11,'api','testsuit'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'contenttypes','contenttype'),
(15,'public','businessfunc'),
(16,'public','firstlayermenu'),
(17,'public','groups'),
(18,'public','icon'),
(19,'public','retrieval'),
(21,'public','role'),
(20,'public','submenu'),
(22,'public','userprofile'),
(5,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2021-05-28 22:27:36.831177'),
(2,'contenttypes','0002_remove_content_type_name','2021-05-28 22:27:36.883224'),
(3,'auth','0001_initial','2021-05-28 22:27:36.945280'),
(4,'auth','0002_alter_permission_name_max_length','2021-05-28 22:27:37.083406'),
(5,'auth','0003_alter_user_email_max_length','2021-05-28 22:27:37.090412'),
(6,'auth','0004_alter_user_username_opts','2021-05-28 22:27:37.095417'),
(7,'auth','0005_alter_user_last_login_null','2021-05-28 22:27:37.101422'),
(8,'auth','0006_require_contenttypes_0002','2021-05-28 22:27:37.104426'),
(9,'auth','0007_alter_validators_add_error_messages','2021-05-28 22:27:37.111435'),
(10,'auth','0008_alter_user_username_max_length','2021-05-28 22:27:37.118438'),
(11,'auth','0009_alter_user_last_name_max_length','2021-05-28 22:27:37.124443'),
(12,'auth','0010_alter_group_name_max_length','2021-05-28 22:27:37.137456'),
(13,'auth','0011_update_proxy_permissions','2021-05-28 22:27:37.143461'),
(14,'public','0001_initial','2021-05-28 22:27:37.362661'),
(15,'admin','0001_initial','2021-05-28 22:27:37.760022'),
(16,'admin','0002_logentry_remove_auto_add','2021-05-28 22:27:37.832087'),
(17,'admin','0003_logentry_add_action_flag_choices','2021-05-28 22:27:37.841095'),
(18,'api','0001_initial','2021-05-28 22:27:38.046282'),
(19,'sessions','0001_initial','2021-05-28 22:27:38.292507'),
(20,'api','0002_auto_20210529_1740','2021-05-29 17:40:13.415918');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('qvfmsaxe417geh0yp3oz7swzjgyj366g','OTZhNDI2OWU4OTJjM2VjMjFlYzVhZjA1ZTRkOGRjZjFhOTNhMWI5NDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjMjNiYWFmMzBkMzY1OWM2ZTRmNjA4MjZjYzg4NDdjNjRjNDNjZGZiIn0=','2021-06-11 22:30:32.375076');

/*Table structure for table `public_businessfunc` */

DROP TABLE IF EXISTS `public_businessfunc`;

CREATE TABLE `public_businessfunc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `expression` varchar(64) NOT NULL,
  `parameter` varchar(128) DEFAULT NULL,
  `return_type` varchar(120) DEFAULT NULL,
  `description` varchar(128) NOT NULL,
  `type` smallint NOT NULL,
  `statue` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_businessfunc` */

insert  into `public_businessfunc`(`id`,`name`,`expression`,`parameter`,`return_type`,`description`,`type`,`statue`) values 
(1,'获取当前时间','get_current_time',NULL,'返回时间字符串','获取当前日期',2,1),
(2,'获取数据库','db_connect','host|port|database_name|username|password','无','获取链接数据库',1,1);

/*Table structure for table `public_firstlayermenu` */

DROP TABLE IF EXISTS `public_firstlayermenu`;

CREATE TABLE `public_firstlayermenu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` smallint NOT NULL,
  `name` varchar(64) NOT NULL,
  `icon` varchar(64) NOT NULL,
  `url_type` smallint NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `order` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_firstlayermenu` */

insert  into `public_firstlayermenu`(`id`,`type`,`name`,`icon`,`url_type`,`url_name`,`order`) values 
(1,2,'公共设置','glyphicon glyphicon-th',0,'public_overview',1),
(2,1,'网页应用概览','glyphicon glyphicon-th',0,'api_overview',1),
(3,0,'接口应用清单','glyphicon glyphicon-th',0,'api_overview',1),
(4,0,'报告查询','glyphicon glyphicon-list-alt',0,'api_report',2),
(5,0,'数据分析','glyphicon glyphicon-education',0,'api_analytics',3),
(6,0,'数据导出','glyphicon glyphicon-folder-open',0,'api_export',4),
(8,2,'定时任务','glyphicon glyphicon-blackboard',0,'public_task',1),
(9,2,'测试页面','glyphicon glyphicon-blackboard',0,'public_test',0);

/*Table structure for table `public_firstlayermenu_sub_menus` */

DROP TABLE IF EXISTS `public_firstlayermenu_sub_menus`;

CREATE TABLE `public_firstlayermenu_sub_menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstlayermenu_id` int NOT NULL,
  `submenu_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_firstlayermenu_su_firstlayermenu_id_submen_54a5a19f_uniq` (`firstlayermenu_id`,`submenu_id`),
  KEY `public_firstlayermen_submenu_id_750cd141_fk_public_su` (`submenu_id`),
  CONSTRAINT `public_firstlayermen_firstlayermenu_id_940240d0_fk_public_fi` FOREIGN KEY (`firstlayermenu_id`) REFERENCES `public_firstlayermenu` (`id`),
  CONSTRAINT `public_firstlayermen_submenu_id_750cd141_fk_public_su` FOREIGN KEY (`submenu_id`) REFERENCES `public_submenu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_firstlayermenu_sub_menus` */

/*Table structure for table `public_groups` */

DROP TABLE IF EXISTS `public_groups`;

CREATE TABLE `public_groups` (
  `group_ptr_id` int NOT NULL,
  `description` varchar(320) DEFAULT NULL,
  PRIMARY KEY (`group_ptr_id`),
  CONSTRAINT `public_groups_group_ptr_id_4d480540_fk_auth_group_id` FOREIGN KEY (`group_ptr_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_groups` */

/*Table structure for table `public_icon` */

DROP TABLE IF EXISTS `public_icon`;

CREATE TABLE `public_icon` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `link` varchar(64) DEFAULT NULL,
  `upload` varchar(100) DEFAULT NULL,
  `type` smallint NOT NULL,
  `color` smallint NOT NULL,
  `remark` varchar(640) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_icon` */

insert  into `public_icon`(`id`,`name`,`link`,`upload`,`type`,`color`,`remark`) values 
(22,'用户管理','/public/userprofile/','static/picture/icon/用户管理_rU9XS19.svg',2,5,NULL),
(23,'权限管理','/public/groups','static/picture/icon/权限管理_uaeXYtp.svg',2,3,NULL),
(24,'角色管理','/public/role/','static/picture/icon/角色管理_sw17X9V.svg',2,5,NULL),
(25,'一级菜单管理','/public/firstlayermenu/','static/picture/icon/一级菜单管理_ghPUYch.svg',2,2,NULL),
(26,'二级菜单管理','/public/submenu/','static/picture/icon/二级菜单管理_y0fptYI.svg',2,1,NULL),
(27,'全局检索','/public/retrieval/','static/picture/icon/全文检索_WpU2ID6.svg',2,1,NULL),
(28,'业务函数','/public/businessfunc/','static/picture/icon/业务管理_q1d1ojN.svg',2,4,NULL),
(29,'菜单ICON管理','/public/icon/','static/picture/icon/科组部门管理.svg',2,1,NULL),
(30,'项目管理','/api/apiproject/','static/picture/icon/空白带领用核算统计_1_t20awjJ.svg',0,1,NULL),
(31,'模板管理','/api/templates/','static/picture/icon/备播带借还.svg',0,3,NULL),
(32,'用例集管理','/api/testsuit/','static/picture/icon/光盘库管理.svg',0,4,NULL),
(33,'函数管理','/api/testcase/','static/picture/icon/空白介质入库.svg',0,5,NULL),
(34,'场景管理','/api/scenario/','static/picture/icon/母版统计_3.svg',0,1,NULL),
(35,'字段映射','/api/cn_en_map/','static/picture/icon/日记管理.svg',0,1,NULL),
(36,'书籍','/api/book/','static/picture/icon/节目分流_1.svg',0,1,NULL),
(37,'出版社','/api/publisher/','static/picture/icon/体育库管理.svg',0,1,NULL);

/*Table structure for table `public_retrieval` */

DROP TABLE IF EXISTS `public_retrieval`;

CREATE TABLE `public_retrieval` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `link` varchar(64) DEFAULT NULL,
  `statue` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_retrieval` */

insert  into `public_retrieval`(`id`,`name`,`link`,`statue`) values 
(1,'用户登录','/login',1),
(2,'WEB菜单','/menus',1),
(3,'API菜单','/menus',1),
(4,'API项目管理','/api/apiproject/',1),
(7,'API接口模板','/api/templates/',1);

/*Table structure for table `public_role` */

DROP TABLE IF EXISTS `public_role`;

CREATE TABLE `public_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rolename` varchar(64) NOT NULL,
  `statue` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rolename` (`rolename`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_role` */

insert  into `public_role`(`id`,`rolename`,`statue`,`create_time`,`update_time`) values 
(1,'领导',1,'2021-05-17 10:00:09.000000','2021-05-26 15:50:56.953646');

/*Table structure for table `public_role_menus` */

DROP TABLE IF EXISTS `public_role_menus`;

CREATE TABLE `public_role_menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `firstlayermenu_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_role_menus_role_id_firstlayermenu_id_dc3afe7a_uniq` (`role_id`,`firstlayermenu_id`),
  KEY `public_role_menus_firstlayermenu_id_24f3ae52_fk_public_fi` (`firstlayermenu_id`),
  CONSTRAINT `public_role_menus_firstlayermenu_id_24f3ae52_fk_public_fi` FOREIGN KEY (`firstlayermenu_id`) REFERENCES `public_firstlayermenu` (`id`),
  CONSTRAINT `public_role_menus_role_id_d7ee9a82_fk_public_role_id` FOREIGN KEY (`role_id`) REFERENCES `public_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_role_menus` */

insert  into `public_role_menus`(`id`,`role_id`,`firstlayermenu_id`) values 
(1,1,1),
(2,1,2),
(3,1,3),
(4,1,4),
(5,1,5),
(6,1,6),
(7,1,8),
(8,1,9);

/*Table structure for table `public_submenu` */

DROP TABLE IF EXISTS `public_submenu`;

CREATE TABLE `public_submenu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` smallint NOT NULL,
  `name` varchar(64) NOT NULL,
  `url_type` smallint NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `order` smallint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_submenu` */

/*Table structure for table `public_userprofile` */

DROP TABLE IF EXISTS `public_userprofile`;

CREATE TABLE `public_userprofile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_superuser` smallint NOT NULL,
  `username` varchar(32) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `is_active` smallint NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_userprofile` */

insert  into `public_userprofile`(`id`,`last_login`,`email`,`password`,`is_superuser`,`username`,`name`,`is_active`,`create_time`,`update_time`) values 
(1,'2021-05-28 22:30:32.365066','root@qq.com','pbkdf2_sha256$150000$hrup6s6pwtrX$lwj2YfLpEjDrfEPESi2exbTKLm2PEDNFfZqQXgSNj20=',1,'root',NULL,1,'2021-05-28 22:28:10.340112','2021-05-28 22:28:10.344116');

/*Table structure for table `public_userprofile_groups` */

DROP TABLE IF EXISTS `public_userprofile_groups`;

CREATE TABLE `public_userprofile_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userprofile_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_userprofile_groups_userprofile_id_group_id_293c6761_uniq` (`userprofile_id`,`group_id`),
  KEY `public_userprofile_groups_group_id_a179d59b_fk_auth_group_id` (`group_id`),
  CONSTRAINT `public_userprofile_g_userprofile_id_35dac251_fk_public_us` FOREIGN KEY (`userprofile_id`) REFERENCES `public_userprofile` (`id`),
  CONSTRAINT `public_userprofile_groups_group_id_a179d59b_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_userprofile_groups` */

/*Table structure for table `public_userprofile_role` */

DROP TABLE IF EXISTS `public_userprofile_role`;

CREATE TABLE `public_userprofile_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userprofile_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_userprofile_role_userprofile_id_role_id_dea9eb81_uniq` (`userprofile_id`,`role_id`),
  KEY `public_userprofile_role_role_id_683ee805_fk_public_role_id` (`role_id`),
  CONSTRAINT `public_userprofile_r_userprofile_id_3e094904_fk_public_us` FOREIGN KEY (`userprofile_id`) REFERENCES `public_userprofile` (`id`),
  CONSTRAINT `public_userprofile_role_role_id_683ee805_fk_public_role_id` FOREIGN KEY (`role_id`) REFERENCES `public_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_userprofile_role` */

insert  into `public_userprofile_role`(`id`,`userprofile_id`,`role_id`) values 
(3,1,1);

/*Table structure for table `public_userprofile_user_permissions` */

DROP TABLE IF EXISTS `public_userprofile_user_permissions`;

CREATE TABLE `public_userprofile_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userprofile_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `public_userprofile_user__userprofile_id_permissio_b2f9aa89_uniq` (`userprofile_id`,`permission_id`),
  KEY `public_userprofile_u_permission_id_39b1f2c3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `public_userprofile_u_permission_id_39b1f2c3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `public_userprofile_u_userprofile_id_faaf091c_fk_public_us` FOREIGN KEY (`userprofile_id`) REFERENCES `public_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `public_userprofile_user_permissions` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
