# Generated by Django 3.2 on 2021-07-22 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_alter_userprofile_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('web_table_data', '可以允许访问表中数据'), ('web_table_data_batch_operation', '可以批量操作表中数据'), ('web_table_update_view', '可以允许访问修改页'), ('web_table_update', '可以允许更新数据'), ('web_table_add', '可以允许新增数据'), ('web_table_add_view', '可以允许访问新增数据页面'), ('web_table_delete', '可以允许删除数据'), ('web_table_delete_view', '可以允许访问删除数据页面'), ('password_reset_get', '可以允许访问修改密码页面'), ('password_reset_post', '可以允许访修改密码')), 'verbose_name_plural': '用户信息表'},
        ),
    ]
