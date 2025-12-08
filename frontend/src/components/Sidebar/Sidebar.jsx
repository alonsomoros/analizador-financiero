import { Link, useLocation } from 'react-router-dom';
import styles from './Sidebar.module.css';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { path: '/dashboard', icon: '📊', label: 'Resumen' },
        { path: '/dashboard/transactions', icon: '💳', label: 'Transacciones' },
        { path: '/dashboard/categories', icon: '🏷️', label: 'Categorías' },
        { path: '/dashboard/analytics', icon: '📈', label: 'Análisis' },
        { path: '/dashboard/reports', icon: '📄', label: 'Reportes' },
    ];

    return (
        <aside className={styles.sidebar}>
            <div className={styles.sidebarHeader}>
                <h2 className={styles.sidebarTitle}>Dashboard</h2>
            </div>

            <nav className={styles.nav}>
                {menuItems.map((item) => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`${styles.navItem} ${location.pathname === item.path ? styles.active : ''}`}
                    >
                        <span className={styles.navIcon}>{item.icon}</span>
                        <span className={styles.navLabel}>{item.label}</span>
                    </Link>
                ))}
            </nav>

            <div className={styles.sidebarFooter}>
                <Link to="/" className={styles.backButton}>
                    <span>←</span>
                    <span>Volver al inicio</span>
                </Link>
            </div>
        </aside>
    );
};

export default Sidebar;
