clear; clc;
h = 0.1; t = 0; Q = [0; 0];  % Condiciones iniciales
N = 21;  % Número de iteraciones

%rk5(1) = 0;  % Almacena el primer valor de la solución RK5
%euler(1)=0;
v_real      = zeros(1, N);
euler_error = zeros(1, N);  % Inicializamos el vector de errores para Euler
rk5_error   = zeros(1, N);  % Inicializamos el vector de errores para RK5

for i = 1:N
    % Método de Euler:
    Q_euler  = Q + h * F(t, Q);
    euler(i) = Q_euler(1,1);  % Guardamos el resultado del método de Euler

    % Método de Runge-Kutta 5to orden (RK5):
    k1 = h * F(t, Q);
    k2 = h * F(t + h/4, Q + k1/4);
    k3 = h * F(t + h/4, Q + k1/8 + k2/8);
    k4 = h * F(t + h/2, Q - k2/2 + k3);
    k5 = h * F(t + 3*h/4, Q + 3*k1/16 + 9*k4/16);
    k6 = h * F(t + h, Q - 3*k1/7 + 2*k2/7 + 12*k3/7 - 12*k4/7 + 8*k5/7);
    
    Q_RK5_nueva = Q + (1/90) * (7*k1 + 32*k3 + 12*k4 + 32*k5 + 7*k6);
    rk5(i+1) = Q_RK5_nueva(1,1);  % Guardamos el valor de RK5

    % Solución analítica (función exacta)
    analitica(i) = (-253/65) * cos(11*t) + (121/65) * sin(11*t) - (44/5) * exp(-2*t) + (165/13) * exp(-3*t);
    
    %fprintf("Iteración: %d\n", i); disp(Q_RK5_nueva); disp(euler(i)); disp(analitica(i)); disp(rk5(i)); % Imprime el resultado de RK5
    
    % Error de Euler y RK5 con respecto a la solución analítica
    euler_error(i) = abs(euler(i) - analitica(i));
    rk5_error(i)   = abs(rk5(i)   - analitica(i));
    v_real(i)      = analitica(i);

    Q = Q_RK5_nueva;  % Actualizamos Q para la siguiente iteración
    t = t + h;  % Avanzamos en el tiempo
end

% Mostrar los resultados en una tabla
%T = table((1:N)', euler', rk5(2:end)', euler_error', rk5_error', 'VariableNames', {'Iteración', 'Euler', 'RK5', 'Error_Euler', 'Error_RK5'});
T = table((1:N)', v_real', euler', rk5(1:end-1)', euler_error', rk5_error', 'VariableNames', {'Iteración', 'Analitica', 'Euler', 'RK5', 'Error_Euler', 'Error_RK5'});
disp('Tabla de resultados con errores:');
disp(T);

% Guardar la tabla de errores en un archivo .csv
writetable(T, 'errores.csv');  % Guardamos la tabla en un archivo llamado "errores.csv"

% Gráficos
hold on;
plot(euler,     'b',   'LineWidth', 1);  % Resultados de Euler
plot(rk5,       'r',   'LineWidth', 1);  % Resultados de RK5
plot(analitica, 'k--', 'LineWidth', 2);  % Solución analítica

legend('Analítica', 'Euler', 'RK5');
title('Comparación de Métodos Numéricos');
xlabel('Iteración');
ylabel('Valor de Q');
grid on;

% Función de la derivada
function res = F(t, Q)
    res = [Q(2,1); 550*cos(11*t) - 5*Q(2,1) - 6*Q(1,1)];
end

disp(Q_RK5_nueva); disp(euler); disp(analitica); disp(rk5(1:end-1));