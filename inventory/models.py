from django.db import models
from resources.models import BizMachine, BizProduct
from users.models import AppUser, SysStaff


class BizInventory(models.Model):
    """库存表 - 核心表，触发器监控对象"""
    machine = models.ForeignKey(
        BizMachine,
        on_delete=models.CASCADE,
        verbose_name='机器',
        related_name='inventories'
    )
    product = models.ForeignKey(
        BizProduct,
        on_delete=models.CASCADE,
        verbose_name='商品',
        related_name='inventories'
    )
    current_stock = models.IntegerField('当前库存', default=0)
    max_capacity = models.IntegerField('最大容量', default=20)

    class Meta:
        db_table = 'biz_inventory'
        verbose_name = '库存'
        verbose_name_plural = verbose_name
        unique_together = ['machine', 'product']  # 联合唯一索引

    def __str__(self):
        return f'{self.machine.machine_code} - {self.product.name}: {self.current_stock}'


class LogTransaction(models.Model):
    """交易流水"""
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        verbose_name='用户',
        related_name='transactions'
    )
    machine = models.ForeignKey(
        BizMachine,
        on_delete=models.CASCADE,
        verbose_name='机器',
        related_name='transactions'
    )
    product = models.ForeignKey(
        BizProduct,
        on_delete=models.CASCADE,
        verbose_name='商品',
        related_name='transactions'
    )
    amount = models.DecimalField('成交金额', max_digits=10, decimal_places=2)
    cost_price = models.DecimalField('成本价', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('交易时间', auto_now_add=True)

    @property
    def profit(self):
        """计算单笔交易利润"""
        return self.amount - self.cost_price

    class Meta:
        db_table = 'log_transaction'
        verbose_name = '交易流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.amount}'


class LogRestock(models.Model):
    """补货记录"""
    staff = models.ForeignKey(
        SysStaff,
        on_delete=models.CASCADE,
        verbose_name='运维人员',
        related_name='restocks'
    )
    machine = models.ForeignKey(
        BizMachine,
        on_delete=models.CASCADE,
        verbose_name='机器',
        related_name='restocks'
    )
    product = models.ForeignKey(
        BizProduct,
        on_delete=models.CASCADE,
        verbose_name='商品',
        related_name='restocks'
    )
    quantity = models.IntegerField('补货数量')
    unit_cost = models.DecimalField('单位成本', max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField('总成本', max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField('补货时间', auto_now_add=True)

    class Meta:
        db_table = 'log_restock'
        verbose_name = '补货记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.staff.name} - {self.machine.machine_code} - {self.product.name}'
