import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Machines from './pages/Machines';
import Products from './pages/Products';
import Inventory from './pages/Inventory';
import Users from './pages/Users';
import MobilePurchase from './pages/MobilePurchase';
import Suppliers from './pages/Suppliers';
import Transactions from './pages/Transactions';
import Restocks from './pages/Restocks';
import Staff from './pages/Staff';
import Statistics from './pages/Statistics';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="machines" element={<Machines />} />
          <Route path="products" element={<Products />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="users" element={<Users />} />
          <Route path="suppliers" element={<Suppliers />} />
          <Route path="transactions" element={<Transactions />} />
          <Route path="restocks" element={<Restocks />} />
          <Route path="staff" element={<Staff />} />
          <Route path="statistics" element={<Statistics />} />
          <Route path="mobile" element={<MobilePurchase />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;

