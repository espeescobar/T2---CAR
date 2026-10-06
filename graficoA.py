import matplotlib.pyplot as plt

# Datos obtenidos
n_values = ['2048', '1024', '512', '256', '128', '64', '32']
tiempos_ms = [5409.92, 5505.41, 6395.82, 4918.70, 4172.19, 4760.45, 5484.10]

plt.figure(figsize=(10, 6))
plt.plot(n_values, tiempos_ms, marker='o', linestyle='-', color='b', label='Tiempo de ejecución secuencial')

# Formato según las exigencias de la tarea
plt.title('Tiempo de ejecución vs Tamaño de bloque (N=2048)', fontsize=16)
plt.xlabel('Tamaño de bloque (n)', fontsize=14)
plt.ylabel('Tiempo (ms)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=12)

# Invertir el eje X para que coincida con el orden en que tomaste los datos (de mayor a menor)
plt.gca().invert_xaxis() 

# Guardar y mostrar
plt.savefig('grafico_bloques.png', dpi=300, bbox_inches='tight')
plt.show()