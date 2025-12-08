import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { NotificationProvider } from './context/NotificationContext';
import Notification from './components/Notification/Notification';
import Home from './pages/Home/Home';
import Dashboard from './pages/Dashboard/Dashboard';
import './App.css';

function App() {
  return (
    <NotificationProvider>
      <Router>
        <Notification />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/*" element={<Dashboard />} />
        </Routes>
      </Router>
    </NotificationProvider>
  );
}

export default App;
