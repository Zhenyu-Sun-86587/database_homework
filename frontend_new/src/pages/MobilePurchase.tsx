import React, { useEffect, useState } from 'react';
import { Select, message, Spin, Card } from 'antd';
import { motion, AnimatePresence } from 'framer-motion';
import api, { endpoints } from '../api/api';
import { UserOutlined, WalletOutlined, ShoppingOutlined } from '@ant-design/icons';

interface Product {
    id: number;
    name: string;
    sell_price: string;
}

interface Machine {
    id: number;
    machine_code: string;
    location: string;
}

interface AppUser {
    id: number;
    username: string;
    balance: string;
}

interface InventoryItem {
    id: number;
    product: number;
    current_stock: number;
}

const MobilePurchase: React.FC = () => {
    const [machines, setMachines] = useState<Machine[]>([]);
    const [products, setProducts] = useState<Product[]>([]);
    const [inventory, setInventory] = useState<InventoryItem[]>([]);

    const [selectedMachineId, setSelectedMachineId] = useState<number | null>(null);
    const [currentUser, setCurrentUser] = useState<AppUser | null>(null);
    const [loading, setLoading] = useState(false);
    const [purchasing, setPurchasing] = useState(false);
    const [droppedProduct, setDroppedProduct] = useState<Product | null>(null);

    useEffect(() => {
        const initData = async () => {
            setLoading(true);
            try {
                const [machRes, prodRes, userRes] = await Promise.all([
                    api.get(endpoints.machines),
                    api.get(endpoints.products),
                    api.get(endpoints.users)
                ]);
                setMachines(machRes.data);
                setProducts(prodRes.data);

                if (machRes.data.length > 0) setSelectedMachineId(machRes.data[0].id);
                if (userRes.data.length > 0) setCurrentUser(userRes.data[0]);
            } catch (error) {
                message.error('初始化数据失败');
            } finally {
                setLoading(false);
            }
        };
        initData();
    }, []);

    useEffect(() => {
        if (selectedMachineId) {
            fetchInventory(selectedMachineId);
        }
    }, [selectedMachineId]);

    const fetchInventory = async (machineId: number) => {
        try {
            const res = await api.get(endpoints.inventories);
            const machineInventory = res.data.filter((item: any) => item.machine === machineId);
            setInventory(machineInventory);
        } catch (error) {
            console.error("Failed to fetch inventory", error);
        }
    };

    const handlePurchase = async (product: Product) => {
        if (!currentUser || !selectedMachineId) return;

        const stockItem = inventory.find(i => i.product === product.id);
        if (!stockItem || stockItem.current_stock <= 0) {
            message.error('该商品缺货');
            return;
        }

        setPurchasing(true);
        try {
            await api.post(endpoints.transactions, {
                user: currentUser.id,
                machine: selectedMachineId,
                product: product.id,
                amount: product.sell_price
            });

            // 刷新用户余额
            const userRes = await api.get(`${endpoints.users}${currentUser.id}/`);
            setCurrentUser(userRes.data);

            setDroppedProduct(product);

            setInventory(prev => prev.map(item =>
                item.product === product.id
                    ? { ...item, current_stock: item.current_stock - 1 }
                    : item
            ));

            message.success('购买成功！');

            setTimeout(() => {
                setDroppedProduct(null);
            }, 3000);

        } catch (error) {
            message.error('购买失败，可能是余额不足');
        } finally {
            setPurchasing(false);
        }
    };

    const getProductStock = (productId: number) => {
        const item = inventory.find(i => i.product === productId);
        return item ? item.current_stock : 0;
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen bg-gray-100">
                <Spin size="large" />
            </div>
        );
    }

    // 商品颜色
    const productColors = [
        { bg: '#ef4444', border: '#dc2626' }, // 红
        { bg: '#3b82f6', border: '#2563eb' }, // 蓝
        { bg: '#22c55e', border: '#16a34a' }, // 绿
        { bg: '#f97316', border: '#ea580c' }, // 橙
        { bg: '#8b5cf6', border: '#7c3aed' }, // 紫
        { bg: '#ec4899', border: '#db2777' }, // 粉
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
            {/* 顶部信息栏 */}
            <div className="max-w-4xl mx-auto mb-6">
                <Card className="shadow-lg">
                    <div className="flex justify-between items-center flex-wrap gap-4">
                        <div className="flex items-center gap-3">
                            <span className="text-gray-700 font-semibold">📍 当前设备:</span>
                            <Select
                                value={selectedMachineId}
                                onChange={setSelectedMachineId}
                                style={{ width: 240 }}
                                size="large"
                                options={machines.map(m => ({
                                    label: `${m.machine_code} - ${m.location}`,
                                    value: m.id
                                }))}
                            />
                        </div>
                        <div className="flex items-center gap-6">
                            <div className="flex items-center gap-2 text-gray-600">
                                <UserOutlined className="text-xl" />
                                <span className="font-medium text-lg">{currentUser?.username}</span>
                            </div>
                            <div className="flex items-center gap-2 bg-green-100 px-4 py-2 rounded-lg">
                                <WalletOutlined className="text-xl text-green-600" />
                                <span className="text-green-700 font-bold text-xl">¥{currentUser?.balance}</span>
                            </div>
                        </div>
                    </div>
                </Card>
            </div>

            {/* 商品展示区 */}
            <div className="max-w-4xl mx-auto">
                <Card
                    title={
                        <div className="flex items-center gap-2 text-xl">
                            <ShoppingOutlined />
                            <span>选择商品</span>
                        </div>
                    }
                    className="shadow-lg"
                >
                    {products.length === 0 ? (
                        <div className="text-center py-12 text-gray-500">
                            <p className="text-lg">暂无商品</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                            {products.map((product, index) => {
                                const stock = getProductStock(product.id);
                                const color = productColors[index % productColors.length];
                                const isOutOfStock = stock <= 0;

                                return (
                                    <motion.div
                                        key={product.id}
                                        whileHover={!isOutOfStock ? { scale: 1.05 } : {}}
                                        whileTap={!isOutOfStock ? { scale: 0.95 } : {}}
                                        className={`relative rounded-xl overflow-hidden cursor-pointer transition-shadow ${isOutOfStock
                                                ? 'opacity-50 cursor-not-allowed grayscale'
                                                : 'hover:shadow-xl'
                                            }`}
                                        onClick={() => !isOutOfStock && !purchasing && handlePurchase(product)}
                                        style={{
                                            backgroundColor: color.bg,
                                            border: `3px solid ${color.border}`,
                                        }}
                                    >
                                        {/* 商品卡片内容 */}
                                        <div className="p-4 text-center text-white">
                                            {/* 商品名称 */}
                                            <div className="font-bold text-lg mb-2 drop-shadow-md">
                                                {product.name}
                                            </div>

                                            {/* 价格 */}
                                            <div className="bg-white/30 backdrop-blur rounded-lg py-2 px-3 inline-block">
                                                <span className="text-2xl font-black">
                                                    ¥{product.sell_price}
                                                </span>
                                            </div>

                                            {/* 库存 */}
                                            <div className="mt-2 text-sm opacity-90">
                                                库存: {stock}
                                            </div>
                                        </div>

                                        {/* 缺货标签 */}
                                        {isOutOfStock && (
                                            <div className="absolute inset-0 flex items-center justify-center bg-black/40">
                                                <span className="bg-red-600 text-white px-4 py-2 rounded-lg font-bold text-lg transform -rotate-12 shadow-lg">
                                                    已售罄
                                                </span>
                                            </div>
                                        )}
                                    </motion.div>
                                );
                            })}
                        </div>
                    )}
                </Card>
            </div>

            {/* 购买成功动画 */}
            <AnimatePresence>
                {droppedProduct && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.5, y: -100 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.5, y: 100 }}
                        className="fixed inset-0 flex items-center justify-center bg-black/50 z-50"
                        onClick={() => setDroppedProduct(null)}
                    >
                        <motion.div
                            initial={{ rotate: -10 }}
                            animate={{ rotate: [10, -10, 10, 0] }}
                            transition={{ duration: 0.5 }}
                            className="bg-white rounded-2xl p-8 shadow-2xl text-center"
                        >
                            <div className="text-6xl mb-4">🎉</div>
                            <div className="text-2xl font-bold text-green-600 mb-2">
                                购买成功！
                            </div>
                            <div className="text-xl text-gray-700">
                                {droppedProduct.name}
                            </div>
                            <div className="text-gray-500 mt-2">
                                点击任意位置关闭
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default MobilePurchase;