import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import styles from './MonthlyTrendChart.module.css';

const MonthlyTrendChart = ({ data }) => {
    // Transformar datos para el gráfico
    const chartData = data.map(item => ({
        month: item.month,
        total: item.total,
    }));

    if (chartData.length === 0) {
        return (
            <div className={styles.emptyState}>
                <p>No hay datos mensuales disponibles</p>
            </div>
        );
    }

    const formatCurrency = (value) => {
        return `€${value.toFixed(0)}`;
    };

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            return (
                <div className={styles.tooltip}>
                    <p className={styles.tooltipLabel}>{label}</p>
                    <p className={styles.tooltipValue}>
                        {formatCurrency(payload[0].value)}
                    </p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className={styles.chartContainer}>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                    <XAxis
                        dataKey="month"
                        stroke="var(--color-text-secondary)"
                        style={{ fontSize: '12px' }}
                    />
                    <YAxis
                        stroke="var(--color-text-secondary)"
                        style={{ fontSize: '12px' }}
                        tickFormatter={formatCurrency}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="total"
                        stroke="hsl(240, 100%, 65%)"
                        strokeWidth={3}
                        dot={{ fill: 'hsl(240, 100%, 65%)', r: 5 }}
                        activeDot={{ r: 7 }}
                        name="Total"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default MonthlyTrendChart;
