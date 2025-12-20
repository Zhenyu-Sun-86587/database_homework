import React, { useEffect, useState, useMemo } from 'react';
import { Table, Button, Space, Modal, Form, Input, InputNumber, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface AppUser {
    id: number;
    username: string;
    balance: string;
    created_at: string;
}

const Users: React.FC = () => {
    const [users, setUsers] = useState<AppUser[]>([]);
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();
    const [editingId, setEditingId] = useState<number | null>(null);
    const [searchText, setSearchText] = useState('');

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const res = await api.get(endpoints.users);
            setUsers(res.data);
        } catch (error) {
            message.error('获取用户列表失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    const filteredUsers = useMemo(() => {
        if (!searchText.trim()) return users;
        const lower = searchText.toLowerCase();
        return users.filter(u => u.username.toLowerCase().includes(lower));
    }, [users, searchText]);

    const handleOk = async () => {
        try {
            const values = await form.validateFields();
            if (editingId) {
                await api.put(`${endpoints.users}${editingId}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.users, values);
                message.success('创建成功');
            }
            setIsModalOpen(false);
            form.resetFields();
            setEditingId(null);
            fetchUsers();
        } catch (error) {
            message.error('操作失败');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.users}${id}/`);
            message.success('删除成功');
            fetchUsers();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const openEdit = (record: AppUser) => {
        setEditingId(record.id);
        form.setFieldsValue(record);
        setIsModalOpen(true);
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: '用户名', dataIndex: 'username', key: 'username' },
        { title: '余额', dataIndex: 'balance', key: 'balance' },
        { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: AppUser) => (
                <Space size="middle">
                    <Button icon={<EditOutlined />} onClick={() => openEdit(record)}>编辑</Button>
                    <Button danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>删除</Button>
                </Space>
            ),
        },
    ];

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">用户管理</h1>
                <Space>
                    <Input
                        placeholder="搜索用户名"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 180 }}
                        allowClear
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => {
                        setEditingId(null);
                        form.resetFields();
                        setIsModalOpen(true);
                    }}>
                        新增用户
                    </Button>
                </Space>
            </div>
            <Table columns={columns} dataSource={filteredUsers} rowKey="id" loading={loading} />


            <Modal title={editingId ? "编辑用户" : "新增用户"} open={isModalOpen} onOk={handleOk} onCancel={() => setIsModalOpen(false)}>
                <Form form={form} layout="vertical">
                    <Form.Item name="username" label="用户名" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="balance" label="余额" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} min={0} step={0.01} />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Users;
