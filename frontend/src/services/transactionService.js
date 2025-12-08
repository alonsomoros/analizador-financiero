import apiClient from './apiClient';

/**
 * Subir archivo CSV de transacciones
 * @param {File} file - Archivo CSV a subir
 * @returns {Promise} Respuesta con estadísticas de procesamiento
 */
export const uploadCSV = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

/**
 * Obtener estadísticas agregadas de transacciones
 * @param {string} startDate - Fecha de inicio (YYYY-MM-DD) opcional
 * @param {string} endDate - Fecha de fin (YYYY-MM-DD) opcional
 * @returns {Promise} Estadísticas de transacciones
 */
export const getTransactionStats = async (startDate = null, endDate = null) => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    const response = await apiClient.get('/transactions/stats', { params });
    return response.data;
};

/**
 * Obtener lista de transacciones con filtros y paginación
 * @param {Object} params - Parámetros de filtrado y paginación
 * @returns {Promise} Lista paginada de transacciones
 */
export const getTransactions = async (params = {}) => {
    const response = await apiClient.get('/transactions', { params });
    return response.data;
};

/**
 * Obtener una transacción específica por ID
 * @param {number} id - ID de la transacción
 * @returns {Promise} Datos de la transacción
 */
export const getTransaction = async (id) => {
    const response = await apiClient.get(`/transactions/${id}`);
    return response.data;
};

/**
 * Eliminar una transacción por ID
 * @param {number} id - ID de la transacción a eliminar
 * @returns {Promise} Confirmación de eliminación
 */
export const deleteTransaction = async (id) => {
    const response = await apiClient.delete(`/transactions/${id}`);
    return response.data;
};

/**
 * Eliminar todas las transacciones (requiere confirmación)
 * @returns {Promise} Confirmación de eliminación
 */
export const deleteAllTransactions = async () => {
    const response = await apiClient.delete('/transactions', {
        params: { confirm: true },
    });
    return response.data;
};
