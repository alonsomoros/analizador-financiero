import styles from './ChartPlaceholder.module.css';

const ChartPlaceholder = ({ title, type = 'chart' }) => {
    const getIcon = () => {
        switch (type) {
            case 'bar':
                return '📊';
            case 'line':
                return '📈';
            case 'pie':
                return '🥧';
            case 'table':
                return '📋';
            default:
                return '📊';
        }
    };

    return (
        <div className={styles.placeholder}>
            <div className={styles.placeholderContent}>
                <div className={styles.icon}>{getIcon()}</div>
                <h3 className={styles.title}>{title}</h3>
                <p className={styles.subtitle}>Gráfico disponible próximamente</p>

                <div className={styles.skeleton}>
                    <div className={styles.skeletonBar} style={{ width: '80%' }}></div>
                    <div className={styles.skeletonBar} style={{ width: '60%' }}></div>
                    <div className={styles.skeletonBar} style={{ width: '90%' }}></div>
                    <div className={styles.skeletonBar} style={{ width: '70%' }}></div>
                </div>
            </div>
        </div>
    );
};

export default ChartPlaceholder;
