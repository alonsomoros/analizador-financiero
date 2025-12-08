import { useNotification } from '../../context/NotificationContext';
import styles from './Notification.module.css';

const Notification = () => {
    const { notifications, removeNotification } = useNotification();

    if (notifications.length === 0) return null;

    return (
        <div className={styles.container}>
            {notifications.map((notification) => (
                <div
                    key={notification.id}
                    className={`${styles.notification} ${styles[notification.type]}`}
                    onClick={() => removeNotification(notification.id)}
                >
                    <div className={styles.icon}>
                        {notification.type === 'success' && '✓'}
                        {notification.type === 'error' && '✕'}
                        {notification.type === 'warning' && '⚠'}
                        {notification.type === 'info' && 'ℹ'}
                    </div>
                    <div className={styles.message}>{notification.message}</div>
                    <button
                        className={styles.closeButton}
                        onClick={() => removeNotification(notification.id)}
                        aria-label="Cerrar notificación"
                    >
                        ✕
                    </button>
                </div>
            ))}
        </div>
    );
};

export default Notification;
