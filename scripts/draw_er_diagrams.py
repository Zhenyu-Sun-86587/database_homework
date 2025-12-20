import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def draw_entity(ax, x, y, text, width=3, height=1.5):
    rect = patches.Rectangle((x - width/2, y - height/2), width, height, 
                             linewidth=1.5, edgecolor='black', facecolor='white', zorder=10)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold', zorder=11)
    return (x, y)

def draw_relationship(ax, x, y, text, width=2.5, height=1.5):
    # 菱形
    polygon = patches.Polygon([[x, y + height/2], [x + width/2, y], [x, y - height/2], [x - width/2, y]],
                              closed=True, linewidth=1.5, edgecolor='black', facecolor='white', zorder=10)
    ax.add_patch(polygon)
    ax.text(x, y, text, ha='center', va='center', fontsize=10, zorder=11)
    return (x, y)

def draw_attribute(ax, x, y, text, is_pk=False, width=2.2, height=1.0):
    ellipse = patches.Ellipse((x, y), width, height, 
                              linewidth=1.5, edgecolor='black', facecolor='white', zorder=10)
    ax.add_patch(ellipse)
    
    if is_pk:
        # 主键用下划线
        ax.text(x, y, text, ha='center', va='center', fontsize=8, zorder=11,
                fontweight='bold', style='italic')
    else:
        ax.text(x, y, text, ha='center', va='center', fontsize=8, zorder=11)
    return (x, y)

def connect(ax, p1, p2, text=None):
    line = lines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color='black', linewidth=1, zorder=1)
    ax.add_line(line)
    if text:
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        ax.text(mid_x, mid_y, text, ha='center', va='center', fontsize=9, backgroundcolor='white', zorder=5)

def setup_plot(figsize=(16, 10), xlim=24, ylim=16):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def save_plot(fig, filename):
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'images', filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved {output_path}")
    plt.close(fig)

# =============================================================================
# 1. 用户子系统 ER图
# 实体: SYS_ADMIN, SYS_STAFF, APP_USER
# =============================================================================
def draw_user_subsystem():
    fig, ax = setup_plot()
    
    # 实体
    p_admin = draw_entity(ax, 4, 10, "SYS_ADMIN\n(管理员)")
    p_staff = draw_entity(ax, 12, 10, "SYS_STAFF\n(运维人员)")
    p_user = draw_entity(ax, 20, 10, "APP_USER\n(用户)")
    
    # 管理员属性: Aid, Aaccount, Apassword, Apermission, Created_time
    connect(ax, p_admin, draw_attribute(ax, 2, 13, "Aid", True))
    connect(ax, p_admin, draw_attribute(ax, 4, 13, "Aaccount"))
    connect(ax, p_admin, draw_attribute(ax, 6, 13, "Apassword"))
    connect(ax, p_admin, draw_attribute(ax, 3, 7, "Apermission"))
    connect(ax, p_admin, draw_attribute(ax, 5.5, 7, "Created_time"))
    
    # 运维人员属性: Sid, Staff_id, Sname, Sphone, Sregion_code, Created_time
    connect(ax, p_staff, draw_attribute(ax, 9, 13, "Sid", True))
    connect(ax, p_staff, draw_attribute(ax, 11, 13, "Staff_id"))
    connect(ax, p_staff, draw_attribute(ax, 13, 13, "Sname"))
    connect(ax, p_staff, draw_attribute(ax, 15, 13, "Sphone"))
    connect(ax, p_staff, draw_attribute(ax, 10.5, 7, "Sregion_code"))
    connect(ax, p_staff, draw_attribute(ax, 13.5, 7, "Created_time"))
    
    # 用户属性: Uid, Uaccount, Ubalance, Created_time
    connect(ax, p_user, draw_attribute(ax, 18, 13, "Uid", True))
    connect(ax, p_user, draw_attribute(ax, 20, 13, "Uaccount"))
    connect(ax, p_user, draw_attribute(ax, 22, 13, "Ubalance"))
    connect(ax, p_user, draw_attribute(ax, 20, 7, "Created_time"))
    
    save_plot(fig, "er_user_mpl.png")

