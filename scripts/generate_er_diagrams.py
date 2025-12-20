import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def create_figure(title, figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=16, pad=20)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax

def draw_entity(ax, x, y, text, width=12, height=6, color='#E6F3FF'):
    """绘制实体（矩形）"""
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, 
                             linewidth=1.5, edgecolor='black', facecolor=color, zorder=10)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold', zorder=11)
    return (x, y)

def draw_attribute(ax, x, y, text, width=10, height=5, color='#FFF2CC', is_primary=False):
    """绘制属性（椭圆）"""
    ellipse = patches.Ellipse((x, y), width, height, 
                              linewidth=1.5, edgecolor='black', facecolor=color, zorder=10)
    ax.add_patch(ellipse)
    
    if is_primary:
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', zorder=11)
        # Draw a line under the text for primary keys
        ax.plot([x-width/3, x+width/3], [y-1, y-1], color='black', linewidth=1, zorder=12)
    else:
        ax.text(x, y, text, ha='center', va='center', fontsize=9, zorder=11)
    return (x, y)

def draw_relationship(ax, x, y, text, width=12, height=8, color='#E2F0D9'):
    """绘制联系（菱形）"""
    polygon = patches.Polygon([[x, y + height/2], [x + width/2, y], 
                               [x, y - height/2], [x - width/2, y]], 
                              linewidth=1.5, edgecolor='black', facecolor=color, zorder=10)
    ax.add_patch(polygon)
    ax.text(x, y, text, ha='center', va='center', fontsize=9, zorder=11)
    return (x, y)

def connect(ax, p1, p2, text=None):
    """连接两个点"""
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='black', linewidth=1, zorder=1)
    if text:
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        # Add a small white box background for the text to make it readable
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7)
        ax.text(mid_x, mid_y, text, ha='center', va='center', fontsize=8, bbox=bbox_props, zorder=5)

def save_fig(fig, filename):
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'images')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated {filepath}")

# --- 1. 用户子系统 ---
def draw_user_subsystem():
    fig, ax = create_figure("用户子系统E-R图")
    
    # Entities
    pos_admin = draw_entity(ax, 20, 70, "管理员")
    pos_staff = draw_entity(ax, 50, 70, "运维人员")
    pos_user = draw_entity(ax, 80, 70, "学生用户")
    
    # Attributes for Admin
    connect(ax, pos_admin, draw_attribute(ax, 10, 85, "管理员编号", is_primary=True))
    connect(ax, pos_admin, draw_attribute(ax, 20, 85, "账号"))
    connect(ax, pos_admin, draw_attribute(ax, 30, 85, "密码"))
    connect(ax, pos_admin, draw_attribute(ax, 10, 55, "权限"))
    connect(ax, pos_admin, draw_attribute(ax, 25, 55, "创建时间"))

    # Attributes for Staff
    connect(ax, pos_staff, draw_attribute(ax, 40, 85, "运维编号", is_primary=True))
    connect(ax, pos_staff, draw_attribute(ax, 50, 85, "工号"))
    connect(ax, pos_staff, draw_attribute(ax, 60, 85, "姓名"))
    connect(ax, pos_staff, draw_attribute(ax, 40, 55, "电话"))
    connect(ax, pos_staff, draw_attribute(ax, 50, 55, "区域"))
    connect(ax, pos_staff, draw_attribute(ax, 60, 55, "入职时间"))

    # Attributes for User
    connect(ax, pos_user, draw_attribute(ax, 70, 85, "用户编号", is_primary=True))
    connect(ax, pos_user, draw_attribute(ax, 80, 85, "账号"))
    connect(ax, pos_user, draw_attribute(ax, 90, 85, "余额"))
    connect(ax, pos_user, draw_attribute(ax, 80, 55, "创建时间"))

    save_fig(fig, 'er_user_mpl.png')

