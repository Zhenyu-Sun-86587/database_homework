import React, { useEffect, useState, useMemo } from 'react';
import { Table, Button, Space, Modal, Form, Input, Select, message, Tag } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Machine {
    id: number;
    machine_code: string;
    location: string;
    status: 'normal' | 'fault';
    region_code: string;
    created_at: string;
}

const Machines: React.FC = () => {
    const [machines, setMachines] = useState<Machine[]>([]);
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();
    const [editingId, setEditingId] = useState<number | null>(null);
    const [searchText, setSearchText] = useState('');

    const fetchMachines = async () => {
        setLoading(true);
        try {
            const res = await api.get(endpoints.machines);
            setMachines(res.data);
        } catch (error) {
            message.error('获取机器列表失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMachines();
    }, []);

    const filteredMachines = useMemo(() => {
        if (!searchText.trim()) return machines;
        const lower = searchText.toLowerCase();
        return machines.filter(m =>
            m.machine_code.toLowerCase().includes(lower) ||
            m.location.toLowerCase().includes(lower) ||
            m.region_code.toLowerCase().includes(lower)
        );
    }, [machines, searchText]);

    const handleOk = async () => {
        try {
            const values = await form.validateFields();
            if (editingId) {
                await api.put(`${endpoints.machines}${editingId}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.machines, values);
                message.success('创建成功');
            }
            setIsModalOpen(false);
            form.resetFields();
            setEditingId(null);
            fetchMachines();
        } catch (error) {
            message.error('操作失败');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.machines}${id}/`);
            message.success('删除成功');
            fetchMachines();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const openEdit = (record: Machine) => {
        setEditingId(record.id);
        form.setFieldsValue(record);
        setIsModalOpen(true);
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: '机器编号', dataIndex: 'machine_code', key: 'machine_code' },
        { title: '位置', dataIndex: 'location', key: 'location' },
        {
            title: '状态',
            dataIndex: 'status',
            key: 'status',
            render: (status: string) => (
                <Tag color={status === 'normal' ? 'green' : 'red'}>
                    {status === 'normal' ? '正常' : '故障'}
                </Tag>
            )
        },
        { title: '区域代码', dataIndex: 'region_code', key: 'region_code' },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: Machine) => (
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
                <h1 className="text-2xl font-bold">机器管理</h1>
                <Space>
                    <Input
                        placeholder="搜索编号/位置/区域"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 200 }}
                        allowClear
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => {
                        setEditingId(null);
                        form.resetFields();
                        setIsModalOpen(true);
                    }}>
                        新增机器
                    </Button>
                </Space>
            </div>
            <Table columns={columns} dataSource={filteredMachines} rowKey="id" loading={loading} />


            <Modal title={editingId ? "编辑机器" : "新增机器"} open={isModalOpen} onOk={handleOk} onCancel={() => setIsModalOpen(false)}>
                <Form form={form} layout="vertical">
                    <Form.Item name="machine_code" label="机器编号" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="location" label="位置" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="status" label="状态" initialValue="normal">
                        <Select>
                            <Select.Option value="normal">正常</Select.Option>
                            <Select.Option value="fault">故障</Select.Option>
                        </Select>
                    </Form.Item>
                    <Form.Item name="region_code" label="区域代码" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Machines;
