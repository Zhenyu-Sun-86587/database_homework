import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Supplier {
    id: number;
    name: string;
    contact: string;
    created_at: string;
}

const Suppliers: React.FC = () => {
    const [suppliers, setSuppliers] = useState<Supplier[]>([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);
    const [form] = Form.useForm();

    const fetchSuppliers = async () => {
        setLoading(true);
        try {
            const res = await api.get(endpoints.suppliers);
            setSuppliers(res.data);
        } catch (error) {
            message.error('获取供应商列表失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSuppliers();
    }, []);

    const handleAdd = () => {
        setEditingSupplier(null);
        form.resetFields();
        setModalVisible(true);
    };

    const handleEdit = (supplier: Supplier) => {
        setEditingSupplier(supplier);
        form.setFieldsValue(supplier);
        setModalVisible(true);
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.suppliers}${id}/`);
            message.success('删除成功');
            fetchSuppliers();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const handleSubmit = async (values: any) => {
        try {
            if (editingSupplier) {
                await api.put(`${endpoints.suppliers}${editingSupplier.id}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.suppliers, values);
                message.success('创建成功');
            }
            setModalVisible(false);
            fetchSuppliers();
        } catch (error) {
            message.error('操作失败');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
        { title: '名称', dataIndex: 'name', key: 'name' },
        { title: '联系方式', dataIndex: 'contact', key: 'contact' },
        { title: '创建时间', dataIndex: 'created_at', key: 'created_at', render: (text: string) => new Date(text).toLocaleString() },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: Supplier) => (
                <Space>
                    <Button icon={<EditOutlined />} onClick={() => handleEdit(record)}>编辑</Button>
                    <Popconfirm title="确定删除?" onConfirm={() => handleDelete(record.id)}>
                        <Button danger icon={<DeleteOutlined />}>删除</Button>
                    </Popconfirm>
                </Space>
            ),
        },
    ];

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">供应商管理</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>添加供应商</Button>
            </div>
            <Table columns={columns} dataSource={suppliers} rowKey="id" loading={loading} />

            <Modal
                title={editingSupplier ? '编辑供应商' : '添加供应商'}
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                onOk={() => form.submit()}
            >
                <Form form={form} layout="vertical" onFinish={handleSubmit}>
                    <Form.Item name="name" label="名称" rules={[{ required: true, message: '请输入名称' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="contact" label="联系方式" rules={[{ required: true, message: '请输入联系方式' }]}>
                        <Input />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Suppliers;
