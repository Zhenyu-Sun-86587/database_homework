from django.db import models


class SysAdmin(models.Model):
    """系统管理员"""
    username = models.CharField('用户名', max_length=50, unique=True)
    password = models.CharField('密码', max_length=128)
    permission = models.CharField('权限', max_length=20, default='admin')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'sys_admin'
        verbose_name = '管理员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class SysStaff(models.Model):
    """运维人员"""
    staff_id = models.CharField('工号', max_length=20, unique=True)
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('电话', max_length=20)
    region_code = models.CharField('负责区域', max_length=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'sys_staff'
        verbose_name = '运维人员'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.staff_id} - {self.name}'


class AppUser(models.Model):
    """学生用户"""
    username = models.CharField('用户名', max_length=50, unique=True)
    balance = models.DecimalField('余额', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'app_user'
        verbose_name = '学生用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