# =============================================================================
# 2. 资源管理子系统 ER图
# 实体: BIZ_SUPPLIER, BIZ_PRODUCT, BIZ_MACHINE
# 关系: 供应(1:N), 销售(M:N)
# =============================================================================
def draw_resource_subsystem():
    fig, ax = setup_plot()
    
    # 实体
    p_supplier = draw_entity(ax, 4, 10, "BIZ_SUPPLIER\n(供应商)")
    p_product = draw_entity(ax, 12, 10, "BIZ_PRODUCT\n(商品)")
    p_machine = draw_entity(ax, 20, 10, "BIZ_MACHINE\n(贩卖机)")
    
    # 关系
    p_supply = draw_relationship(ax, 8, 10, "供应")
    p_store = draw_relationship(ax, 16, 10, "销售")
    
    # 连接
    connect(ax, p_supplier, p_supply, "1")
    connect(ax, p_supply, p_product, "N")
    connect(ax, p_machine, p_store, "1")
    connect(ax, p_store, p_product, "N")
    
    # 供应商属性: Sid, Sname, Scontact, Created_time
    connect(ax, p_supplier, draw_attribute(ax, 2, 13, "Sid", True))
    connect(ax, p_supplier, draw_attribute(ax, 4, 13, "Sname"))
    connect(ax, p_supplier, draw_attribute(ax, 6, 13, "Scontact"))
    connect(ax, p_supplier, draw_attribute(ax, 4, 7, "Created_time"))
    
    # 商品属性: Pid, Pname, Inprice, Outprice, Sid(FK), Created_time
    connect(ax, p_product, draw_attribute(ax, 10, 13, "Pid", True))
    connect(ax, p_product, draw_attribute(ax, 12, 13, "Pname"))
    connect(ax, p_product, draw_attribute(ax, 14, 13, "Inprice"))
    connect(ax, p_product, draw_attribute(ax, 10, 7, "Outprice"))
    connect(ax, p_product, draw_attribute(ax, 12, 7, "Sid(FK)"))
    connect(ax, p_product, draw_attribute(ax, 14, 7, "Created_time"))
    
    # 贩卖机属性: Mid, Machine_code, Mlocation, Mstatus, Mregion_code, Created_time
    connect(ax, p_machine, draw_attribute(ax, 18, 13, "Mid", True))
    connect(ax, p_machine, draw_attribute(ax, 20, 13, "Machine_code"))
    connect(ax, p_machine, draw_attribute(ax, 22, 13, "Mlocation"))
    connect(ax, p_machine, draw_attribute(ax, 18, 7, "Mstatus"))
    connect(ax, p_machine, draw_attribute(ax, 20, 7, "Mregion_code"))
    connect(ax, p_machine, draw_attribute(ax, 22, 7, "Created_time"))
    
    save_plot(fig, "er_resource_mpl.png")

