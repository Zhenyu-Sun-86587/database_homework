from django.db import models
from resources.models import BizMachine


class LogAlert(models.Model):
    """报警日志 - 系统自动生成（由数据库触发器写入）"""
    ALERT_TYPE_CHOICES = [
        ('low_stock', '缺货'),
        ('fault', '故障'),
    ]

    machine = models.ForeignKey(
        BizMachine,
        on_delete=models.CASCADE,
        verbose_name='机器',
        related_name='alerts'
    )
    alert_type = models.CharField('类型', max_length=20, choices=ALERT_TYPE_CHOICES, default='low_stock')
    message = models.CharField('报警内容', max_length=500)
    created_at = models.DateTimeField('报警时间', auto_now_add=True)

    class Meta:
        db_table = 'log_alert'
        verbose_name = '报警日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.machine.machine_code} - {self.alert_type} - {self.message}'


class StatDaily(models.Model):
    """日结统计"""
    date = models.DateField('日期')
    machine = models.ForeignKey(
        BizMachine,
        on_delete=models.CASCADE,
        verbose_name='机器',
        related_name='daily_stats'
    )
    total_revenue = models.DecimalField('总营收', max_digits=12, decimal_places=2, default=0)
    order_count = models.IntegerField('订单数', default=0)
    alert_count = models.IntegerField('报警次数', default=0)

    class Meta:
        db_table = 'stat_daily'
        verbose_name = '日结统计'
        verbose_name_plural = verbose_name
        unique_together = ['date', 'machine']

    def __str__(self):
        return f'{self.date} - {self.machine.machine_code}'
