# AUTOR: Jhon Fredy Ayala
#
import numpy as np
import matplotlib.pyplot as plt

# Condiciones iniciales
h = 0.1; 
t = 0;
Q = np.array([0, 0])  # Condiciones iniciales
N = 21  # Número de iteraciones

# Inicializar array para almacenar resultados
rk5 = np.zeros(N)

# Función de la derivada
def F(t, Q):
    return np.array([Q[1], 550*np.cos(11*t) - 5*Q[1] - 6*Q[0]])

for i in range(N):
    # Método de Runge-Kutta de 5to orden (RK5)
    k1 = h * F(t, Q)
    k2 = h * F(t + h/4, Q + k1/4)
    k3 = h * F(t + h/4, Q + k1/8 + k2/8)
    k4 = h * F(t + h/2, Q - k2/2 + k3)
    k5 = h * F(t + 3*h/4, Q + 3*k1/16 + 9*k4/16)
    k6 = h * F(t + h, Q - 3*k1/7 + 2*k2/7 + 12*k3/7 - 12*k4/7 + 8*k5/7)
    
    Q_RK5_nueva = Q + (1/90) * (7*k1 + 32*k3 + 12*k4 + 32*k5 + 7*k6)
    rk5[i] = Q_RK5_nueva[0]  # Guardamos el valor de RK5

    # Actualizamos Q para la siguiente iteración
    Q = Q_RK5_nueva
    t += h  # Avanzamos en el tiempo

# Gráficos
plt.figure()
plt.plot(rk5, 'r', label='RK5', linewidth=2)
plt.legend()
plt.title('Método de Runge-Kutta de 5to Orden')
plt.xlabel('Iteración')
plt.ylabel('Valor de Q')
plt.grid(True)
plt.show()
