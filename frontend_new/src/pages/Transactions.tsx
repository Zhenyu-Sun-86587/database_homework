import React, { useEffect, useState, useMemo } from 'react';
import { Table, message, Tag, DatePicker, Space, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';
import dayjs, { Dayjs } from 'dayjs';

const { RangePicker } = DatePicker;

interface Transaction {
    id: number;
    user: number;
    user_name?: string;
    machine: number;
    machine_code?: string;
    product: number;
    product_name?: string;
    amount: string;
    created_at: string;
}

const Transactions: React.FC = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(false);
    const [dateRange, setDateRange] = useState<[Dayjs | null, Dayjs | null]>([null, null]);
    const [searchText, setSearchText] = useState('');

    useEffect(() => {
        const fetchTransactions = async () => {
            setLoading(true);
            try {
                const res = await api.get(endpoints.transactions);
                setTransactions(res.data);
            } catch (error) {
                message.error('获取交易记录失败');
            } finally {
                setLoading(false);
            }
        };
        fetchTransactions();
    }, []);

    // 过滤逻辑：按日期范围和关键词
    const filteredTransactions = useMemo(() => {
        let result = transactions;

        // 日期范围过滤
        if (dateRange[0] && dateRange[1]) {
            const startDate = dateRange[0].startOf('day');
            const endDate = dateRange[1].endOf('day');
            result = result.filter(t => {
                const txDate = dayjs(t.created_at);
                return txDate.isAfter(startDate) && txDate.isBefore(endDate);
            });
        }

        // 关键词过滤
        if (searchText.trim()) {
            const lower = searchText.toLowerCase();
            result = result.filter(t =>
                String(t.user).includes(lower) ||
                String(t.machine).includes(lower) ||
                String(t.product).includes(lower) ||
                t.user_name?.toLowerCase().includes(lower) ||
                t.machine_code?.toLowerCase().includes(lower) ||
                t.product_name?.toLowerCase().includes(lower)
            );
        }

        return result;
    }, [transactions, dateRange, searchText]);

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
        { title: '用户', dataIndex: 'user_name', key: 'user_name', render: (text: string, record: Transaction) => text || `用户${record.user}` },
        { title: '机器', dataIndex: 'machine_code', key: 'machine_code', render: (text: string, record: Transaction) => text || `机器${record.machine}` },
        { title: '商品', dataIndex: 'product_name', key: 'product_name', render: (text: string, record: Transaction) => text || `商品${record.product}` },
        {
            title: '金额',
            dataIndex: 'amount',
            key: 'amount',
            render: (text: string) => <Tag color="green">¥{text}</Tag>
        },
        {
            title: '交易时间',
            dataIndex: 'created_at',
            key: 'created_at',
            render: (text: string) => new Date(text).toLocaleString()
        },
    ];

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">交易记录</h1>
                <Space>
                    <RangePicker
                        value={dateRange}
                        onChange={(dates) => setDateRange(dates as [Dayjs | null, Dayjs | null])}
                        placeholder={['开始日期', '结束日期']}
                    />
                    <Input
                        placeholder="搜索用户/机器/商品"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 200 }}
                        allowClear
                    />
                </Space>
            </div>
            <Table
                columns={columns}
                dataSource={filteredTransactions}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 10 }}
            />
        </div>
    );
};

export default Transactions;

