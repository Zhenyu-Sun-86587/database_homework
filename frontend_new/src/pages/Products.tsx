import React, { useEffect, useState, useMemo } from 'react';
import { Table, Button, Space, Modal, Form, Input, InputNumber, Select, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Product {
    id: number;
    name: string;
    cost_price: string;
    sell_price: string;
    supplier: number;
    supplier_name: string;
}

interface Supplier {
    id: number;
    name: string;
}

const Products: React.FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [suppliers, setSuppliers] = useState<Supplier[]>([]);
    const [loading, setLoading] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();
    const [editingId, setEditingId] = useState<number | null>(null);
    const [searchText, setSearchText] = useState('');

    const fetchData = async () => {
        setLoading(true);
        try {
            const [prodRes, suppRes] = await Promise.all([
                api.get(endpoints.products),
                api.get(endpoints.suppliers)
            ]);
            setProducts(prodRes.data);
            setSuppliers(suppRes.data);
        } catch (error) {
            message.error('获取数据失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // 搜索过滤逻辑
    const filteredProducts = useMemo(() => {
        if (!searchText.trim()) return products;
        const lowerSearch = searchText.toLowerCase();
        return products.filter(p => 
            p.name.toLowerCase().includes(lowerSearch) ||
            p.supplier_name?.toLowerCase().includes(lowerSearch)
        );
    }, [products, searchText]);

    const handleOk = async () => {
        try {
            const values = await form.validateFields();
            if (editingId) {
                await api.put(`${endpoints.products}${editingId}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.products, values);
                message.success('创建成功');
            }
            setIsModalOpen(false);
            form.resetFields();
            setEditingId(null);
            fetchData();
        } catch (error) {
            message.error('操作失败');
        }
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.products}${id}/`);
            message.success('删除成功');
            fetchData();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const openEdit = (record: Product) => {
        setEditingId(record.id);
        form.setFieldsValue(record);
        setIsModalOpen(true);
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id' },
        { title: '商品名称', dataIndex: 'name', key: 'name' },
        { title: '进价', dataIndex: 'cost_price', key: 'cost_price' },
        { title: '售价', dataIndex: 'sell_price', key: 'sell_price' },
        { title: '供应商', dataIndex: 'supplier_name', key: 'supplier_name' },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: Product) => (
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
                <h1 className="text-2xl font-bold">商品管理</h1>
                <Space>
                    <Input
                        placeholder="搜索商品名称或供应商"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 240 }}
                        allowClear
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => {
                        setEditingId(null);
                        form.resetFields();
                        setIsModalOpen(true);
                    }}>
                        新增商品
                    </Button>
                </Space>
            </div>
            <Table columns={columns} dataSource={filteredProducts} rowKey="id" loading={loading} />


            <Modal title={editingId ? "编辑商品" : "新增商品"} open={isModalOpen} onOk={handleOk} onCancel={() => setIsModalOpen(false)}>
                <Form form={form} layout="vertical">
                    <Form.Item name="name" label="商品名称" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="cost_price" label="进价" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} min={0} step={0.01} />
                    </Form.Item>
                    <Form.Item name="sell_price" label="售价" rules={[{ required: true }]}>
                        <InputNumber style={{ width: '100%' }} min={0} step={0.01} />
                    </Form.Item>
                    <Form.Item name="supplier" label="供应商" rules={[{ required: true }]}>
                        <Select>
                            {suppliers.map(s => (
                                <Select.Option key={s.id} value={s.id}>{s.name}</Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Products;
