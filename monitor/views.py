from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from .models import LogAlert, StatDaily
from .serializers import LogAlertSerializer, StatDailySerializer
from resources.models import BizMachine
from inventory.models import LogTransaction


class LogAlertViewSet(viewsets.ModelViewSet):
    queryset = LogAlert.objects.all().order_by('-created_at')
    serializer_class = LogAlertSerializer


class StatDailyViewSet(viewsets.ModelViewSet):
    queryset = StatDaily.objects.all().order_by('-date')
    serializer_class = StatDailySerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        生成指定日期的日结统计
        POST /api/stat-daily/generate/
        Body: {"date": "2025-12-15"} (可选，默认为今天)
        """
        date_str = request.data.get('date')
        if date_str:
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "日期格式错误，应为 YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            target_date = timezone.now().date()
        
        # 使用时间范围查询而非 __date
        start_dt = timezone.make_aware(datetime.combine(target_date, datetime.min.time()))
        end_dt = start_dt + timedelta(days=1)
        
        transactions = LogTransaction.objects.filter(created_at__gte=start_dt, created_at__lt=end_dt)
        
        machines = BizMachine.objects.all()
        created_count = 0
        
        for machine in machines:
            machine_trans = transactions.filter(machine=machine)
            machine_alerts = LogAlert.objects.filter(machine=machine, created_at__gte=start_dt, created_at__lt=end_dt)
            
            total_revenue = machine_trans.aggregate(Sum('amount'))['amount__sum'] or 0
            total_cost = machine_trans.aggregate(Sum('cost_price'))['cost_price__sum'] or 0
            total_profit = float(total_revenue) - float(total_cost)
            order_count = machine_trans.count()
            alert_count = machine_alerts.count()
            
            stat, created = StatDaily.objects.update_or_create(
                date=target_date,
                machine=machine,
                defaults={
                    'total_revenue': total_revenue,
                    'total_cost': total_cost,
                    'total_profit': total_profit,
                    'order_count': order_count,
                    'alert_count': alert_count
                }
            )
            if created:
                created_count += 1
        
        return Response({
            "message": f"已生成 {target_date} 的日结统计",
            "machines_processed": machines.count(),
            "new_records": created_count
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        获取财务汇总统计 - 实时从交易记录计算
        GET /api/stat-daily/summary/?period=week|month|today|all
        """
        period = request.query_params.get('period', 'week')
        now = timezone.now()
        
        if period == 'today':
            # 今天开始时间（本地时区）
            start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_dt = now - timedelta(days=7)
        elif period == 'month':
            start_dt = now - timedelta(days=30)
        elif period == 'all':
            start_dt = None  # 所有数据
        else:
            start_dt = now - timedelta(days=7)
        
        # 直接从交易记录实时计算
        if start_dt:
            transactions = LogTransaction.objects.filter(created_at__gte=start_dt)
            alerts = LogAlert.objects.filter(created_at__gte=start_dt)
        else:
            transactions = LogTransaction.objects.all()
            alerts = LogAlert.objects.all()
        
        # 汇总
        total_revenue = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        total_cost = transactions.aggregate(Sum('cost_price'))['cost_price__sum'] or 0
        total_profit = float(total_revenue) - float(total_cost)
        total_orders = transactions.count()
        total_alerts = alerts.count()
        
        # 按日期分组
        daily = transactions.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            revenue=Sum('amount'),
            cost=Sum('cost_price'),
            orders=Count('id')
        ).order_by('date')
        
        daily_list = []
        for d in daily:
            daily_list.append({
                'date': str(d['date']) if d['date'] else '',
                'revenue': float(d['revenue'] or 0),
                'cost': float(d['cost'] or 0),
                'profit': float(d['revenue'] or 0) - float(d['cost'] or 0),
                'orders': d['orders']
            })
        
        # 按机器分组
        by_machine = transactions.values('machine__machine_code').annotate(
            revenue=Sum('amount'),
            cost=Sum('cost_price'),
            orders=Count('id')
        ).order_by('-revenue')[:10]
        
        machine_list = []
        for m in by_machine:
            machine_list.append({
                'machine__machine_code': m['machine__machine_code'],
                'revenue': float(m['revenue'] or 0),
                'profit': float(m['revenue'] or 0) - float(m['cost'] or 0),
                'orders': m['orders']
            })
        
        return Response({
            'period': period,
            'start_date': str(start_dt.date()) if start_dt else 'all',
            'end_date': str(now.date()),
            'summary': {
                'total_revenue': float(total_revenue),
                'total_cost': float(total_cost),
                'total_profit': total_profit,
                'total_orders': total_orders,
                'total_alerts': total_alerts
            },
            'daily_stats': daily_list,
            'machine_ranking': machine_list
        })