# =============================================================================
# 3. 库存与交易子系统 ER图
# 实体: BIZ_INVENTORY, LOG_TRANSACTION, LOG_RESTOCK
# 引用: BIZ_MACHINE, BIZ_PRODUCT, APP_USER, SYS_STAFF
# =============================================================================
def draw_inventory_subsystem():
    fig, ax = setup_plot(figsize=(22, 14), xlim=32, ylim=20)
    
    # --- 实体 ---
    # 中间核心
    p_machine = draw_entity(ax, 14, 10, "BIZ_MACHINE\n(贩卖机)", width=3.5, height=1.5)
    p_product = draw_entity(ax, 20, 10, "BIZ_PRODUCT\n(商品)", width=3.5, height=1.5)
    
    # 上方库存
    p_inventory = draw_entity(ax, 17, 16, "BIZ_INVENTORY\n(库存)")
    
    # 左侧交易
    p_user = draw_entity(ax, 4, 10, "APP_USER\n(用户)", width=3, height=1.5)
    p_transaction = draw_entity(ax, 9, 4, "LOG_TRANSACTION\n(交易)")
    
    # 右侧补货
    p_staff = draw_entity(ax, 28, 10, "SYS_STAFF\n(运维人员)", width=3.5, height=1.5)
    p_restock = draw_entity(ax, 23, 4, "LOG_RESTOCK\n(补货)")
    
    # --- 属性 ---
    
    # 库存属性: Iid, Mid(FK), Pid(FK), Current_stock, Max_capacity, Created_time
    connect(ax, p_inventory, draw_attribute(ax, 14, 18.5, "Iid", True))
    connect(ax, p_inventory, draw_attribute(ax, 16.5, 18.5, "Mid(FK)"))
    connect(ax, p_inventory, draw_attribute(ax, 19, 18.5, "Pid(FK)"))
    connect(ax, p_inventory, draw_attribute(ax, 15, 13.5, "Current_stock"))
    connect(ax, p_inventory, draw_attribute(ax, 19, 13.5, "Max_capacity"))
    connect(ax, p_inventory, draw_attribute(ax, 21.5, 16, "Created_time")) # Added
    
    # 交易属性: Tid, Uid(FK), Mid(FK), Pid(FK), Tamount, Tcost_price, Tdate
    connect(ax, p_transaction, draw_attribute(ax, 5, 2, "Tid", True))
    connect(ax, p_transaction, draw_attribute(ax, 7, 2, "Uid(FK)"))
    connect(ax, p_transaction, draw_attribute(ax, 9, 2, "Mid(FK)"))
    connect(ax, p_transaction, draw_attribute(ax, 11, 2, "Pid(FK)"))
    connect(ax, p_transaction, draw_attribute(ax, 13, 2, "Tamount"))
    connect(ax, p_transaction, draw_attribute(ax, 6, 6, "Tcost_price"))
    connect(ax, p_transaction, draw_attribute(ax, 12, 6, "Tdate"))
    
    # 补货属性: Rid, Sid(FK), Mid(FK), Pid(FK), Rquantity, Runit_cost, Rdate
    connect(ax, p_restock, draw_attribute(ax, 19, 2, "Rid", True))
    connect(ax, p_restock, draw_attribute(ax, 21, 2, "Sid(FK)"))
    connect(ax, p_restock, draw_attribute(ax, 23, 2, "Mid(FK)"))
    connect(ax, p_restock, draw_attribute(ax, 25, 2, "Pid(FK)"))
    connect(ax, p_restock, draw_attribute(ax, 27, 2, "Rquantity"))
    connect(ax, p_restock, draw_attribute(ax, 20, 6, "Runit_cost"))
    connect(ax, p_restock, draw_attribute(ax, 26, 6, "Rdate"))
    
    # --- 关系与连接 ---
    
    # 库存关系
    p_r_inv = draw_relationship(ax, 17, 13, "库存", width=1.8, height=1.2)
    connect(ax, p_machine, p_r_inv)
    connect(ax, p_product, p_r_inv)
    connect(ax, p_r_inv, p_inventory)

    # 交易关系
    p_r_trans = draw_relationship(ax, 8, 10, "购买", width=1.8, height=1.2)
    connect(ax, p_user, p_r_trans)
    connect(ax, p_r_trans, p_transaction)
    connect(ax, p_machine, p_transaction)
    connect(ax, p_product, p_transaction)

    # 补货关系
    p_r_restock = draw_relationship(ax, 24, 10, "补货", width=1.8, height=1.2)
    connect(ax, p_staff, p_r_restock)
    connect(ax, p_r_restock, p_restock)
    connect(ax, p_machine, p_restock)
    connect(ax, p_product, p_restock)
    
    save_plot(fig, "er_inventory_mpl.png")

# =============================================================================
# 4. 监控统计子系统 ER图
# 实体: LOG_ALERT, STAT_DAILY
# 引用: BIZ_MACHINE
# =============================================================================
def draw_monitor_subsystem():
    fig, ax = setup_plot()
    
    # 实体
    p_machine = draw_entity(ax, 12, 11, "BIZ_MACHINE\n(贩卖机)")
    p_alert = draw_entity(ax, 6, 5, "LOG_ALERT\n(预警)")
    p_daily = draw_entity(ax, 18, 5, "STAT_DAILY\n(日结)")
    
    # 关系
    p_r_alert = draw_relationship(ax, 6, 9, "预警")
    p_r_stat = draw_relationship(ax, 18, 9, "统计")
    
    # 连接
    connect(ax, p_machine, p_r_alert, "1")
    connect(ax, p_r_alert, p_alert, "N")
    connect(ax, p_machine, p_r_stat, "1")
    connect(ax, p_r_stat, p_daily, "N")
    
    # 预警属性: Aid, Mid(FK), Alert_type, Amessage, Adate
    connect(ax, p_alert, draw_attribute(ax, 3, 6.5, "Aid", True))
    connect(ax, p_alert, draw_attribute(ax, 3, 3.5, "Mid(FK)"))
    connect(ax, p_alert, draw_attribute(ax, 6, 3, "Alert_type"))
    connect(ax, p_alert, draw_attribute(ax, 9, 3.5, "Amessage"))
    connect(ax, p_alert, draw_attribute(ax, 9, 6.5, "Adate"))
    
    # 日结属性: Did, Stat_date, Mid(FK), Total_revenue, Total_cost, Order_count, Alert_count
    connect(ax, p_daily, draw_attribute(ax, 15, 6.5, "Did", True))
    connect(ax, p_daily, draw_attribute(ax, 15, 3.5, "Stat_date"))
    connect(ax, p_daily, draw_attribute(ax, 18, 3, "Mid(FK)"))
    connect(ax, p_daily, draw_attribute(ax, 21, 3.5, "Total_revenue"))
    connect(ax, p_daily, draw_attribute(ax, 21, 6.5, "Total_cost"))
    connect(ax, p_daily, draw_attribute(ax, 18, 7, "Order_count"))
    connect(ax, p_daily, draw_attribute(ax, 15, 7.5, "Alert_count"))
    
    save_plot(fig, "er_monitor_mpl.png")

