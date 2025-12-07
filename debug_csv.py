import pandas as pd

# Leer el CSV
df = pd.read_csv('TransactionExcelFile.csv', sep=';', encoding='latin-1', skiprows=7)

print("=== Análisis de la columna Importe ===")
print(f"\nPrimeros 10 valores:")
for i in range(min(10, len(df))):
    val = df['Importe'].iloc[i]
    print(f"  {i+1}. Valor: {repr(val)} | Tipo: {type(val)}")

print(f"\n=== Valores únicos (primeros 20) ===")
unique_vals = df['Importe'].unique()[:20]
for val in unique_vals:
    print(f"  {repr(val)}")
