import React, { useEffect, useState, useMemo } from 'react';
import { Table, Button, Modal, Form, InputNumber, Select, message, Space, Input } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Restock {
    id: number;
    staff: number;
    staff_name?: string;
    machine: number;
    machine_code?: string;
    product: number;
    product_name?: string;
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
    const [searchText, setSearchText] = useState('');

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

    const filteredRestocks = useMemo(() => {
        if (!searchText.trim()) return restocks;
        const lower = searchText.toLowerCase();
        return restocks.filter(r =>
            String(r.staff).includes(lower) ||
            String(r.machine).includes(lower) ||
            String(r.product).includes(lower) ||
            r.staff_name?.toLowerCase().includes(lower) ||
            r.machine_code?.toLowerCase().includes(lower) ||
            r.product_name?.toLowerCase().includes(lower)
        );
    }, [restocks, searchText]);

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
        { title: '运维人员', dataIndex: 'staff_name', key: 'staff_name', render: (text: string, record: Restock) => text || `人员${record.staff}` },
        { title: '机器', dataIndex: 'machine_code', key: 'machine_code', render: (text: string, record: Restock) => text || `机器${record.machine}` },
        { title: '商品', dataIndex: 'product_name', key: 'product_name', render: (text: string, record: Restock) => text || `商品${record.product}` },
        { title: '数量', dataIndex: 'quantity', key: 'quantity' },
        { title: '补货时间', dataIndex: 'created_at', key: 'created_at', render: (text: string) => new Date(text).toLocaleString() },
    ];

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-2xl font-bold">补货记录</h1>
                <Space>
                    <Input
                        placeholder="搜索人员/机器/商品"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 200 }}
                        allowClear
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增补货</Button>
                </Space>
            </div>
            <Table columns={columns} dataSource={filteredRestocks} rowKey="id" loading={loading} />


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
