### 1\. 项目背景 (Background)

针对校园自动贩卖机人工巡检效率低、缺货响应慢的问题，设计一套**全链路管理系统**。

  * **核心痛点**：不知道哪台机器缺货、补货记录混乱、销售数据不透明。
  * **解决方案**：利用**数据库触发器**实现毫秒级库存预警，结合运维人员管理，打通“销售-监控-补货-统计”闭环。

### 2\. 技术栈 (Tech Stack)

  * **语言框架**：Python 3.9 + Django 4.2 (LTS)
  * **数据库**：MySQL 8.0 (必须 8.0+ 以支持高级触发器)
  * **前端展示**：Django Admin (自带后台) + Bootstrap 5 (简单大屏)

### 3\. 数据库表结构 (11张表)

我将表分为三类，你可以直接复制这个结构给 AI 工具生成代码。

#### A. 基础与资源 (Base & Resources)

1.  **`sys_admin`** (管理员): ID, 用户名, 密码, 权限
2.  **`sys_staff`** (运维人员): 工号, 姓名, 电话, **负责区域** (Region\_Code)
3.  **`app_user`** (学生用户): ID, 用户名, **余额**
4.  **`biz_supplier`** (供应商): ID, 名称, 联系方式
5.  **`biz_machine`** (贩卖机): 机器编号, 位置, **状态** (正常/故障), 所属区域
6.  **`biz_product`** (商品): ID, 名称, **进价**, **售价**, 所属供应商ID

#### B. 核心业务 (Core Business)

7.  **`biz_inventory` (库存表 - 核心)**:

      * 字段: ID, **机器ID**, **商品ID**, **当前库存**, 最大容量
      * *逻辑*: 机器与商品的多对多关系，**触发器监控对象**。

8.  **`log_transaction` (交易流水)**:

      * 字段: 流水号, 用户ID, 机器ID, 商品ID, 成交金额, 时间

9.  **`log_restock` (补货记录)**:

      * 字段: 记录号, **运维人员ID**, 机器ID, 商品ID, 补货数量, 时间

#### C. 监控与统计 (Monitor & Stats)

10. **`log_alert` (报警日志 - 系统自动生成)**:

      * 字段: ID, 机器ID, 类型(缺货/故障), 报警内容, 时间
      * *逻辑*: **完全由数据库 Trigger 写入，无需 Python 写入**。

11. **`stat_daily` (日结统计)**:

      * 字段: ID, 日期, 机器ID, 总营收, 订单数, 报警次数

-----

### 4\. 执行步骤 (TODO List)

请按照以下顺序操作，每一步都可以直接发给 AI (如 ChatGPT/Cursor) 执行：

#### 步骤 1：初始化项目与模型 (Setup)

  * **指令**：创建 Django 项目 `vending_system`。创建 4 个 app：`users`, `resources`, `inventory`, `monitor`。
  * **动作**：将上面 **“3. 数据库表结构”** 中的 11 张表定义写入对应的 `models.py`。
  * **关键点**：确保 `Inventory` 表中 `machine` 和 `product` 是联合唯一索引 (`unique_together`)。

#### 步骤 2：植入核心触发器 (Inject Trigger)

这是拿分的关键，不要手动在 Navicat 里建，要写在代码里。

  * **指令**：创建一个空的 Django migration 文件。
  * **动作**：写入原生 SQL 触发器逻辑：
    ```sql
    CREATE TRIGGER monitor_low_stock AFTER UPDATE ON biz_inventory
    FOR EACH ROW
    BEGIN
        IF NEW.current_stock < 5 AND OLD.current_stock >= 5 THEN
            INSERT INTO log_alert (machine_id, message, created_at)
            VALUES (NEW.machine_id, CONCAT('缺货预警: ', NEW.product_id), NOW());
        END IF;
    END;
    ```
  * **执行**：`python manage.py migrate`

#### 步骤 3：生成管理后台与逻辑 (Logic & UI)

  * **指令**：在 `admin.py` 中注册所有模型，开启 Django Admin 后台。
  * **动作**：编写一个简单的 Python 脚本（或 Django View）模拟“购买”操作：
    1.  找到指定 Inventory 记录。
    2.  `current_stock` 减 1。
    3.  `item.save()`。
  * **验证**：运行脚本后，去数据库看 `log_alert` 表是否自动多了一条数据。
