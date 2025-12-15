import React from 'react';
import { Layout, Menu, theme } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
    DesktopOutlined,
    PieChartOutlined,
    UserOutlined,
    ShoppingOutlined,
    DatabaseOutlined,
    MobileOutlined,
    ShopOutlined,
    TransactionOutlined,
    ReloadOutlined,
    TeamOutlined
} from '@ant-design/icons';

const { Header, Content, Footer, Sider } = Layout;

const MainLayout: React.FC = () => {
    const {
        token: { colorBgContainer, borderRadiusLG },
    } = theme.useToken();
    const navigate = useNavigate();
    const location = useLocation();

    const items = [
        { key: '/', icon: <PieChartOutlined />, label: '仪表盘' },
        { key: '/machines', icon: <DesktopOutlined />, label: '机器管理' },
        { key: '/products', icon: <ShoppingOutlined />, label: '商品管理' },
        { key: '/inventory', icon: <DatabaseOutlined />, label: '库存管理' },
        { key: '/users', icon: <UserOutlined />, label: '用户管理' },
        { key: '/suppliers', icon: <ShopOutlined />, label: '供应商管理' },
        { key: '/transactions', icon: <TransactionOutlined />, label: '交易记录' },
        { key: '/restocks', icon: <ReloadOutlined />, label: '补货记录' },
        { key: '/staff', icon: <TeamOutlined />, label: '运维人员' },
        { key: '/mobile', icon: <MobileOutlined />, label: '手机端购买演示' },
    ];

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider collapsible breakpoint="lg">
                <div className="demo-logo-vertical" style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)', borderRadius: 6 }} />
                <Menu
                    theme="dark"
                    defaultSelectedKeys={['/']}
                    selectedKeys={[location.pathname]}
                    mode="inline"
                    items={items}
                    onClick={({ key }) => navigate(key)}
                />
            </Sider>
            <Layout>
                <Header style={{ padding: 0, background: colorBgContainer }} />
                <Content style={{ margin: '0 16px' }}>
                    <div
                        style={{
                            padding: 24,
                            minHeight: 360,
                            background: colorBgContainer,
                            borderRadius: borderRadiusLG,
                            marginTop: 16,
                        }}
                    >
                        <Outlet />
                    </div>
                </Content>
                <Footer style={{ textAlign: 'center' }}>
                    Vending System ©{new Date().getFullYear()} Created by Antigravity
                </Footer>
            </Layout>
        </Layout>
    );
};

export default MainLayout;
