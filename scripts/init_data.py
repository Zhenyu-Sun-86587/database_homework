"""
测试数据初始化脚本
运行方式: python scripts/init_data.py
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vending_system.settings')
django.setup()

from decimal import Decimal
from users.models import SysAdmin, SysStaff, AppUser
from resources.models import BizSupplier, BizMachine, BizProduct
from inventory.models import BizInventory

print("开始初始化测试数据...")

# 1. 创建管理员
admin, created = SysAdmin.objects.get_or_create(
    username='superadmin',
    defaults={'password': 'admin123', 'permission': 'superadmin'}
)
print(f"管理员: {admin.username} {'(新建)' if created else '(已存在)'}")

# 2. 创建运维人员
staffs_data = [
    {'staff_id': 'S001', 'name': '张三', 'phone': '13800001111', 'region_code': 'A'},
    {'staff_id': 'S002', 'name': '李四', 'phone': '13800002222', 'region_code': 'B'},
    {'staff_id': 'S003', 'name': '王五', 'phone': '13800003333', 'region_code': 'C'},
]
for data in staffs_data:
    staff, created = SysStaff.objects.get_or_create(staff_id=data['staff_id'], defaults=data)
    print(f"运维人员: {staff.name} {'(新建)' if created else '(已存在)'}")

# 3. 创建学生用户
users_data = [
    {'username': 'student001', 'balance': Decimal('100.00')},
    {'username': 'student002', 'balance': Decimal('50.00')},
    {'username': 'student003', 'balance': Decimal('200.00')},
]
for data in users_data:
    user, created = AppUser.objects.get_or_create(username=data['username'], defaults=data)
    print(f"学生用户: {user.username} {'(新建)' if created else '(已存在)'}")

# 4. 创建供应商
suppliers_data = [
    {'name': '可口可乐公司', 'contact': '010-12345678'},
    {'name': '农夫山泉', 'contact': '010-87654321'},
    {'name': '统一企业', 'contact': '021-55556666'},
]
suppliers = []
for data in suppliers_data:
    supplier, created = BizSupplier.objects.get_or_create(name=data['name'], defaults=data)
    suppliers.append(supplier)
    print(f"供应商: {supplier.name} {'(新建)' if created else '(已存在)'}")

# 5. 创建贩卖机
machines_data = [
    {'machine_code': 'VM-A001', 'location': '教学楼A栋1楼', 'status': 'normal', 'region_code': 'A'},
    {'machine_code': 'VM-A002', 'location': '教学楼A栋3楼', 'status': 'normal', 'region_code': 'A'},
    {'machine_code': 'VM-B001', 'location': '图书馆1楼', 'status': 'normal', 'region_code': 'B'},
    {'machine_code': 'VM-C001', 'location': '食堂门口', 'status': 'normal', 'region_code': 'C'},
]
machines = []
for data in machines_data:
    machine, created = BizMachine.objects.get_or_create(machine_code=data['machine_code'], defaults=data)
    machines.append(machine)
    print(f"贩卖机: {machine.machine_code} {'(新建)' if created else '(已存在)'}")

# 6. 创建商品
products_data = [
    {'name': '可口可乐', 'cost_price': Decimal('2.00'), 'sell_price': Decimal('3.50'), 'supplier': suppliers[0]},
    {'name': '雪碧', 'cost_price': Decimal('2.00'), 'sell_price': Decimal('3.50'), 'supplier': suppliers[0]},
    {'name': '芬达', 'cost_price': Decimal('2.00'), 'sell_price': Decimal('3.50'), 'supplier': suppliers[0]},
    {'name': '农夫山泉', 'cost_price': Decimal('1.00'), 'sell_price': Decimal('2.00'), 'supplier': suppliers[1]},
    {'name': '东方树叶', 'cost_price': Decimal('3.00'), 'sell_price': Decimal('5.00'), 'supplier': suppliers[1]},
    {'name': '统一冰红茶', 'cost_price': Decimal('2.50'), 'sell_price': Decimal('4.00'), 'supplier': suppliers[2]},
]
products = []
for data in products_data:
    product, created = BizProduct.objects.get_or_create(name=data['name'], defaults=data)
    products.append(product)
    print(f"商品: {product.name} {'(新建)' if created else '(已存在)'}")

# 7. 创建库存（每台机器放置所有商品，初始库存10个）
for machine in machines:
    for product in products:
        inventory, created = BizInventory.objects.get_or_create(
            machine=machine,
            product=product,
            defaults={'current_stock': 10, 'max_capacity': 20}
        )
        if created:
            print(f"库存: {machine.machine_code} - {product.name} (10/20)")

print("\n测试数据初始化完成!")
print(f"- 管理员: 1")
print(f"- 运维人员: {len(staffs_data)}")
print(f"- 学生用户: {len(users_data)}")
print(f"- 供应商: {len(suppliers_data)}")
print(f"- 贩卖机: {len(machines_data)}")
print(f"- 商品: {len(products_data)}")
print(f"- 库存记录: {len(machines) * len(products)}")
