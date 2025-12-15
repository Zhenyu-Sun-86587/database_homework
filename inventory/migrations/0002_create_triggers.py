from django.db import migrations


class Migration(migrations.Migration):
    """创建库存预警触发器"""

    dependencies = [
        ('inventory', '0001_initial'),
        ('monitor', '0001_initial'),
    ]

    operations = [
        # 库存更新后触发 - 缺货预警（库存低于5时）
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER monitor_low_stock
            AFTER UPDATE ON biz_inventory
            FOR EACH ROW
            BEGIN
                IF NEW.current_stock < 5 AND OLD.current_stock >= 5 THEN
                    INSERT INTO log_alert (machine_id, alert_type, message, created_at)
                    VALUES (NEW.machine_id, 'low_stock',
                            CONCAT('缺货预警: 商品ID ', NEW.product_id, ' 库存仅剩 ', NEW.current_stock),
                            NOW());
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS monitor_low_stock;"
        ),

        # 库存为0时触发紧急预警
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER monitor_empty_stock
            AFTER UPDATE ON biz_inventory
            FOR EACH ROW
            BEGIN
                IF NEW.current_stock = 0 AND OLD.current_stock > 0 THEN
                    INSERT INTO log_alert (machine_id, alert_type, message, created_at)
                    VALUES (NEW.machine_id, 'low_stock',
                            CONCAT('紧急预警: 商品ID ', NEW.product_id, ' 已售罄!'),
                            NOW());
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS monitor_empty_stock;"
        ),

        # 机器状态变更触发故障预警
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER monitor_machine_fault
            AFTER UPDATE ON biz_machine
            FOR EACH ROW
            BEGIN
                IF NEW.status = 'fault' AND OLD.status = 'normal' THEN
                    INSERT INTO log_alert (machine_id, alert_type, message, created_at)
                    VALUES (NEW.id, 'fault',
                            CONCAT('故障预警: 机器 ', NEW.machine_code, ' 发生故障'),
                            NOW());
                END IF;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS monitor_machine_fault;"
        ),

        # 交易记录插入后自动扣减库存
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER after_transaction_insert
            AFTER INSERT ON log_transaction
            FOR EACH ROW
            BEGIN
                UPDATE biz_inventory
                SET current_stock = current_stock - 1
                WHERE machine_id = NEW.machine_id AND product_id = NEW.product_id;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS after_transaction_insert;"
        ),

        # 补货记录插入后自动增加库存
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER after_restock_insert
            AFTER INSERT ON log_restock
            FOR EACH ROW
            BEGIN
                UPDATE biz_inventory
                SET current_stock = LEAST(current_stock + NEW.quantity, max_capacity)
                WHERE machine_id = NEW.machine_id AND product_id = NEW.product_id;
            END;
            """,
            reverse_sql="DROP TRIGGER IF EXISTS after_restock_insert;"
        ),
    ]
