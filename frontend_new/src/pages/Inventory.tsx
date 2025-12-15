import React, { useEffect, useState } from 'react';
import { Table, Button, Space, Modal, Form, InputNumber, Select, message, Progress } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface InventoryItem {
    id: number;
    machine: number;
    machine_code: string;
    product: number;
    product_name: string;
    current_stock: number;
    max_capacity: number;
}

interface Machine {
    id: number;
    machine_code: string;
}

interface Product {
    id: number;
    name: string;
}

const Inventory: React.FC = () => {
    const [inventory, setInventory] = useState<InventoryItem[]>([]);
    const [machines, setMachines] = useState<Machine[]>([]);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();
    const [editingId, setEditingId] = useState<number | null>(null);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [invRes, machRes, prodRes] = await Promise.all([
                api.get(endpoints.inventories),
                api.get(endpoints.machines),
                api.get(endpoints.products)
            ]);
            setInventory(invRes.data);
            setMachines(machRes.data);
            setProducts(prodRes.data);
        } catch (error) {
            message.error('获取数据失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleOk = async () => {
        try {
            const values = await form.validateFields();
            if (editingId) {
                await api.put(`${endpoints.inventories}${editingId}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.inventories, values);
                message.success('创建成功');
            }
            setIsModalOpen(false);
            form.resetFields();
            setEditingId(null);
            fetchData();
        } catch (error) {
            message.error('操作失败，可能该机器已存在该商品库存');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.inventories}${id}/`);
            message.success('删除成功');
            fetchData();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const openEdit = (record: InventoryItem) => {
        setEditingId(record.id);
        form.setFieldsValue(record);
        setIsModalOpen(true);
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: '机器', dataIndex: 'machine_code', key: 'machine_code' },
        { title: '商品', dataIndex: 'product_name', key: 'product_name' },
        {
            title: '当前库存',
            dataIndex: 'current_stock',
            key: 'current_stock',
            render: (text: number, record: InventoryItem) => (
                <div style={{ width: 150 }}>
                    <Progress
                        percent={Math.round((text / record.max_capacity) * 100)}
                        size="small"
                        status={text < 5 ? 'exception' : 'active'}
                        format={() => `${text} / ${record.max_capacity}`}
                    />
                </div>
            )
        },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: InventoryItem) => (
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
                <h1 className="text-2xl font-bold">库存管理</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={() => {
                    setEditingId(null);
                    form.resetFields();
                    setIsModalOpen(true);
                }}>
                    新增库存记录
                </Button>
            </div>
            <Table columns={columns} dataSource={inventory} rowKey="id" loading={loading} />

            <Modal title={editingId ? "编辑库存" : "新增库存"} open={isModalOpen} onOk={handleOk} onCancel={() => setIsModalOpen(false)}>
                <Form form={form} layout="vertical">
                    <Form.Item name="machine" label="机器" rules={[{ required: true }]}>
                        <Select disabled={!!editingId}>
                            {machines.map(m => (
                                <Select.Option key={m.id} value={m.id}>{m.machine_code}</Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item name="product" label="商品" rules={[{ required: true }]}>
                        <Select disabled={!!editingId}>
                            {products.map(p => (
                                <Select.Option key={p.id} value={p.id}>{p.name}</Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                    <Form.Item name="current_stock" label="当前库存" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} min={0} />
                    </Form.Item>
                    <Form.Item name="max_capacity" label="最大容量" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} min={1} />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Inventory;
