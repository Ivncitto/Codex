# BY: IIV
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import random

# Colores del GUI
color_fondo = "#272822"
color_texto = "#F8F8F2"
color_boton = "#6699CC"
color_entrada = "#1E1E1E"
color_fondo_grafico = "#1E1E1E"
color_linea_grafico = "#A6E22E"
color_resaltado = "#FD971F"
color_boton_hover = "#506680"

# Funciones auxiliares
def validar_entrada(entrada_binaria):
    """Valida que la entrada sea una cadena binaria."""
    if not entrada_binaria or any(bit not in '01' for bit in entrada_binaria):
        messagebox.showerror("Error de entrada", "Por favor, ingrese solo bits binarios (0 o 1).")
        return False
    return True

def configurar_ejes(titulo, datos_binarios):
    """Configura los ejes del gráfico con entrada binaria en el eje X."""
    eje.clear()
    eje.set_ylim(-1.2, 1.2)
    eje.set_facecolor(color_fondo_grafico)
    eje.tick_params(colors=color_texto)
    eje.xaxis.label.set_color(color_texto)
    eje.yaxis.label.set_color(color_texto)
    eje.set_title(titulo, color=color_texto)
    eje.grid(True, color="#444444", linestyle="--", linewidth=0.5)
    eje.yaxis.set_major_locator(plt.MultipleLocator(0.5))
    eje.set_xlabel('Bits de Entrada', color=color_texto)
    eje.set_ylabel('Amplitud (V)', color=color_texto)
    eje.set_xticks(np.arange(0, len(datos_binarios) * 2, 2))
    eje.set_xticklabels(datos_binarios)

def expandir_senal(senal, factor=2):
    """Expande una señal duplicando cada elemento."""
    return np.repeat(senal, factor)

# Funciones de codificación
def codificar_nrzl(datos):
    """Codificación NRZ-L: 0 = nivel alto, 1 = nivel bajo."""
    senal_codificada = np.array([1 if bit == '0' else -1 for bit in datos])
    tiempo = np.arange(len(datos) * 2)
    return expandir_senal(senal_codificada), tiempo, list(datos)

def codificar_nrzi(datos):
    """Codificación NRZ-I: Transición según el bit."""
    senal_codificada = []
    nivel_anterior = -1
    for bit in datos:
        if bit == '1':
            nivel_anterior *= -1
        senal_codificada.append(nivel_anterior)
    tiempo = np.arange(len(datos) * 2)
    return expandir_senal(senal_codificada), tiempo, list(datos)

def codificar_bipolar_ami(datos):
    """Codificación Bipolar-AMI: Polaridad alternante para 1s."""
    nivel = 1
    senal_codificada = []
    for bit in datos:
        if bit == '1':
            senal_codificada.append(nivel)
            nivel *= -1
        else:
            senal_codificada.append(0)
    tiempo = np.arange(len(datos) * 2)
    return expandir_senal(senal_codificada), tiempo, list(datos)

def codificar_pseudoternaria(datos):
    """Codificación Pseudoternaria: Polaridad alternante para 0s."""
    nivel = 1
    senal_codificada = []
    for bit in datos:
        if bit == '0':
            senal_codificada.append(nivel)
            nivel *= -1
        else:
            senal_codificada.append(0)
    tiempo = np.arange(len(datos) * 2)
    return expandir_senal(senal_codificada), tiempo, list(datos)

def codificar_manchester(datos):
    """Codificación Manchester: Transición en mitad del intervalo."""
    senal_codificada = []
    for bit in datos:
        if bit == '1':
            senal_codificada.extend([-1, 1])
        else:
            senal_codificada.extend([1, -1])
    tiempo = np.arange(len(datos) * 2)
    return senal_codificada, tiempo, list(datos)

def codificar_manchester_diferencial(datos):
    """Codificación Manchester Diferencial."""
    nivel_actual = -1
    senal_codificada = []
    for bit in datos:
        if bit == '0':
            nivel_actual *= -1
            senal_codificada.extend([nivel_actual, -nivel_actual])
        else:
            senal_codificada.extend([-nivel_actual, nivel_actual])
    tiempo = np.arange(len(datos) * 2)
    return senal_codificada, tiempo, list(datos)

def codificar_b8zs(datos):
    """Codificación B8ZS: Sustitución de 8 ceros según la polaridad del último pulso."""
    nivel = 1
    senal_codificada = []
    i = 0

    while i < len(datos):
        if datos[i:i+8] == '00000000':  # Detecta una secuencia de 8 ceros
            if nivel == 1:  # Último pulso fue positivo
                senal_codificada.extend([0, 0, 0, -1, 0, 1, -1, 1])
            else:  # Último pulso fue negativo
                senal_codificada.extend([0, 0, 0, 1, 0, -1, 1, -1])
            i += 8
        else:
            if datos[i] == '1':
                senal_codificada.append(nivel)
                nivel *= -1
            else:
                senal_codificada.append(0)
            i += 1

    tiempo = np.arange(len(senal_codificada) * 2)
    return expandir_senal(senal_codificada), tiempo, list(datos)

