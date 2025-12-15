import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table, Select, Button, message, Spin, DatePicker } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, DollarOutlined, ShoppingCartOutlined, BarChartOutlined, SyncOutlined } from '@ant-design/icons';
import api from '../api/api';

interface StatsSummary {
    total_revenue: number;
    total_cost: number;
    total_profit: number;
    total_orders: number;
    total_alerts: number;
}

interface DailyStat {
    date: string;
    revenue: number;
    cost: number;
    profit: number;
    orders: number;
}

interface MachineRanking {
    machine__machine_code: string;
    revenue: number;
    profit: number;
    orders: number;
}

const Statistics: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [period, setPeriod] = useState<'week' | 'month'>('month');
    const [summary, setSummary] = useState<StatsSummary | null>(null);
    const [dailyStats, setDailyStats] = useState<DailyStat[]>([]);
    const [machineRanking, setMachineRanking] = useState<MachineRanking[]>([]);

    const fetchStats = async () => {
        setLoading(true);
        try {
            const res = await api.get(`stat-daily/summary/?period=${period}`);
            setSummary(res.data.summary);
            setDailyStats(res.data.daily_stats);
            setMachineRanking(res.data.machine_ranking);
        } catch (error) {
            message.error('获取统计数据失败');
        } finally {
            setLoading(false);
        }
    };

    const generateDailyStats = async (date?: string) => {
        setGenerating(true);
        try {
            const body = date ? { date } : {};
            await api.post('stat-daily/generate/', body);
            message.success('日结统计生成成功');
            fetchStats();
        } catch (error) {
            message.error('生成日结统计失败');
        } finally {
            setGenerating(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, [period]);

    const dailyColumns = [
        { title: '日期', dataIndex: 'date', key: 'date' },
        {
            title: '营收',
            dataIndex: 'revenue',
            key: 'revenue',
            render: (val: number) => <span style={{ color: '#3f8600', fontWeight: 600 }}>¥{val?.toFixed(2)}</span>
        },
        {
            title: '成本',
            dataIndex: 'cost',
            key: 'cost',
            render: (val: number) => <span style={{ color: '#cf1322' }}>¥{val?.toFixed(2)}</span>
        },
        {
            title: '利润',
            dataIndex: 'profit',
            key: 'profit',
            render: (val: number) => (
                <span style={{ color: val >= 0 ? '#1890ff' : '#cf1322', fontWeight: 'bold' }}>
                    ¥{val?.toFixed(2)}
                </span>
            )
        },
        { title: '订单数', dataIndex: 'orders', key: 'orders' },
    ];

    const machineColumns = [
        { title: '机器编号', dataIndex: 'machine__machine_code', key: 'machine' },
        {
            title: '营收',
            dataIndex: 'revenue',
            key: 'revenue',
            render: (val: number) => <span style={{ color: '#3f8600', fontWeight: 600 }}>¥{val?.toFixed(2)}</span>
        },
        {
            title: '利润',
            dataIndex: 'profit',
            key: 'profit',
            render: (val: number) => <span style={{ color: '#1890ff', fontWeight: 'bold' }}>¥{val?.toFixed(2)}</span>
        },
        { title: '订单数', dataIndex: 'orders', key: 'orders' },
    ];

    if (loading && !summary) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 256 }}>
                <Spin size="large" />
            </div>
        );
    }

    return (
        <div style={{ padding: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
                <h1 style={{ fontSize: 24, fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 8, margin: 0 }}>
                    <BarChartOutlined />
                    财务统计
                </h1>
                <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                    <Select
                        value={period}
                        onChange={(val) => setPeriod(val)}
                        style={{ width: 120 }}
                        options={[
                            { label: '近7天', value: 'week' },
                            { label: '近30天', value: 'month' },
                        ]}
                    />
                    <DatePicker
                        placeholder="选择日期生成日结"
                        onChange={(date) => {
                            if (date) {
                                generateDailyStats(date.format('YYYY-MM-DD'));
                            }
                        }}
                    />
                    <Button
                        type="primary"
                        icon={<SyncOutlined spin={generating} />}
                        loading={generating}
                        onClick={() => generateDailyStats()}
                    >
                        生成今日日结
                    </Button>
                </div>
            </div>

            {/* 汇总卡片 */}
            <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Statistic
                            title="总营收"
                            value={summary?.total_revenue || 0}
                            precision={2}
                            valueStyle={{ color: '#3f8600' }}
                            prefix={<DollarOutlined />}
                            suffix="CNY"
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Statistic
                            title="总成本"
                            value={summary?.total_cost || 0}
                            precision={2}
                            valueStyle={{ color: '#cf1322' }}
                            prefix={<ArrowDownOutlined />}
                            suffix="CNY"
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Statistic
                            title="总利润"
                            value={summary?.total_profit || 0}
                            precision={2}
                            valueStyle={{ color: (summary?.total_profit || 0) >= 0 ? '#1890ff' : '#cf1322' }}
                            prefix={<ArrowUpOutlined />}
                            suffix="CNY"
                        />
                    </Card>
                </Col>
                <Col xs={24} sm={12} lg={6}>
                    <Card>
                        <Statistic
                            title="总订单"
                            value={summary?.total_orders || 0}
                            valueStyle={{ color: '#722ed1' }}
                            prefix={<ShoppingCartOutlined />}
                            suffix="笔"
                        />
                    </Card>
                </Col>
            </Row>

            {/* 每日统计表格 */}
            <Row gutter={[16, 16]}>
                <Col xs={24} lg={14}>
                    <Card title="每日统计" style={{ marginBottom: 16 }}>
                        <Table
                            columns={dailyColumns}
                            dataSource={dailyStats}
                            rowKey="date"
                            pagination={false}
                            size="small"
                            loading={loading}
                        />
                    </Card>
                </Col>
                <Col xs={24} lg={10}>
                    <Card title="机器营收排名" style={{ marginBottom: 16 }}>
                        <Table
                            columns={machineColumns}
                            dataSource={machineRanking}
                            rowKey="machine__machine_code"
                            pagination={false}
                            size="small"
                            loading={loading}
                        />
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Statistics;
