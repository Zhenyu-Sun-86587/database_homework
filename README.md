# 校园智能贩卖机管理系统

## 项目简介

针对校园自动贩卖机人工巡检效率低、缺货响应慢的问题，设计的**全链路管理系统**。

**核心特性：**
- 利用 **MySQL 触发器** 实现毫秒级库存预警
- 现代化 **React + TypeScript** 前端
- 完整的 **CRUD 管理** + **财务统计**
- 打通"销售-监控-补货-统计"闭环

---

## 技术栈

| 层级       | 技术                                              |
| ---------- | ------------------------------------------------- |
| **后端**   | Python 3.10+ / Django 6.0 / Django REST Framework |
| **数据库** | MySQL 8.0+ (必须，支持触发器)                     |
| **前端**   | React 19 / TypeScript / Ant Design / Vite         |
| **样式**   | Tailwind CSS / Framer Motion                      |

---

## 环境配置

### 1. 安装依赖

#### 后端
```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装 Python 依赖
pip install django djangorestframework django-cors-headers mysqlclient
```

#### 前端
```bash
cd frontend_new
npm install
```

### 2. 数据库配置

1. 创建 MySQL 数据库：
```sql
CREATE DATABASE vending_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `vending_system/settings.py` 中的数据库配置：
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

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 初始化测试数据

```bash
python scripts/init_data.py
```

### 5. 创建管理员账号

```bash
python manage.py createsuperuser
```

---

## 启动项目

### 启动后端
```bash
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

### 📊 仪表盘 (Dashboard)
- 实时显示机器数量、低库存预警、今日营收等统计数据

### 🖥️ 机器管理 (Machines)
- 贩卖机 CRUD（增删改查）
- 状态管理（正常/故障）
- 区域分配

### 📦 商品管理 (Products)
- 商品 CRUD
- 进价/售价设置
- 供应商关联

### 📈 库存管理 (Inventory)
- 机器-商品库存查询
- 库存预警提示

### 👥 用户管理 (Users)
- 学生用户管理
- 余额查看

### 🏪 供应商管理 (Suppliers)
- 供应商信息 CRUD

### 💰 交易记录 (Transactions)
- 交易流水查询
- 支持退货（自动恢复库存和余额）

### 📥 补货记录 (Restocks)
- 补货历史
- 新建补货记录

### 👨‍🔧 运维人员 (Staff)
- 运维人员 CRUD
- 区域分配

### 📈 财务统计 (Statistics)
- 总营收/成本/利润统计
- 日/周/月报表
- 机器营收排名
- 日结统计生成

### 📱 手机端购买演示 (Mobile)
- 模拟手机购买界面
- 选择机器和商品
- 自动扣款和库存更新

---

## 数据库表结构 (11张表)

### A. 基础与资源

| 表名           | 说明     | 关键字段                           |
| -------------- | -------- | ---------------------------------- |
| `sys_admin`    | 管理员   | 用户名, 密码, 权限                 |
| `sys_staff`    | 运维人员 | 工号, 姓名, 电话, 负责区域         |
| `app_user`     | 学生用户 | 用户名, **余额**                   |
| `biz_supplier` | 供应商   | 名称, 联系方式                     |
| `biz_machine`  | 贩卖机   | 机器编号, 位置, **状态**, 区域     |
| `biz_product`  | 商品     | 名称, **进价**, **售价**, 供应商ID |

### B. 核心业务

| 表名              | 说明         | 关键字段                                       |
| ----------------- | ------------ | ---------------------------------------------- |
| `biz_inventory`   | 库存（核心） | 机器ID, 商品ID, **当前库存**, 最大容量         |
| `log_transaction` | 交易流水     | 用户ID, 机器ID, 商品ID, 金额, **成本价**       |
| `log_restock`     | 补货记录     | 运维人员ID, 机器ID, 商品ID, 数量, **单位成本** |

### C. 监控与统计

| 表名         | 说明     | 关键字段                                     |
| ------------ | -------- | -------------------------------------------- |
| `log_alert`  | 报警日志 | 机器ID, 类型, 报警内容 (触发器自动写入)      |
| `stat_daily` | 日结统计 | 日期, 机器ID, 总营收, **总成本**, **总利润** |

---

## 数据库触发器 (5个)

触发器定义在 `inventory/migrations/0002_create_triggers.py`：

| 触发器                     | 触发条件       | 功能                               |
| -------------------------- | -------------- | ---------------------------------- |
| `monitor_low_stock`        | 库存更新后     | 库存 ≥5 → <5 时插入**缺货预警**    |
| `monitor_empty_stock`      | 库存更新后     | 库存 >0 → 0 时插入**售罄紧急预警** |
| `monitor_machine_fault`    | 机器状态更新后 | 状态变为 fault 时插入**故障预警**  |
| `after_transaction_insert` | 交易记录插入后 | **自动扣减库存 -1**                |
| `after_restock_insert`     | 补货记录插入后 | **自动增加库存**（不超最大容量）   |

### 触发器工作流程
```
用户购买 → 插入 log_transaction → 触发器扣库存 → 触发预警检查 → 写入 log_alert
```

---

## API 接口

### RESTful API 端点

| 模块   | 端点                 | 方法                     |
| ------ | -------------------- | ------------------------ |
| 机器   | `/api/machines/`     | GET, POST, PUT, DELETE   |
| 商品   | `/api/products/`     | GET, POST, PUT, DELETE   |
| 库存   | `/api/inventories/`  | GET, POST, PUT, DELETE   |
| 交易   | `/api/transactions/` | GET, POST, DELETE (退货) |
| 补货   | `/api/restocks/`     | GET, POST, DELETE        |
| 用户   | `/api/app-users/`    | GET, POST, PUT, DELETE   |
| 供应商 | `/api/suppliers/`    | GET, POST, PUT, DELETE   |
| 运维   | `/api/sys-staffs/`   | GET, POST, PUT, DELETE   |
| 预警   | `/api/alerts/`       | GET                      |
| 日结   | `/api/stat-daily/`   | GET                      |

### 财务统计 API

```
GET  /api/stat-daily/summary/?period=week|month|today|all
POST /api/stat-daily/generate/  # 生成日结统计
GET  /api/transactions/statistics/?period=today|week|month
```

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
├── scripts/                # 初始化和测试脚本
│   ├── init_data.py        # 初始化测试数据
│   └── simulate_purchase.py # 模拟购买
└── frontend_new/           # React 前端
    ├── src/
    │   ├── pages/          # 页面组件
    │   ├── components/     # 公共组件
    │   └── api/            # API 配置
    └── package.json
```

---

## 验证触发器

运行模拟购买脚本：
```bash
python scripts/simulate_purchase.py
```

查看 `log_alert` 表，当库存 ≥5→<5 或 >0→0 时会自动新增预警记录。

---

## 注意事项

1. **必须使用 MySQL 8.0+**：SQLite 不支持触发器语法
2. **时区设置**：`settings.py` 中 `USE_TZ = True` 使用 UTC 时间存储
3. **CORS 配置**：已配置 `django-cors-headers` 允许前端跨域访问
4. **并发安全**：使用 `select_for_update()` 行级锁防止超卖

---

## 作者

Vending System ©2025
