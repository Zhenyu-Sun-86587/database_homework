import React, { useEffect, useState } from 'react';
import { Table, message, Tag } from 'antd';
import api, { endpoints } from '../api/api';

interface Transaction {
    id: number;
    user: number;
    machine: number;
    product: number;
    amount: string;
    created_at: string;
}

const Transactions: React.FC = () => {
    const [transactions, setTransactions] = useState<Transaction[]>([]);
    const [loading, setLoading] = useState(false);

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

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
        { title: '用户ID', dataIndex: 'user', key: 'user' },
        { title: '机器ID', dataIndex: 'machine', key: 'machine' },
        { title: '商品ID', dataIndex: 'product', key: 'product' },
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
            <h1 className="text-2xl font-bold mb-4">交易记录</h1>
            <Table
                columns={columns}
                dataSource={transactions}
                rowKey="id"
                loading={loading}
                pagination={{ pageSize: 10 }}
            />
        </div>
    );
};

export default Transactions;
