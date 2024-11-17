import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Condiciones iniciales
h = 0.1
t = 0
Q = np.array([0, 0])  # Condiciones iniciales
N = 21  # Número de iteraciones

# Inicializar arrays para almacenar resultados
v_real = np.zeros(N)
euler = np.zeros(N)
euler_error = np.zeros(N)
rk5 = np.zeros(N)
rk5_error = np.zeros(N)

# Función de la derivada
def F(t, Q):
    return np.array([Q[1], 550 * np.cos(11 * t) - 5 * Q[1] - 6 * Q[0]])

for i in range(N):
    j=i-1;
    # Método de Euler
    Q_euler = Q + h * F(t, Q)
    euler[i] = Q_euler[0]  # Guardamos el resultado del método de Euler

    # Método de Runge-Kutta de 5to orden (RK5)
    k1 = h * F(t, Q)
    k2 = h * F(t + h / 4, Q + k1 / 4)
    k3 = h * F(t + h / 4, Q + k1 / 8 + k2 / 8)
    k4 = h * F(t + h / 2, Q - k2 / 2 + k3)
    k5 = h * F(t + 3 * h / 4, Q + 3 * k1 / 16 + 9 * k4 / 16)
    k6 = h * F(t + h, Q - 3 * k1 / 7 + 2 * k2 / 7 + 12 * k3 / 7 - 12 * k4 / 7 + 8 * k5 / 7)
    
    Q_RK5_nueva = Q + (1 / 90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
    rk5[i] = Q_RK5_nueva[0]  # Guardamos el valor de RK5

    # Solución analítica (función exacta)
    analitica = (-253 / 65) * np.cos(11 * t) + (121 / 65) * np.sin(11 * t) - (44 / 5) * np.exp(-2 * t) + (165 / 13) * np.exp(-3 * t)
    
    # Error de Euler y RK5 con respecto a la solución analítica
    euler_error[j] = abs(euler[j] - analitica)
    rk5_error[j] = abs(rk5[j] - analitica)
    v_real[j] = analitica
    
    # Actualizamos Q para la siguiente iteración
    Q = Q_RK5_nueva
    t += h  # Avanzamos en el tiempo

# Crear la tabla de resultados
df = pd.DataFrame({
    'i'          : np.arange(1, N+1),
    'Analítica'  : v_real,
    'Euler'      : euler,
    'RK5'        : rk5,
    'Error_Euler': euler_error,
    'Error_RK5'  : rk5_error
})

# Mostrar la tabla de resultados
print("Tabla de resultados con errores:")
print(df)

# Obtener la ruta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))  # Ruta del script .py
output_file = 'ERROR.csv'

# Crear la ruta completa del archivo .csv en el mismo directorio que el script
output_path = os.path.join(script_dir, output_file)

# Guardar la tabla de errores en un archivo *.csv
#df.to_csv('error.csv', index=False)
df.to_csv(output_path, index=False)
print(f"Archivo CSV guardado en: {output_path}")

# Gráficos
plt.figure()
plt.plot(v_real,'k--', label='Analítica', linewidth=3)
plt.plot(euler, 'b',   label='Euler',     linewidth=2)
plt.plot(rk5,   'r',   label='RK5',       linewidth=2)
plt.legend()
plt.title('Comparación de Métodos Numéricos')
plt.xlabel('Iteración')
plt.ylabel('Valor de Q')
plt.grid(True)
plt.show()