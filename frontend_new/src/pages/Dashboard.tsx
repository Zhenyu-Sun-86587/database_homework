import React, { useEffect, useState } from 'react';
import { Card, Col, Row, Statistic, Spin } from 'antd';
import { ArrowUpOutlined, WarningOutlined, DesktopOutlined, ShoppingCartOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface DashboardStats {
    totalMachines: number;
    activeMachines: number;
    todayRevenue: number;
    lowStockCount: number;
    totalProducts: number;
    totalUsers: number;
}

const Dashboard: React.FC = () => {
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState<DashboardStats>({
        totalMachines: 0,
        activeMachines: 0,
        todayRevenue: 0,
        lowStockCount: 0,
        totalProducts: 0,
        totalUsers: 0,
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const [machinesRes, productsRes, usersRes, inventoriesRes, transactionsRes] = await Promise.all([
                    api.get(endpoints.machines),
                    api.get(endpoints.products),
                    api.get(endpoints.users),
                    api.get(endpoints.inventories),
                    api.get(endpoints.transactions),
                ]);

                const machines = machinesRes.data;
                const products = productsRes.data;
                const users = usersRes.data;
                const inventories = inventoriesRes.data;
                const transactions = transactionsRes.data;

                // 计算活跃机器（状态为normal的）
                const activeMachines = machines.filter((m: any) => m.status === 'normal').length;

                // 计算今日营收
                const today = new Date().toISOString().split('T')[0];
                const todayTransactions = transactions.filter((t: any) =>
                    t.created_at && t.created_at.startsWith(today)
                );
                const todayRevenue = todayTransactions.reduce((sum: number, t: any) =>
                    sum + parseFloat(t.amount || 0), 0
                );

                // 计算低库存警报（库存小于5的商品数量）
                const lowStockCount = inventories.filter((inv: any) => inv.current_stock < 5).length;

                setStats({
                    totalMachines: machines.length,
                    activeMachines,
                    todayRevenue,
                    lowStockCount,
                    totalProducts: products.length,
                    totalUsers: users.length,
                });
            } catch (error) {
                console.error('Failed to fetch dashboard stats', error);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <Spin size="large" />
            </div>
        );
    }

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">系统概览</h1>
            <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} lg={6}>
                    <Card bordered={false}>
                        <Statistic
                            title="今日销售额"
                            value={stats.todayRevenue}
                            precision={2}
                            valueStyle={{ color: '#3f8600' }}
                            prefix={<ArrowUpOutlined />}
                            suffix="CNY"
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card bordered={false}>
                        <Statistic
                            title="活跃机器"
                            value={stats.activeMachines}
                            valueStyle={{ color: stats.activeMachines < stats.totalMachines ? '#cf1322' : '#3f8600' }}
                            prefix={<DesktopOutlined />}
                            suffix={`/ ${stats.totalMachines}`}
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card bordered={false}>
                        <Statistic
                            title="库存预警"
                            value={stats.lowStockCount}
                            valueStyle={{ color: stats.lowStockCount > 0 ? '#faad14' : '#3f8600' }}
                            prefix={<WarningOutlined />}
                            suffix="项"
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card bordered={false}>
                        <Statistic
                            title="商品种类"
                            value={stats.totalProducts}
                            valueStyle={{ color: '#1890ff' }}
                            prefix={<ShoppingCartOutlined />}
                            suffix="种"
                        />
                    </Card>
                </Col>
            </Row>

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">欢迎使用智能贩卖机管理系统</h2>
                <p className="text-gray-600">
                    请从左侧菜单选择功能进行操作。
                    <br />
                    本系统支持机器管理、商品管理、库存监控以及手机端购买演示。
                </p>
            </div>
        </div>
    );
};

export default Dashboard;
