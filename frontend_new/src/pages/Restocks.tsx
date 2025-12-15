import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, InputNumber, Select, message } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Restock {
    id: number;
    staff: number;
    machine: number;
    product: number;
    quantity: number;
    created_at: string;
}

const Restocks: React.FC = () => {
    const [restocks, setRestocks] = useState<Restock[]>([]);
    const [staffs, setStaffs] = useState<any[]>([]);
    const [machines, setMachines] = useState<any[]>([]);
    const [products, setProducts] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [form] = Form.useForm();

    const fetchData = async () => {
        setLoading(true);
        try {
            const [restockRes, staffRes, machineRes, productRes] = await Promise.all([
                api.get(endpoints.restocks),
                api.get(endpoints.staffs),
                api.get(endpoints.machines),
                api.get(endpoints.products),
            ]);
            setRestocks(restockRes.data);
            setStaffs(staffRes.data);
            setMachines(machineRes.data);
            setProducts(productRes.data);
        } catch (error) {
            message.error('获取数据失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleAdd = () => {
        form.resetFields();
        setModalVisible(true);
    };

    const handleSubmit = async (values: any) => {
        try {
            await api.post(endpoints.restocks, values);
            message.success('补货记录创建成功');
            setModalVisible(false);
            fetchData();
        } catch (error) {
            message.error('创建失败');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
        { title: '运维人员ID', dataIndex: 'staff', key: 'staff' },
        { title: '机器ID', dataIndex: 'machine', key: 'machine' },
        { title: '商品ID', dataIndex: 'product', key: 'product' },
        { title: '数量', dataIndex: 'quantity', key: 'quantity' },
        { title: '补货时间', dataIndex: 'created_at', key: 'created_at', render: (text: string) => new Date(text).toLocaleString() },
    ];

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">补货记录</h1>
                <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增补货</Button>
            </div>
            <Table columns={columns} dataSource={restocks} rowKey="id" loading={loading} />

            <Modal
                title="新增补货"
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                onOk={() => form.submit()}
            >
                <Form form={form} layout="vertical" onFinish={handleSubmit}>
                    <Form.Item name="staff" label="运维人员" rules={[{ required: true }]}>
                        <Select options={staffs.map(s => ({ label: s.name, value: s.id }))} />
                    </Form.Item>
                    <Form.Item name="machine" label="机器" rules={[{ required: true }]}>
                        <Select options={machines.map(m => ({ label: `${m.machine_code} - ${m.location}`, value: m.id }))} />
                    </Form.Item>
                    <Form.Item name="product" label="商品" rules={[{ required: true }]}>
                        <Select options={products.map(p => ({ label: p.name, value: p.id }))} />
                    </Form.Item>
                    <Form.Item name="quantity" label="数量" rules={[{ required: true }]}>
                        <InputNumber min={1} style={{ width: '100%' }} />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Restocks;
