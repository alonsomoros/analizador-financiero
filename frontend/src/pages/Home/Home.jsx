import Header from '../../components/Header/Header';
import UploadComponent from '../../components/UploadComponent/UploadComponent';
import styles from './Home.module.css';

const Home = () => {
    return (
        <div className={styles.homePage}>
            <Header />

            <main className={styles.main}>
                <div className={styles.hero}>
                    <h1 className={styles.title}>
                        Analizador Financiero
                    </h1>
                    <p className={styles.subtitle}>
                        Sube tu archivo CSV y obtén análisis detallados de tus transacciones financieras
                    </p>
                </div>

                <div className={styles.uploadSection}>
                    <UploadComponent />
                </div>

                <div className={styles.features}>
                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>📊</div>
                        <h3 className={styles.featureTitle}>Análisis Automático</h3>
                        <p className={styles.featureText}>
                            Clasificación inteligente de tus transacciones
                        </p>
                    </div>

                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>📈</div>
                        <h3 className={styles.featureTitle}>Visualizaciones</h3>
                        <p className={styles.featureText}>
                            Gráficos interactivos y reportes detallados
                        </p>
                    </div>

                    <div className={styles.feature}>
                        <div className={styles.featureIcon}>🔒</div>
                        <h3 className={styles.featureTitle}>Seguro</h3>
                        <p className={styles.featureText}>
                            Tus datos se procesan de forma segura
                        </p>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Home;
