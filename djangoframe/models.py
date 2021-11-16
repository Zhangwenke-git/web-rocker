from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=32,verbose_name="人员姓名")
    sex_choice = (
        (1,"男性"),
        (0,"女性"),
        (2,"未知"),
    )
    sex = models.SmallIntegerField(choices=sex_choice,verbose_name="性别")
    statue_choice = (
        (1,"在职"),
        (0,"离职"),
    )
    statue = models.SmallIntegerField(choices=statue_choice,verbose_name="在职状态")
    department = models.CharField(max_length=32, verbose_name="部门")
    position = models.CharField(max_length=32, verbose_name="职务")
    telephone = models.CharField(max_length=11, verbose_name="联系方式")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    class Meta:
        verbose_name_plural = '人员信息'
    def __str__(self):
        return "%s-%s" % (self.name,id)