# --- 2. 资源管理子系统 ---
def draw_resource_subsystem():
    fig, ax = create_figure("资源管理子系统E-R图")
    
    # Entities
    pos_supplier = draw_entity(ax, 20, 50, "供应商")
    pos_product = draw_entity(ax, 50, 50, "商品")
    pos_machine = draw_entity(ax, 80, 50, "贩卖机")
    
    # Relationship
    pos_supply = draw_relationship(ax, 35, 50, "供应")
    connect(ax, pos_supplier, pos_supply, "1")
    connect(ax, pos_supply, pos_product, "n")

    # Attributes for Supplier
    connect(ax, pos_supplier, draw_attribute(ax, 10, 65, "供应商编号", is_primary=True))
    connect(ax, pos_supplier, draw_attribute(ax, 20, 65, "名称"))
    connect(ax, pos_supplier, draw_attribute(ax, 30, 65, "联系人"))
    connect(ax, pos_supplier, draw_attribute(ax, 20, 35, "合作时间"))

    # Attributes for Product
    connect(ax, pos_product, draw_attribute(ax, 40, 65, "商品编号", is_primary=True))
    connect(ax, pos_product, draw_attribute(ax, 50, 65, "名称"))
    connect(ax, pos_product, draw_attribute(ax, 60, 65, "进价"))
    connect(ax, pos_product, draw_attribute(ax, 40, 35, "售价"))
    connect(ax, pos_product, draw_attribute(ax, 60, 35, "创建时间"))

    # Attributes for Machine
    connect(ax, pos_machine, draw_attribute(ax, 70, 65, "设备编号", is_primary=True))
    connect(ax, pos_machine, draw_attribute(ax, 80, 65, "机器编码"))
    connect(ax, pos_machine, draw_attribute(ax, 90, 65, "位置"))
    connect(ax, pos_machine, draw_attribute(ax, 70, 35, "状态"))
    connect(ax, pos_machine, draw_attribute(ax, 80, 35, "区域"))
    connect(ax, pos_machine, draw_attribute(ax, 90, 35, "部署时间"))

    save_fig(fig, 'er_resource_mpl.png')

# --- 3. 库存与交易子系统 ---
def draw_inventory_subsystem():
    fig, ax = create_figure("库存与交易子系统E-R图")
    
    # Entities
    pos_machine = draw_entity(ax, 20, 50, "贩卖机")
    pos_product = draw_entity(ax, 80, 50, "商品")
    pos_user = draw_entity(ax, 50, 80, "学生用户")
    pos_staff = draw_entity(ax, 50, 20, "运维人员")

    # Relationships
    # Inventory (Machine - Product) M:N
    pos_stock = draw_relationship(ax, 50, 50, "库存")
    connect(ax, pos_machine, pos_stock, "m")
    connect(ax, pos_stock, pos_product, "n")
    
    # Transaction (User - Machine - Product)
    pos_trans = draw_relationship(ax, 50, 65, "交易")
    connect(ax, pos_user, pos_trans, "m")
    connect(ax, pos_machine, pos_trans, "n")
    connect(ax, pos_product, pos_trans, "p")

    # Restock (Staff - Machine - Product)
    pos_restock = draw_relationship(ax, 50, 35, "补货")
    connect(ax, pos_staff, pos_restock, "m")
    connect(ax, pos_machine, pos_restock, "n")
    connect(ax, pos_product, pos_restock, "p")

    # Attributes for Inventory Relation
    connect(ax, pos_stock, draw_attribute(ax, 40, 55, "当前库存"))
    connect(ax, pos_stock, draw_attribute(ax, 60, 55, "最大容量"))

    # Attributes for Transaction Relation
    connect(ax, pos_trans, draw_attribute(ax, 35, 70, "交易编号", is_primary=True))
    connect(ax, pos_trans, draw_attribute(ax, 45, 75, "金额"))
    connect(ax, pos_trans, draw_attribute(ax, 55, 75, "成本"))
    connect(ax, pos_trans, draw_attribute(ax, 65, 70, "时间"))

    # Attributes for Restock Relation
    connect(ax, pos_restock, draw_attribute(ax, 35, 30, "补货编号", is_primary=True))
    connect(ax, pos_restock, draw_attribute(ax, 45, 25, "数量"))
    connect(ax, pos_restock, draw_attribute(ax, 55, 25, "成本"))
    connect(ax, pos_restock, draw_attribute(ax, 65, 30, "时间"))

    save_fig(fig, 'er_inventory_mpl.png')

