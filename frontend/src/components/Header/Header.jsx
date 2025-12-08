import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header = () => {
    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <Link to="/" className={styles.logo}>
                    <span className={styles.logoIcon}>📊</span>
                    <span className={styles.logoText}>Analizador Financiero</span>
                </Link>

                <nav className={styles.nav}>
                    <Link to="/" className={styles.navLink}>
                        Inicio
                    </Link>
                    <Link to="/dashboard" className={styles.navLink}>
                        Dashboard
                    </Link>
                </nav>
            </div>
        </header>
    );
};

export default Header;
