# 自动无人售货机数据库系统 - 后端

## 项目简介

本项目是为数据库课程设计的一个自动无人售货机系统的后端部分。它基于Python的Django框架构建，并采用了前后端分离的架构。后端负责处理所有业务逻辑、数据存储和API接口。

## 技术栈

*   **语言:** Python 3.x
*   **框架:** Django
*   **API框架:** Django REST Framework
*   **数据库:** MySQL

## 核心功能

*   **商品管理:**
    *   商品的添加、删除、修改和查询。
    *   商品分类管理。
*   **库存管理:**
    *   实时库存跟踪。
    *   库存预警提醒。
    *   补货记录。
*   **用户管理:**
    *   用户注册与登录。
    *   用户信息管理。
*   **交易系统:**
    *   创建订单与支付。
    *   交易记录查询与统计。
*   **售货机管理:**
    *   售货机状态监控。
    *   售货机位置信息。

## 本地开发

### 1. 克隆仓库

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. 环境设置

建议使用虚拟环境以隔离项目依赖。

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

*(注意: `requirements.txt` 文件需要您通过 `pip freeze > requirements.txt` 命令生成)*

### 4. 数据库迁移

```bash
python manage.py migrate
```

### 5. 运行开发服务器

```bash
python manage.py runserver
```

服务将在 `http://127.0.0.1:8000/` 启动。

## API 接口

(此处可以添加您的API文档链接或主要接口列表)

---
*这是一个数据库课程作业项目。*