# --- 4. 监控统计子系统 ---
def draw_monitor_subsystem():
    fig, ax = create_figure("监控统计子系统E-R图")
    
    # Entities
    pos_machine = draw_entity(ax, 50, 50, "贩卖机")
    
    # Weak Entities (modeled as entities for simplicity but logically dependent)
    pos_alert = draw_entity(ax, 20, 50, "预警记录")
    pos_stat = draw_entity(ax, 80, 50, "日结统计")

    # Relationships
    pos_has_alert = draw_relationship(ax, 35, 50, "产生")
    connect(ax, pos_machine, pos_has_alert, "1")
    connect(ax, pos_has_alert, pos_alert, "n")

    pos_has_stat = draw_relationship(ax, 65, 50, "生成")
    connect(ax, pos_machine, pos_has_stat, "1")
    connect(ax, pos_has_stat, pos_stat, "n")

    # Attributes for Alert
    connect(ax, pos_alert, draw_attribute(ax, 10, 65, "预警编号", is_primary=True))
    connect(ax, pos_alert, draw_attribute(ax, 20, 65, "类型"))
    connect(ax, pos_alert, draw_attribute(ax, 30, 65, "信息"))
    connect(ax, pos_alert, draw_attribute(ax, 20, 35, "时间"))

    # Attributes for Stat
    connect(ax, pos_stat, draw_attribute(ax, 70, 65, "统计编号", is_primary=True))
    connect(ax, pos_stat, draw_attribute(ax, 80, 65, "日期"))
    connect(ax, pos_stat, draw_attribute(ax, 90, 65, "总收入"))
    connect(ax, pos_stat, draw_attribute(ax, 70, 35, "总成本"))
    connect(ax, pos_stat, draw_attribute(ax, 80, 35, "订单数"))
    connect(ax, pos_stat, draw_attribute(ax, 90, 35, "报警数"))

    save_fig(fig, 'er_monitor_mpl.png')

# --- 5. 全局E-R图 (无属性) ---
def draw_global_er():
    fig, ax = create_figure("全局E-R图", figsize=(14, 10))
    
    # Entities
    pos_machine = draw_entity(ax, 50, 50, "贩卖机")
    pos_product = draw_entity(ax, 80, 50, "商品")
    pos_supplier = draw_entity(ax, 80, 80, "供应商")
    pos_user = draw_entity(ax, 20, 50, "学生用户")
    pos_staff = draw_entity(ax, 50, 80, "运维人员")
    pos_admin = draw_entity(ax, 20, 80, "管理员")
    pos_alert = draw_entity(ax, 50, 20, "预警记录")
    pos_stat = draw_entity(ax, 80, 20, "日结统计")

    # Relationships
    
    # Supplier - Product
    pos_supply = draw_relationship(ax, 80, 65, "供应")
    connect(ax, pos_supplier, pos_supply, "1")
    connect(ax, pos_supply, pos_product, "n")

    # Machine - Product (Inventory)
    pos_stock = draw_relationship(ax, 65, 50, "库存")
    connect(ax, pos_machine, pos_stock, "m")
    connect(ax, pos_stock, pos_product, "n")

    # User - Machine - Product (Transaction)
    # Ternary relationship: User buys Product from Machine
    pos_buy = draw_relationship(ax, 50, 35, "交易")
    connect(ax, pos_user, pos_buy, "m")
    connect(ax, pos_machine, pos_buy, "n")
    connect(ax, pos_product, pos_buy, "p")
    
    # Staff - Machine - Product (Restock)
    # Ternary relationship: Staff restocks Product in Machine
    # Placing Restock node to avoid overlap. 
    # Staff(50,80), Machine(50,50), Product(80,50)
    pos_restock = draw_relationship(ax, 60, 65, "补货")
    connect(ax, pos_staff, pos_restock, "m")
    connect(ax, pos_machine, pos_restock, "n")
    connect(ax, pos_product, pos_restock, "p")

    # Machine - Alert
    pos_gen_alert = draw_relationship(ax, 40, 35, "产生")
    connect(ax, pos_machine, pos_gen_alert, "1")
    connect(ax, pos_gen_alert, pos_alert, "n")

    # Machine - Stat
    pos_gen_stat = draw_relationship(ax, 65, 35, "统计")
    connect(ax, pos_machine, pos_gen_stat, "1")
    connect(ax, pos_gen_stat, pos_stat, "n")

    # Admin manages System
    pos_manage = draw_relationship(ax, 35, 80, "管理")
    connect(ax, pos_admin, pos_manage, "1")
    connect(ax, pos_manage, pos_staff, "n")
    connect(ax, pos_manage, pos_user, "n")

    save_fig(fig, 'er_global_mpl.png')

if __name__ == "__main__":
    draw_user_subsystem()
    draw_resource_subsystem()
    draw_inventory_subsystem()
    draw_monitor_subsystem()
    draw_global_er()
