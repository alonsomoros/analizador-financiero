import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import styles from './IncomeVsExpensesChart.module.css';

const IncomeVsExpensesChart = ({ totalIncome, totalExpenses }) => {
    const chartData = [
        {
            name: 'Resumen',
            Ingresos: totalIncome,
            Gastos: Math.abs(totalExpenses),
        },
    ];

    const formatCurrency = (value) => {
        return `€${value.toFixed(0)}`;
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className={styles.tooltip}>
                    {payload.map((entry, index) => (
                        <div key={index} className={styles.tooltipItem}>
                            <span className={styles.tooltipLabel}>{entry.name}:</span>
                            <span className={styles.tooltipValue} style={{ color: entry.color }}>
                                {formatCurrency(entry.value)}
                            </span>
                        </div>
                    ))}
                </div>
            );
        }
        return null;
    };

    return (
        <div className={styles.chartContainer}>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                    <XAxis
                        dataKey="name"
                        stroke="var(--color-text-secondary)"
                        style={{ fontSize: '14px' }}
                    />
                    <YAxis
                        stroke="var(--color-text-secondary)"
                        style={{ fontSize: '12px' }}
                        tickFormatter={formatCurrency}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Bar
                        dataKey="Ingresos"
                        fill="hsl(140, 70%, 55%)"
                        radius={[8, 8, 0, 0]}
                    />
                    <Bar
                        dataKey="Gastos"
                        fill="hsl(0, 85%, 60%)"
                        radius={[8, 8, 0, 0]}
                    />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default IncomeVsExpensesChart;
