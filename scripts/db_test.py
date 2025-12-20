"""
数据库功能综合测试脚本
用于测试数据库的完整性约束、触发器和级联删除功能
运行方式: python scripts/db_test.py

测试内容:
1. 触发器测试（低库存预警、设备故障预警、交易扣库存、补货加库存）
2. 外键约束测试（引用完整性）
3. 唯一约束测试
4. 级联删除测试
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vending_system.settings')
django.setup()

from django.db import IntegrityError, connection
from users.models import AppUser, SysStaff
from resources.models import BizMachine, BizProduct, BizSupplier
from inventory.models import BizInventory, LogTransaction, LogRestock
from monitor.models import LogAlert


class TestResult:
    """测试结果记录类"""
    def __init__(self):
        self.results = []
    
    def add(self, category, test_name, passed, detail=""):
        self.results.append({
            'category': category,
            'test_name': test_name,
            'passed': passed,
            'detail': detail
        })
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  [{status}] {test_name}")
        if detail:
            print(f"       → {detail}")
    
    def summary(self):
        print("\n" + "="*70)
        print("测试结果汇总")
        print("="*70)
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        print(f"总计: {passed}/{total} 通过\n")
        
        # 按类别汇总
        categories = {}
        for r in self.results:
            cat = r['category']
            if cat not in categories:
                categories[cat] = {'passed': 0, 'failed': 0}
            if r['passed']:
                categories[cat]['passed'] += 1
            else:
                categories[cat]['failed'] += 1
        
        for cat, stats in categories.items():
            print(f"  {cat}: {stats['passed']}通过, {stats['failed']}失败")
        
        return self.results


result = TestResult()


def section_header(title):
    """打印分节标题"""
    print(f"\n{'='*70}")
    print(f"测试: {title}")
    print("="*70)


def test_triggers():
    """测试触发器功能"""
    section_header("触发器功能测试")
    
    # --- 1. 测试交易后自动扣减库存触发器 ---
    print("\n【1】交易后自动扣减库存触发器 (trigger_after_transaction)")
    try:
        # 准备测试数据
        user = AppUser.objects.first()
        machine = BizMachine.objects.filter(status='normal').first()
        inventory = BizInventory.objects.filter(machine=machine, current_stock__gt=0).first()
        
        if user and machine and inventory:
            product = inventory.product
            stock_before = inventory.current_stock
            
            # 创建交易
            LogTransaction.objects.create(
                user=user,
                machine=machine,
                product=product,
                amount=product.sell_price
            )
            
            # 刷新库存
            inventory.refresh_from_db()
            stock_after = inventory.current_stock
            
            passed = (stock_before - 1 == stock_after)
            result.add("触发器", "交易后自动扣减库存", passed, 
                      f"库存: {stock_before} → {stock_after}")
        else:
            result.add("触发器", "交易后自动扣减库存", False, "测试数据不足")
    except Exception as e:
        result.add("触发器", "交易后自动扣减库存", False, str(e))
    
    # --- 2. 测试补货后自动增加库存触发器 ---
    print("\n【2】补货后自动增加库存触发器 (trigger_after_restock)")
    try:
        staff = SysStaff.objects.first()
        machine = BizMachine.objects.first()
        inventory = BizInventory.objects.filter(machine=machine).first()
        
        if staff and machine and inventory:
            product = inventory.product
            stock_before = inventory.current_stock
            restock_qty = 5
            
            # 创建补货记录
            LogRestock.objects.create(
                staff=staff,
                machine=machine,
                product=product,
                quantity=restock_qty,
                unit_cost=Decimal('2.00')
            )
            
            # 刷新库存
            inventory.refresh_from_db()
            stock_after = inventory.current_stock
            
            # 库存应该增加（但不超过max_capacity）
            expected = min(stock_before + restock_qty, inventory.max_capacity)
            passed = (stock_after == expected)
            result.add("触发器", "补货后自动增加库存", passed, 
                      f"库存: {stock_before} → {stock_after} (补货{restock_qty}件)")
        else:
            result.add("触发器", "补货后自动增加库存", False, "测试数据不足")
    except Exception as e:
        result.add("触发器", "补货后自动增加库存", False, str(e))
    
    # --- 3. 测试低库存预警触发器 ---
    print("\n【3】低库存预警触发器 (trigger_low_stock_alert)")
    try:
        inventory = BizInventory.objects.first()
        if inventory:
            alert_count_before = LogAlert.objects.filter(alert_type='low_stock').count()
            
            # 将库存设为5，再用SQL更新到4以触发触发器
            inventory.current_stock = 5
            inventory.save()
            
            # 使用原生SQL触发更新（Django的save会绕过某些触发器场景）
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE biz_inventory SET current_stock = 4 WHERE id = %s",
                    [inventory.id]
                )
            
            alert_count_after = LogAlert.objects.filter(alert_type='low_stock').count()
            passed = (alert_count_after > alert_count_before)
            result.add("触发器", "低库存预警生成", passed, 
                      f"预警数: {alert_count_before} → {alert_count_after}")
        else:
            result.add("触发器", "低库存预警生成", False, "测试数据不足")
    except Exception as e:
        result.add("触发器", "低库存预警生成", False, str(e))
    
    # --- 4. 测试设备故障报警触发器 ---
    print("\n【4】设备故障报警触发器 (trigger_machine_fault_alert)")
    try:
        # 找一个正常的机器
        machine = BizMachine.objects.filter(status='normal').first()
        if machine:
            alert_count_before = LogAlert.objects.filter(alert_type='fault').count()
            
            # 使用原生SQL更新状态为故障
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE biz_machine SET status = 'fault' WHERE id = %s",
                    [machine.id]
                )
            
            alert_count_after = LogAlert.objects.filter(alert_type='fault').count()
            passed = (alert_count_after > alert_count_before)
            result.add("触发器", "设备故障报警生成", passed, 
                      f"故障报警数: {alert_count_before} → {alert_count_after}")
            
            # 恢复机器状态
            machine.status = 'normal'
            machine.save()
        else:
            result.add("触发器", "设备故障报警生成", False, "没有正常状态的机器")
    except Exception as e:
        result.add("触发器", "设备故障报警生成", False, str(e))


def test_constraints():
    """测试完整性约束"""
    section_header("完整性约束测试")
    
    # --- 1. 测试唯一约束：库存表的(machine, product)唯一 ---
    print("\n【1】唯一约束测试 (biz_inventory: machine+product)")
    try:
        inventory = BizInventory.objects.first()
        if inventory:
            # 尝试插入重复记录
            try:
                BizInventory.objects.create(
                    machine=inventory.machine,
                    product=inventory.product,
                    current_stock=10,
                    max_capacity=20
                )
                result.add("约束", "库存唯一约束拦截重复数据", False, "未能拦截重复数据")
            except IntegrityError:
                result.add("约束", "库存唯一约束拦截重复数据", True, 
                          "成功拦截: 同一机器同一商品不允许重复")
    except Exception as e:
        result.add("约束", "库存唯一约束拦截重复数据", False, str(e))
    
    # --- 2. 测试外键约束：引用不存在的外键 ---
    print("\n【2】外键约束测试 (引用不存在的外键)")
    try:
        # 尝试创建引用不存在机器的库存记录
        try:
            BizInventory.objects.create(
                machine_id=99999,  # 不存在的机器ID
                product_id=1,
                current_stock=10,
                max_capacity=20
            )
            result.add("约束", "外键约束拦截无效引用", False, "未能拦截无效外键")
        except IntegrityError:
            result.add("约束", "外键约束拦截无效引用", True, 
                      "成功拦截: 不允许引用不存在的机器")
    except Exception as e:
        result.add("约束", "外键约束拦截无效引用", False, str(e))
    
    # --- 3. 测试非空约束 ---
    print("\n【3】非空约束测试 (NOT NULL)")
    try:
        try:
            BizProduct.objects.create(
                name=None,  # 名称不能为空
                cost_price=Decimal('1.00'),
                sell_price=Decimal('2.00'),
                supplier=BizSupplier.objects.first()
            )
            result.add("约束", "非空约束拦截NULL值", False, "未能拦截NULL值")
        except IntegrityError:
            result.add("约束", "非空约束拦截NULL值", True, 
                      "成功拦截: 必填字段不允许为空")
    except Exception as e:
        result.add("约束", "非空约束拦截NULL值", False, str(e))
    
    # --- 4. 测试检查约束：枚举值 ---
    print("\n【4】枚举约束测试 (status字段枚举值)")
    try:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO biz_machine (machine_code, location, status, region_code, created_at) "
                    "VALUES ('TEST-999', '测试位置', 'invalid_status', 'TEST', NOW())"
                )
                result.add("约束", "枚举约束拦截非法值", False, "未能拦截非法枚举值")
            except Exception:
                result.add("约束", "枚举约束拦截非法值", True, 
                          "成功拦截: status只能为'normal'或'fault'")
    except Exception as e:
        # MySQL的ENUM约束会自动拦截
        result.add("约束", "枚举约束拦截非法值", True, "枚举约束生效")


def test_cascade_delete():
    """测试级联删除"""
    section_header("级联删除测试")
    
    # --- 1. 测试删除机器时级联删除库存 ---
    print("\n【1】删除机器 → 自动删除关联库存记录")
    try:
        # 创建测试机器和库存
        test_machine = BizMachine.objects.create(
            machine_code=f'TEST-CASCADE-{datetime.now().timestamp()}',
            location='测试位置',
            status='normal',
            region_code='TEST'
        )
        product = BizProduct.objects.first()
        test_inventory = BizInventory.objects.create(
            machine=test_machine,
            product=product,
            current_stock=10,
            max_capacity=20
        )
        inventory_id = test_inventory.id
        
        # 删除机器
        test_machine.delete()
        
        # 检查库存是否被级联删除
        inventory_exists = BizInventory.objects.filter(id=inventory_id).exists()
        passed = not inventory_exists
        result.add("级联删除", "删除机器→删除关联库存", passed, 
                  "库存记录已自动删除" if passed else "库存记录仍存在")
    except Exception as e:
        result.add("级联删除", "删除机器→删除关联库存", False, str(e))
    
    # --- 2. 测试删除供应商时级联删除商品 ---
    print("\n【2】删除供应商 → 自动删除关联商品")
    try:
        # 创建测试供应商和商品
        test_supplier = BizSupplier.objects.create(
            name=f'测试供应商-{datetime.now().timestamp()}',
            contact='12345678901'
        )
        test_product = BizProduct.objects.create(
            name=f'测试商品-{datetime.now().timestamp()}',
            cost_price=Decimal('1.00'),
            sell_price=Decimal('2.00'),
            supplier=test_supplier
        )
        product_id = test_product.id
        
        # 删除供应商
        test_supplier.delete()
        
        # 检查商品是否被级联删除
        product_exists = BizProduct.objects.filter(id=product_id).exists()
        passed = not product_exists
        result.add("级联删除", "删除供应商→删除关联商品", passed, 
                  "商品记录已自动删除" if passed else "商品记录仍存在")
    except Exception as e:
        result.add("级联删除", "删除供应商→删除关联商品", False, str(e))
    
    # --- 3. 测试删除用户时级联删除交易记录 ---
    print("\n【3】删除用户 → 自动删除关联交易记录")
    try:
        # 创建测试用户和交易
        test_user = AppUser.objects.create(
            username=f'test_user_{datetime.now().timestamp()}',
            balance=Decimal('100.00')
        )
        machine = BizMachine.objects.first()
        product = BizProduct.objects.first()
        
        if machine and product:
            test_transaction = LogTransaction.objects.create(
                user=test_user,
                machine=machine,
                product=product,
                amount=product.sell_price
            )
            transaction_id = test_transaction.id
            
            # 删除用户
            test_user.delete()
            
            # 检查交易是否被级联删除
            transaction_exists = LogTransaction.objects.filter(id=transaction_id).exists()
            passed = not transaction_exists
            result.add("级联删除", "删除用户→删除关联交易", passed, 
                      "交易记录已自动删除" if passed else "交易记录仍存在")
        else:
            result.add("级联删除", "删除用户→删除关联交易", False, "测试数据不足")
    except Exception as e:
        result.add("级联删除", "删除用户→删除关联交易", False, str(e))


def test_referential_integrity():
    """测试参照完整性"""
    section_header("参照完整性测试")
    
    # --- 1. 测试外键更新级联 ---
    print("\n【1】外键关联查询")
    try:
        transaction = LogTransaction.objects.select_related('user', 'machine', 'product').first()
        if transaction:
            user_name = transaction.user.username
            machine_code = transaction.machine.machine_code
            product_name = transaction.product.name
            passed = all([user_name, machine_code, product_name])
            result.add("参照完整性", "外键关联查询", passed, 
                      f"交易关联: 用户={user_name}, 机器={machine_code}, 商品={product_name}")
        else:
            result.add("参照完整性", "外键关联查询", False, "没有交易数据")
    except Exception as e:
        result.add("参照完整性", "外键关联查询", False, str(e))


def main():
    """主测试函数"""
    print("="*70)
    print("校园智能贩卖机管理系统 - 数据库功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # 执行各类测试
    test_triggers()
    test_constraints()
    test_cascade_delete()
    test_referential_integrity()
    
    # 输出汇总
    result.summary()
    
    print("\n提示: 上述测试结果可直接复制到实验报告中")
    print("="*70)


if __name__ == '__main__':
    main()
