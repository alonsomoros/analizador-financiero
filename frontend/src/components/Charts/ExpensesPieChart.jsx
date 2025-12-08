import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import styles from './ExpensesPieChart.module.css';

const COLORS = [
    'hsl(0, 85%, 60%)',     // Rojo
    'hsl(45, 100%, 60%)',   // Amarillo
    'hsl(140, 70%, 55%)',   // Verde
    'hsl(200, 100%, 60%)',  // Azul
    'hsl(280, 100%, 65%)',  // Púrpura
    'hsl(320, 100%, 65%)',  // Rosa
    'hsl(30, 100%, 60%)',   // Naranja
    'hsl(180, 70%, 55%)',   // Cian
];

const ExpensesPieChart = ({ data }) => {
    // Filtrar solo gastos (montos negativos) y convertir a positivo
    const expensesData = data
        .filter(item => item.total < 0)
        .map(item => ({
            name: item.category,
            value: Math.abs(item.total),
        }))
        .sort((a, b) => b.value - a.value); // Ordenar de mayor a menor

    if (expensesData.length === 0) {
        return (
            <div className={styles.emptyState}>
                <p>No hay datos de gastos disponibles</p>
            </div>
        );
    }

    const formatCurrency = (value) => {
        return `€${value.toFixed(2)}`;
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0];
            const total = expensesData.reduce((sum, item) => sum + item.value, 0);
            const percentage = ((data.value / total) * 100).toFixed(1);

            return (
                <div className={styles.tooltip}>
                    <p className={styles.tooltipLabel}>{data.name}</p>
                    <p className={styles.tooltipValue}>{formatCurrency(data.value)}</p>
                    <p className={styles.tooltipPercent}>{percentage}%</p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className={styles.chartContainer}>
            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={expensesData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {expensesData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend
                        verticalAlign="bottom"
                        height={36}
                        formatter={(value, entry) => {
                            const percentage = ((entry.payload.value / expensesData.reduce((sum, item) => sum + item.value, 0)) * 100).toFixed(1);
                            return `${value} (${percentage}%)`;
                        }}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ExpensesPieChart;
