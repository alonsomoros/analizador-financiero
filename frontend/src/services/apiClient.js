import axios from 'axios';

// Crear instancia de axios con configuración base
const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    timeout: 30000, // 30 segundos para uploads grandes
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para requests
apiClient.interceptors.request.use(
    (config) => {
        // Aquí podrías agregar tokens de autenticación en el futuro
        // config.headers.Authorization = `Bearer ${token}`;
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para responses
apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Manejo centralizado de errores
        if (error.response) {
            // El servidor respondió con un código de error
            console.error('Error de respuesta:', error.response.data);
        } else if (error.request) {
            // La petición fue hecha pero no hubo respuesta
            console.error('Error de red:', error.message);
        } else {
            // Algo pasó al configurar la petición
            console.error('Error:', error.message);
        }
        return Promise.reject(error);
    }
);

export default apiClient;
