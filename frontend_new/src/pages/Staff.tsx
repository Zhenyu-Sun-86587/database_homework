import React, { useEffect, useState, useMemo } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api, { endpoints } from '../api/api';

interface Staff {
    id: number;
    staff_id: string;
    name: string;
    phone: string;
    region_code: string;
    created_at: string;
}

const Staff: React.FC = () => {
    const [staffs, setStaffs] = useState<Staff[]>([]);
    const [loading, setLoading] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingStaff, setEditingStaff] = useState<Staff | null>(null);
    const [form] = Form.useForm();
    const [searchText, setSearchText] = useState('');

    const fetchStaffs = async () => {
        setLoading(true);
        try {
            const res = await api.get(endpoints.staffs);
            setStaffs(res.data);
        } catch (error) {
            message.error('获取运维人员列表失败');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStaffs();
    }, []);

    const filteredStaffs = useMemo(() => {
        if (!searchText.trim()) return staffs;
        const lower = searchText.toLowerCase();
        return staffs.filter(s =>
            s.staff_id.toLowerCase().includes(lower) ||
            s.name.toLowerCase().includes(lower) ||
            s.phone.includes(searchText) ||
            s.region_code.toLowerCase().includes(lower)
        );
    }, [staffs, searchText]);

    const handleAdd = () => {
        setEditingStaff(null);
        form.resetFields();
        setModalVisible(true);
    };

    const handleEdit = (staff: Staff) => {
        setEditingStaff(staff);
        form.setFieldsValue(staff);
        setModalVisible(true);
    };

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`${endpoints.staffs}${id}/`);
            message.success('删除成功');
            fetchStaffs();
        } catch (error) {
            message.error('删除失败');
        }
    };

    const handleSubmit = async (values: any) => {
        try {
            if (editingStaff) {
                await api.put(`${endpoints.staffs}${editingStaff.id}/`, values);
                message.success('更新成功');
            } else {
                await api.post(endpoints.staffs, values);
                message.success('创建成功');
            }
            setModalVisible(false);
            fetchStaffs();
        } catch (error) {
            message.error('操作失败');
        }
    };

    const columns = [
        { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
        { title: '工号', dataIndex: 'staff_id', key: 'staff_id' },
        { title: '姓名', dataIndex: 'name', key: 'name' },
        { title: '电话', dataIndex: 'phone', key: 'phone' },
        { title: '负责区域', dataIndex: 'region_code', key: 'region_code' },
        {
            title: '操作',
            key: 'action',
            render: (_: any, record: Staff) => (
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
                <h1 className="text-2xl font-bold">运维人员管理</h1>
                <Space>
                    <Input
                        placeholder="搜索工号/姓名/电话/区域"
                        prefix={<SearchOutlined />}
                        value={searchText}
                        onChange={e => setSearchText(e.target.value)}
                        style={{ width: 220 }}
                        allowClear
                    />
                    <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>添加人员</Button>
                </Space>
            </div>
            <Table columns={columns} dataSource={filteredStaffs} rowKey="id" loading={loading} />


            <Modal
                title={editingStaff ? '编辑人员' : '添加人员'}
                open={modalVisible}
                onCancel={() => setModalVisible(false)}
                onOk={() => form.submit()}
            >
                <Form form={form} layout="vertical" onFinish={handleSubmit}>
                    <Form.Item name="staff_id" label="工号" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="name" label="姓名" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="phone" label="电话" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="region_code" label="负责区域" rules={[{ required: true }]}>
                        <Input />
                    </Form.Item>
                </Form>
            </Modal>
        </div>
    );
};

export default Staff;