# =============================================================================
# 5. 全局ER图（省略属性）
# =============================================================================
def draw_global_er():
    fig, ax = setup_plot(figsize=(18, 12), xlim=26, ylim=18)
    
    # 所有实体 - 增加中文标注
    p_admin = draw_entity(ax, 3, 14, "SYS_ADMIN\n(管理员)", width=3, height=1.2)
    p_staff = draw_entity(ax, 3, 10, "SYS_STAFF\n(运维人员)", width=3, height=1.2)
    p_user = draw_entity(ax, 3, 6, "APP_USER\n(用户)", width=3, height=1.2)
    
    p_supplier = draw_entity(ax, 3, 2, "BIZ_SUPPLIER\n(供应商)", width=3, height=1.2)
    
    p_machine = draw_entity(ax, 13, 10, "BIZ_MACHINE\n(贩卖机)", width=3.5, height=1.5)
    p_product = draw_entity(ax, 13, 5, "BIZ_PRODUCT\n(商品)", width=3.5, height=1.5)
    
    p_inventory = draw_entity(ax, 13, 15, "BIZ_INVENTORY\n(库存)", width=3.5, height=1.2)
    p_transaction = draw_entity(ax, 8, 3, "LOG_TRANSACTION\n(交易)", width=3.5, height=1.2)
    p_restock = draw_entity(ax, 18, 3, "LOG_RESTOCK\n(补货)", width=3.5, height=1.2)
    
    p_alert = draw_entity(ax, 23, 12, "LOG_ALERT\n(预警)", width=3, height=1.2)
    p_daily = draw_entity(ax, 23, 8, "STAT_DAILY\n(日结)", width=3, height=1.2)
    
    # 关系
    p_r_supply = draw_relationship(ax, 8, 4, "供应", width=1.5, height=1)
    p_r_inv = draw_relationship(ax, 13, 12.5, "库存", width=1.5, height=1)
    p_r_trans = draw_relationship(ax, 7, 6, "交易", width=1.5, height=1)
    p_r_restock = draw_relationship(ax, 19, 6, "补货", width=1.5, height=1)
    p_r_alert = draw_relationship(ax, 19, 12, "预警", width=1.5, height=1)
    p_r_stat = draw_relationship(ax, 19, 8, "统计", width=1.5, height=1)
    
    # 连接
    connect(ax, p_supplier, p_r_supply)
    connect(ax, p_r_supply, p_product)
    
    connect(ax, p_machine, p_r_inv)
    connect(ax, p_product, p_r_inv)
    connect(ax, p_r_inv, p_inventory)
    
    connect(ax, p_user, p_r_trans)
    connect(ax, p_r_trans, p_transaction)
    connect(ax, p_machine, p_transaction)
    connect(ax, p_product, p_transaction)
    
    connect(ax, p_staff, p_r_restock)
    connect(ax, p_r_restock, p_restock)
    connect(ax, p_machine, p_restock)
    connect(ax, p_product, p_restock)
    
    connect(ax, p_machine, p_r_alert)
    connect(ax, p_r_alert, p_alert)
    
    connect(ax, p_machine, p_r_stat)
    connect(ax, p_r_stat, p_daily)
    
    save_plot(fig, "er_global_mpl.png")

if __name__ == "__main__":
    print("Generating ER diagrams...")
    draw_user_subsystem()
    draw_resource_subsystem()
    draw_inventory_subsystem()
    draw_monitor_subsystem()
    draw_global_er()
    print("Done.")
