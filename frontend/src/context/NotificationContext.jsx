import { createContext, useContext, useState, useCallback } from 'react';

const NotificationContext = createContext();

export const useNotification = () => {
    const context = useContext(NotificationContext);
    if (!context) {
        throw new Error('useNotification must be used within NotificationProvider');
    }
    return context;
};

export const NotificationProvider = ({ children }) => {
    const [notifications, setNotifications] = useState([]);

    const addNotification = useCallback((message, type = 'info') => {
        const id = Date.now();
        const notification = { id, message, type };

        setNotifications((prev) => [...prev, notification]);

        // Auto-remove después de 5 segundos
        setTimeout(() => {
            removeNotification(id);
        }, 5000);

        return id;
    }, []);

    const removeNotification = useCallback((id) => {
        setNotifications((prev) => prev.filter((n) => n.id !== id));
    }, []);

    const showSuccess = useCallback((message) => {
        return addNotification(message, 'success');
    }, [addNotification]);

    const showError = useCallback((message) => {
        return addNotification(message, 'error');
    }, [addNotification]);

    const showInfo = useCallback((message) => {
        return addNotification(message, 'info');
    }, [addNotification]);

    const showWarning = useCallback((message) => {
        return addNotification(message, 'warning');
    }, [addNotification]);

    return (
        <NotificationContext.Provider
            value={{
                notifications,
                addNotification,
                removeNotification,
                showSuccess,
                showError,
                showInfo,
                showWarning,
            }}
        >
            {children}
        </NotificationContext.Provider>
    );
};
