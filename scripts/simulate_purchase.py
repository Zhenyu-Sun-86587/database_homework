"""
购买模拟脚本 - 测试触发器功能
运行方式: python scripts/simulate_purchase.py
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vending_system.settings')
django.setup()

from users.models import AppUser
from resources.models import BizMachine, BizProduct
from inventory.models import BizInventory, LogTransaction
from monitor.models import LogAlert


def purchase(user_username: str, machine_code: str, product_name: str):
    """
    模拟购买操作
    1. 验证用户余额
    2. 验证库存
    3. 创建交易记录（触发器会自动扣减库存）
    4. 扣减用户余额
    """
    print(f"\n{'='*50}")
    print(f"购买操作: 用户={user_username}, 机器={machine_code}, 商品={product_name}")
    print('='*50)

    # 获取用户
    try:
        user = AppUser.objects.get(username=user_username)
    except AppUser.DoesNotExist:
        print(f"错误: 用户 {user_username} 不存在")
        return False

    # 获取机器
    try:
        machine = BizMachine.objects.get(machine_code=machine_code)
    except BizMachine.DoesNotExist:
        print(f"错误: 机器 {machine_code} 不存在")
        return False

    # 检查机器状态
    if machine.status == 'fault':
        print(f"错误: 机器 {machine_code} 故障中")
        return False

    # 获取商品
    try:
        product = BizProduct.objects.get(name=product_name)
    except BizProduct.DoesNotExist:
        print(f"错误: 商品 {product_name} 不存在")
        return False

    # 获取库存
    try:
        inventory = BizInventory.objects.get(machine=machine, product=product)
    except BizInventory.DoesNotExist:
        print(f"错误: 机器 {machine_code} 没有商品 {product_name}")
        return False

    # 检查库存
    if inventory.current_stock <= 0:
        print(f"错误: 商品 {product_name} 已售罄")
        return False

    # 检查余额
    if user.balance < product.sell_price:
        print(f"错误: 余额不足 (需要 {product.sell_price}, 当前 {user.balance})")
        return False

    print(f"购买前库存: {inventory.current_stock}")
    print(f"用户余额: {user.balance}")

    # 获取当前报警数量
    alert_count_before = LogAlert.objects.count()

    # 创建交易记录（触发器会自动扣减库存）
    transaction = LogTransaction.objects.create(
        user=user,
        machine=machine,
        product=product,
        amount=product.sell_price
    )
    print(f"交易创建成功: ID={transaction.id}")

    # 扣减用户余额
    user.balance -= product.sell_price
    user.save()

    # 刷新库存数据
    inventory.refresh_from_db()
    print(f"购买后库存: {inventory.current_stock}")
    print(f"用户余额: {user.balance}")

    # 检查是否触发了报警
    alert_count_after = LogAlert.objects.count()
    if alert_count_after > alert_count_before:
        new_alerts = LogAlert.objects.order_by('-id')[:alert_count_after - alert_count_before]
        for alert in new_alerts:
            print(f"\n*** 触发报警 ***: {alert.alert_type} - {alert.message}")

    print(f"\n购买成功!")
    return True


def show_status():
    """显示当前系统状态"""
    print("\n" + "="*60)
    print("当前系统状态")
    print("="*60)

    print("\n--- 库存状态 ---")
    for inv in BizInventory.objects.select_related('machine', 'product').all():
        status = ""
        if inv.current_stock == 0:
            status = " [售罄]"
        elif inv.current_stock < 5:
            status = " [低库存]"
        print(f"{inv.machine.machine_code} - {inv.product.name}: {inv.current_stock}/{inv.max_capacity}{status}")

    print("\n--- 最近报警 ---")
    alerts = LogAlert.objects.order_by('-created_at')[:5]
    if alerts:
        for alert in alerts:
            print(f"[{alert.created_at}] {alert.alert_type}: {alert.message}")
    else:
        print("暂无报警记录")

    print("\n--- 最近交易 ---")
    transactions = LogTransaction.objects.order_by('-created_at')[:5]
    if transactions:
        for t in transactions:
            print(f"[{t.created_at}] {t.user.username} 在 {t.machine.machine_code} 购买 {t.product.name} - {t.amount}元")
    else:
        print("暂无交易记录")


if __name__ == '__main__':
    # 显示初始状态
    show_status()

    # 模拟多次购买，测试触发器
    print("\n" + "#"*60)
    print("开始模拟购买测试...")
    print("#"*60)

    # 连续购买同一商品，测试库存预警触发器
    machine_code = 'VM-A001'
    product_name = '可口可乐'
    user = 'student001'

    # 先把库存设置到5，便于测试
    inv = BizInventory.objects.get(
        machine__machine_code=machine_code,
        product__name=product_name
    )
    inv.current_stock = 6
    inv.save()
    print(f"\n已将 {machine_code} 的 {product_name} 库存设置为 6，准备测试低库存预警...")

    # 进行两次购买，第二次应该触发预警
    purchase(user, machine_code, product_name)  # 6->5 不触发
    purchase(user, machine_code, product_name)  # 5->4 触发预警!

    # 再买几次测试售罄
    inv.refresh_from_db()
    inv.current_stock = 1
    inv.save()
    print(f"\n已将库存设置为 1，准备测试售罄预警...")
    purchase(user, machine_code, product_name)  # 1->0 触发售罄预警!

    # 最终状态
    show_status()
