import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// 响应拦截器，处理错误
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
    }
);

export const endpoints = {
    machines: 'machines/',
    products: 'products/',
    inventories: 'inventories/',
    transactions: 'transactions/',
    restocks: 'restocks/',
    suppliers: 'suppliers/',
    users: 'app-users/',
    staffs: 'sys-staffs/',
    admins: 'sys-admins/',
    alerts: 'alerts/',
    statDaily: 'stat-daily/',
};

export default api;