# Función de animación del gráfico
def animar_grafico(funcion_codificacion):
    entrada_binaria = entrada_texto.get()
    if not validar_entrada(entrada_binaria):
        return
    senal, tiempo, datos_binarios = funcion_codificacion(entrada_binaria)
    configurar_ejes('Señal Codificada', datos_binarios)
    eje.set_xlim(0, len(tiempo) - 1)

    def animar(i):
        eje.clear()
        configurar_ejes('Señal Codificada', datos_binarios)
        eje.set_xlim(0, len(tiempo) - 1)
        eje.plot(tiempo[:i + 1], senal[:i + 1], drawstyle='steps-pre', color=color_linea_grafico, linewidth=2)

        if i < len(senal):
            eje.plot(tiempo[i], senal[i], 'o', color=color_resaltado)

        eje.axvline(x=tiempo[i], color=color_resaltado, linestyle='--', linewidth=1)

    animacion = FuncAnimation(figura, animar, frames=np.arange(0, len(senal)), interval=30, repeat=False)
    canvas.draw()

def generar_binario_aleatorio():
    longitud = random.randint(8, 42)
    binario_aleatorio = ''.join(random.choice('01') for _ in range(longitud))
    entrada_texto.delete(0, tk.END)
    entrada_texto.insert(0, binario_aleatorio)

def cerrar_aplicacion():
    ventana_principal.destroy()

# Configuración de la ventana
ventana_principal = tk.Tk()
ventana_principal.title("Proyecto de Codificadores")
ventana_principal.configure(bg=color_fondo)
ventana_principal.attributes('-fullscreen', True)

# Título del proyecto
titulo_label = tk.Label(ventana_principal, text="Proyecto de Codificadores", font=("Helvetica", 20),
                        fg=color_texto, bg=color_fondo, pady=10)
titulo_label.grid(row=0, column=0, columnspan=3)

# Etiqueta y campo de entrada
frame_entrada = tk.Frame(ventana_principal, bg=color_fondo)
frame_entrada.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="we")

entrada_label = tk.Label(frame_entrada, text="Ingresa código binario:", font=("Helvetica", 16),
                         fg=color_texto, bg=color_fondo)
entrada_label.pack(side=tk.LEFT, padx=10)

entrada_texto = tk.Entry(frame_entrada, font=("Helvetica", 16), fg=color_texto, bg=color_entrada, insertbackground=color_texto)
entrada_texto.pack(side=tk.LEFT, expand=True, fill="x", padx=10)

# Área de gráficos
figura, eje = plt.subplots(figsize=(14, 7))
figura.patch.set_facecolor(color_fondo)
configurar_ejes('Señal Codificada', [])

canvas = FigureCanvasTkAgg(figura, master=ventana_principal)
widget_canvas = canvas.get_tk_widget()
widget_canvas.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

# Botones para las codificaciones
frame_botones = tk.Frame(ventana_principal, bg=color_fondo)
frame_botones.grid(row=2, column=0, padx=10, pady=10, sticky="ns")

opciones_codificacion = [
    ("NRZ-L", codificar_nrzl),
    ("NRZ-I", codificar_nrzi),
    ("Bipolar AMI", codificar_bipolar_ami),
    ("Pseudoternaria", codificar_pseudoternaria),
    ("Manchester", codificar_manchester),
    ("Manchester Diferencial", codificar_manchester_diferencial),
    ("B8ZS", codificar_b8zs),
]

for etiqueta, funcion in opciones_codificacion:
    boton = tk.Button(frame_botones, text=etiqueta, command=lambda f=funcion: animar_grafico(f),
                      font=("Helvetica", 12), fg=color_texto, bg=color_boton,
                      activebackground=color_boton_hover, cursor="hand2")
    boton.pack(pady=5, fill='x')

# Botón para generar un número binario aleatorio
boton_generar = tk.Button(ventana_principal, text="Generar Binario Aleatorio", command=generar_binario_aleatorio,
                          font=("Helvetica", 12), fg=color_texto, bg=color_boton,
                          activebackground=color_boton_hover, cursor="hand2")
boton_generar.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

# Botón de cerrar aplicación
boton_cerrar = tk.Button(ventana_principal, text="Cerrar Aplicación", command=cerrar_aplicacion,
                         font=("Helvetica", 12), fg=color_texto, bg=color_boton,
                         activebackground=color_boton_hover, cursor="hand2")
boton_cerrar.grid(row=3, column=2, padx=10, pady=5, sticky="e")

ventana_principal.mainloop()
