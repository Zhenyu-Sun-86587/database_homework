from django.db import models


class BizSupplier(models.Model):
    """供应商"""
    name = models.CharField('名称', max_length=100)
    contact = models.CharField('联系方式', max_length=100)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'biz_supplier'
        verbose_name = '供应商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BizMachine(models.Model):
    """贩卖机"""
    STATUS_CHOICES = [
        ('normal', '正常'),
        ('fault', '故障'),
    ]

    machine_code = models.CharField('机器编号', max_length=50, unique=True)
    location = models.CharField('位置', max_length=200)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='normal')
    region_code = models.CharField('所属区域', max_length=20)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'biz_machine'
        verbose_name = '贩卖机'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.machine_code} - {self.location}'


class BizProduct(models.Model):
    """商品"""
    name = models.CharField('名称', max_length=100)
    cost_price = models.DecimalField('进价', max_digits=10, decimal_places=2)
    sell_price = models.DecimalField('售价', max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(
        BizSupplier,
        on_delete=models.CASCADE,
        verbose_name='供应商',
        related_name='products'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'biz_product'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
