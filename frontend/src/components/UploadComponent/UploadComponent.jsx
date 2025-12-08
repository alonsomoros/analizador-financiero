import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNotification } from '../../context/NotificationContext';
import { uploadCSV } from '../../services/transactionService';
import styles from './UploadComponent.module.css';

const UploadComponent = () => {
    const [isDragging, setIsDragging] = useState(false);
    const [fileName, setFileName] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const navigate = useNavigate();
    const { showSuccess, showError } = useNotification();

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    };

    const handleFileInput = (e) => {
        const files = e.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    };

    const handleFile = async (file) => {
        // Validar que sea un archivo CSV
        if (!file.name.endsWith('.csv')) {
            showError('Por favor selecciona un archivo CSV válido');
            return;
        }

        setFileName(file.name);
        setIsUploading(true);

        try {
            const result = await uploadCSV(file);

            // Mostrar notificación de éxito con estadísticas
            const stats = result.statistics;
            showSuccess(
                `✓ Archivo procesado exitosamente! ${stats.new_transactions} transacciones nuevas, ${stats.duplicates_skipped} duplicados omitidos`
            );

            // Navegar al dashboard después de un breve delay
            setTimeout(() => {
                navigate('/dashboard');
            }, 1500);

        } catch (error) {
            console.error('Error al subir archivo:', error);

            let errorMessage = 'Error al procesar el archivo';
            if (error.response?.data?.detail) {
                errorMessage = error.response.data.detail;
            } else if (error.message) {
                errorMessage = error.message;
            }

            showError(errorMessage);
            setFileName('');
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className={styles.uploadContainer}>
            <div
                className={`${styles.dropZone} ${isDragging ? styles.dragging : ''} ${fileName ? styles.hasFile : ''} ${isUploading ? styles.uploading : ''}`}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="fileInput"
                    className={styles.fileInput}
                    accept=".csv"
                    onChange={handleFileInput}
                    disabled={isUploading}
                />

                {isUploading ? (
                    <>
                        <div className={styles.spinner}></div>
                        <h3 className={styles.uploadTitle}>Procesando archivo...</h3>
                        <p className={styles.uploadSubtitle}>Por favor espera</p>
                    </>
                ) : (
                    <>
                        <div className={styles.uploadIcon}>
                            {fileName ? '✓' : '📁'}
                        </div>

                        <h3 className={styles.uploadTitle}>
                            {fileName ? 'Archivo Cargado' : 'Arrastra tu archivo CSV aquí'}
                        </h3>

                        <p className={styles.uploadSubtitle}>
                            {fileName || 'o haz clic para seleccionar'}
                        </p>

                        <label htmlFor="fileInput" className={styles.uploadButton}>
                            {fileName ? 'Cambiar archivo' : 'Seleccionar archivo'}
                        </label>
                    </>
                )}
            </div>

            {fileName && !isUploading && (
                <div className={styles.fileInfo}>
                    <p className={styles.fileInfoText}>
                        <span className={styles.fileInfoLabel}>Archivo:</span>
                        <span className={styles.fileInfoValue}>{fileName}</span>
                    </p>
                </div>
            )}
        </div>
    );
};

export default UploadComponent;
