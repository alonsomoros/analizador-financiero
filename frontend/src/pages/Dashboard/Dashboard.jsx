import { useState, useEffect } from 'react';
import Header from '../../components/Header/Header';
import Sidebar from '../../components/Sidebar/Sidebar';
import ExpensesPieChart from '../../components/Charts/ExpensesPieChart';
import MonthlyTrendChart from '../../components/Charts/MonthlyTrendChart';
import IncomeVsExpensesChart from '../../components/Charts/IncomeVsExpensesChart';
import { getTransactionStats } from '../../services/transactionService';
import { useNotification } from '../../context/NotificationContext';
import styles from './Dashboard.module.css';

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const { showError } = useNotification();

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        setIsLoading(true);
        try {
            const data = await getTransactionStats();
            setStats(data);
        } catch (error) {
            console.error('Error al cargar estadísticas:', error);
            showError('Error al cargar los datos del dashboard');
        } finally {
            setIsLoading(false);
        }
    };

    const formatCurrency = (value) => {
        return `€${value.toFixed(2)}`;
    };

    if (isLoading) {
        return (
            <div className={styles.dashboardPage}>
                <Header />
                <div className={styles.dashboardLayout}>
                    <Sidebar />
                    <main className={styles.mainContent}>
                        <div className={styles.loadingContainer}>
                            <div className={styles.spinner}></div>
                            <p>Cargando datos...</p>
                        </div>
                    </main>
                </div>
            </div>
        );
    }

    const hasData = stats && stats.total_transactions > 0;

    return (
        <div className={styles.dashboardPage}>
            <Header />

            <div className={styles.dashboardLayout}>
                <Sidebar />

                <main className={styles.mainContent}>
                    <div className={styles.header}>
                        <h1 className={styles.title}>Dashboard Financiero</h1>
                        <p className={styles.subtitle}>
                            {hasData
                                ? 'Visualiza y analiza tus transacciones financieras'
                                : 'Sube un archivo CSV para comenzar'
                            }
                        </p>
                    </div>

                    {hasData ? (
                        <>
                            <div className={styles.statsGrid}>
                                <div className={styles.statCard}>
                                    <div className={styles.statIcon}>💰</div>
                                    <div className={styles.statContent}>
                                        <p className={styles.statLabel}>Balance Total</p>
                                        <p className={styles.statValue}>{formatCurrency(stats.net_balance)}</p>
                                    </div>
                                </div>

                                <div className={styles.statCard}>
                                    <div className={styles.statIcon}>📥</div>
                                    <div className={styles.statContent}>
                                        <p className={styles.statLabel}>Ingresos</p>
                                        <p className={`${styles.statValue} ${styles.positive}`}>
                                            {formatCurrency(stats.total_income)}
                                        </p>
                                    </div>
                                </div>

                                <div className={styles.statCard}>
                                    <div className={styles.statIcon}>📤</div>
                                    <div className={styles.statContent}>
                                        <p className={styles.statLabel}>Gastos</p>
                                        <p className={`${styles.statValue} ${styles.negative}`}>
                                            {formatCurrency(Math.abs(stats.total_expenses))}
                                        </p>
                                    </div>
                                </div>

                                <div className={styles.statCard}>
                                    <div className={styles.statIcon}>📊</div>
                                    <div className={styles.statContent}>
                                        <p className={styles.statLabel}>Transacciones</p>
                                        <p className={styles.statValue}>{stats.total_transactions}</p>
                                    </div>
                                </div>
                            </div>

                            <div className={styles.chartsGrid}>
                                <div className={styles.chartCard}>
                                    <h3 className={styles.chartTitle}>Gastos por Categoría</h3>
                                    <ExpensesPieChart data={stats.by_category} />
                                </div>

                                <div className={styles.chartCard}>
                                    <h3 className={styles.chartTitle}>Tendencia Mensual</h3>
                                    <MonthlyTrendChart data={stats.by_month} />
                                </div>

                                <div className={styles.chartCard}>
                                    <h3 className={styles.chartTitle}>Ingresos vs Gastos</h3>
                                    <IncomeVsExpensesChart
                                        totalIncome={stats.total_income}
                                        totalExpenses={stats.total_expenses}
                                    />
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className={styles.emptyState}>
                            <div className={styles.emptyIcon}>📊</div>
                            <h2 className={styles.emptyTitle}>No hay datos disponibles</h2>
                            <p className={styles.emptyText}>
                                Sube un archivo CSV desde la página de inicio para comenzar a visualizar tus transacciones
                            </p>
                            <a href="/" className={styles.emptyButton}>
                                Ir a Inicio
                            </a>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
};

export default Dashboard;
