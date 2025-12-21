# 校园智能贩卖机管理系统

## 项目简介

针对校园自动贩卖机人工巡检效率低、缺货响应慢的问题，设计的**全链路管理系统**。

**核心特性：**
- 利用 **MySQL 触发器** 实现毫秒级库存预警
- 现代化 **React + TypeScript** 前端
- 完整的 **CRUD 管理** + **财务统计**
- 打通"销售-监控-补货-统计"闭环
- 陈氏风格 **E-R 图** 自动生成

---

## 技术栈

| 层级       | 技术                                              |
| ---------- | ------------------------------------------------- |
| **后端**   | Python 3.13+ / Django 4.2 / Django REST Framework |
| **数据库** | MySQL 8.0+ (必须，支持触发器)                     |
| **前端**   | React 19 / TypeScript / Ant Design / Vite         |
| **样式**   | Tailwind CSS / Framer Motion                      |

---

## 快速开始

### 1. 克隆项目
```bash
git clone <repo_url>
cd database_homework
```

### 2. 后端配置
```bash
# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 安装依赖
pip install django djangorestframework django-cors-headers mysqlclient
```

### 3. 数据库配置

**方式一：使用备份文件恢复（推荐）**
```bash
mysql -u root -p < vending_db_backup.sql
```

**方式二：手动创建**
```sql
CREATE DATABASE vending_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `vending_system/settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vending_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 初始化测试数据
```bash
python scripts/init_data.py
```

### 6. 前端配置
```bash
cd frontend_new
npm install
```

---

## 启动项目

### 启动后端
```bash
.venv\Scripts\activate
python manage.py runserver
```
后端地址: http://127.0.0.1:8000/

### 启动前端
```bash
cd frontend_new
npm run dev
```
前端地址: http://localhost:5173/

---

## 功能模块

| 模块             | 功能说明                                   |
| ---------------- | ------------------------------------------ |
| 📊 **仪表盘**     | 实时显示机器数量、低库存预警、今日营收统计 |
| 🖥️ **设备管理**   | 贩卖机 CRUD、状态管理、区域分配            |
| 📦 **商品管理**   | 商品 CRUD、进价/售价设置、供应商关联       |
| 📈 **库存管理**   | 机器-商品库存查询、库存预警提示            |
| 👥 **用户管理**   | 学生用户管理、余额查看                     |
| 🏪 **供应商管理** | 供应商信息 CRUD                            |
| 💰 **交易记录**   | 交易流水查询、退货处理                     |
| 📥 **补货记录**   | 补货历史、新建补货                         |
| 👨‍🔧 **运维人员**   | 运维人员 CRUD、区域分配                    |
| 📈 **财务统计**   | 营收/成本/利润统计、日/周/月报表           |
| 📱 **移动端购买** | 模拟手机购买界面                           |

---

## 数据库设计

### 关系模式 (11张表)

| 表名              | 中文名   | 说明              |
| ----------------- | -------- | ----------------- |
| `sys_admin`       | 管理员   | 系统管理账号      |
| `sys_staff`       | 运维人员 | 负责补货维护      |
| `app_user`        | 学生用户 | 购买商品的消费者  |
| `biz_supplier`    | 供应商   | 商品供应来源      |
| `biz_machine`     | 贩卖机   | 核心设备实体      |
| `biz_product`     | 商品     | 销售商品信息      |
| `biz_inventory`   | 库存     | 机器-商品库存关系 |
| `log_transaction` | 交易记录 | 购买交易流水      |
| `log_restock`     | 补货记录 | 补货操作日志      |
| `log_alert`       | 预警记录 | 触发器自动生成    |
| `stat_daily`      | 日结统计 | 每日经营数据      |

### 数据库触发器 (5个)

触发器定义文件：`inventory/migrations/0002_create_triggers.py`

| 触发器                     | 触发条件       | 功能                          |
| -------------------------- | -------------- | ----------------------------- |
| `monitor_low_stock`        | 库存更新后     | 库存 ≥5→<5 时插入缺货预警     |
| `monitor_empty_stock`      | 库存更新后     | 库存 >0→0 时插入售罄紧急预警  |
| `monitor_machine_fault`    | 机器状态更新后 | 状态变为 fault 时插入故障预警 |
| `after_transaction_insert` | 交易记录插入后 | 自动扣减库存 -1               |
| `after_restock_insert`     | 补货记录插入后 | 自动增加库存（不超最大容量）  |

---

## 项目结构

```
database_homework/
├── vending_system/         # Django 项目配置
│   ├── settings.py         # 数据库配置
│   └── urls.py             # API 路由
├── users/                  # 用户模块 (SysAdmin, SysStaff, AppUser)
├── resources/              # 资源模块 (BizMachine, BizProduct, BizSupplier)
├── inventory/              # 库存模块 (BizInventory, LogTransaction, LogRestock)
│   └── migrations/
│       └── 0002_create_triggers.py  # ⭐ 触发器定义
├── monitor/                # 监控模块 (LogAlert, StatDaily)
├── scripts/                # 工具脚本
│   ├── init_data.py        # 初始化测试数据
│   ├── simulate_purchase.py # 模拟购买测试
│   └── generate_er_diagrams.py # 生成 E-R 图
├── assets/images/          # 图片资源 (E-R 图、截图等)
├── frontend_new/           # React 前端
├── vending_db_backup.sql   # 数据库备份文件
├── 实验八报告.md           # 完整实验报告
└── README.md
```

---

## API 接口

| 模块   | 端点                 | 方法                   |
| ------ | -------------------- | ---------------------- |
| 机器   | `/api/machines/`     | GET, POST, PUT, DELETE |
| 商品   | `/api/products/`     | GET, POST, PUT, DELETE |
| 库存   | `/api/inventories/`  | GET, POST, PUT, DELETE |
| 交易   | `/api/transactions/` | GET, POST, DELETE      |
| 补货   | `/api/restocks/`     | GET, POST, DELETE      |
| 用户   | `/api/app-users/`    | GET, POST, PUT, DELETE |
| 供应商 | `/api/suppliers/`    | GET, POST, PUT, DELETE |
| 运维   | `/api/sys-staffs/`   | GET, POST, PUT, DELETE |
| 预警   | `/api/alerts/`       | GET                    |
| 日结   | `/api/stat-daily/`   | GET                    |


