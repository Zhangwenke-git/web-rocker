# Generated by Django 3.2 on 2021-09-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210903_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='parameter',
            field=models.JSONField(verbose_name='请求参数'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='validator',
            field=models.JSONField(verbose_name='验证字段'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='data',
            field=models.JSONField(help_text='\n    \n    <div class="alert border-0 border-start border-5 border-primary alert-dismissible fade show py-2">\n        <div class="d-flex align-items-center">\n            <div class="font-35 text-primary"><i class=\'bx bx-bookmark-heart\'></i>\n            </div>\n            <div class="ms-3">\n                <h6 class="mb-0 text-primary">提醒</h6>\n                <div>\n                ① 常规变量使用{{}}标识，例如：{{username}} <br>② 调用其他函数，则使用${function}|<>形式标识 <br>③ 需传参的函数，则使用${login}|<{{username}},{{password}}>标识 </span>\n                </div>\n            </div>\n        </div>\n        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\n    </div>\n    \n    ', null=True, verbose_name='请求模板'),
        ),
        migrations.AlterField(
            model_name='templates',
            name='header',
            field=models.JSONField(default="{'Content-Type':'application/json'}", null=True, verbose_name='header'),
        ),
    ]
