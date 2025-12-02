# Importamos nuestras librerias
# Necesitamos numpy para valores aleatorios y exponenciales de la función
# Streamlit para la interfaz
# Pandas para el dataframe de resultados
import numpy as np 
import streamlit as st
import pandas as pd

# Clase entrada que tiene atributos a, b y n como parámetros, a y b siendo floats por los límites y n un entero para no tener cantidad decimal de muestras
class Entrada:
    def __init__(self, tamaño_muestra: int, a: float, b: float, f: str):
        assert tamaño_muestra > 0, "Valor de tamaño de muestra inválido" # Tiene que haber al menos una muestra porque no tiene chiste hacer el código sin muestras
        assert a < b, "a debe ser menor que b" # El límite inferior debe ser menor al superior
        
        # Aseguramos que sean del tipo que necesitamos
        self.tamaño_muestra = int(tamaño_muestra)
        self.a = float(a)
        self.b = float(b)
        self.f = f

    # La función 1 / (e^x + e^-x) 
    def f1(self, x):
        return 1 / (np.exp(x) + np.exp(-x))
    
    # La función 2 / (e^x + e^-x) 
    def f2(self, x):
        return 2 / (np.exp(x) + np.exp(-x))

    # Función para generar muestras aleatorias
    def muestra_aleatoria(self):

        # Listas vacías para guardar los resultados
        muestras = []
        valores_a = []
        valores_b = []
        valores_x = []
        valores_y = []
        valores_estimados = []

        b_a = (self.b - self.a) # b-a para aproximar la integral en toda el área

        for i in range(self.tamaño_muestra): # Cantidad de muestras
            x = np.random.uniform(self.a, self.b) # Número aleatorio entre los límites

            if self.f == 'a':
                y = self.f1(x) # Evaluar x en la función
            elif self.f == 'b':
                y = self.f2(x) 
            else:
                raise ValueError("Funciones válidas: 'a' y 'b'")

            integral_estimada = b_a * y # Estimamos la integral como (b-a)/n * f(x)

            # Añadimos los valores a las listas y repetimos hasta llegar al número de muestras
            muestras.append(i + 1)
            valores_a.append(self.a)
            valores_b.append(self.b)
            valores_x.append(x)
            valores_y.append(y)
            valores_estimados.append(integral_estimada)

        # Almacenamos las listas como un dataframe
        df = pd.DataFrame({
            'Muestra': muestras,
            'a': valores_a,
            'b': valores_b,
            'x': valores_x,
            'y': valores_y,
            'Integral Estimada': valores_estimados
        })

        return df

def main():
    # Título de la página, el que sale arriba en las pestañas y en la app de streamlit
    st.set_page_config(page_title = "Examen Argumentativo Periodo III AgoDic2025", layout = "wide", initial_sidebar_state = "expanded")
    st.title("Examen Argumentativo Periodo III AgoDic2025")
    
    # Header en la barra lateral
    st.sidebar.header("Parámetros (Se puede dar click en los valores para cambiarlos)")
    
    # Inputs para a, b y n
    a = st.sidebar.number_input(
        label  = "Límite inferior (a):",
        value = 0.0
    )

    b = st.sidebar.number_input(
        label  = "Límite superior (b):", 
        value = 2.0, 
        min_value = a + 0.00001 # b tiene que ser mayor que a
    )

    n = st.sidebar.number_input(
        label  = "Tamaño de muestra (n):", 
        value = 100,
        min_value = 1, # mínimo una muestra
    )

    f = st.sidebar.text_input(
        label  = "Función (a o b):", 
    )

    # Botón para ejecutar la simulación
    col1, col2 = st.sidebar.columns(2) # Necesito 2 columnas porque da error en streamlit pero solo uso una
    with col1:
        ejecutar_simulacion = st.button("Simular Monte Carlo")

    # Creamos un dataframe para guardar todo
    resultados = pd.DataFrame()

    # Se hace el proceso de muestras aleatorias cuando se presiona el botón
    if ejecutar_simulacion:
        st.info(f"Simulación con: n = {n}, a = {a}, b = {b}, función = {f}")
        entrada = Entrada(n, a, b, f)
        resultados = entrada.muestra_aleatoria()
    
    # Display del dataframe
    st.subheader("Resultados")
    st.dataframe(resultados)

    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        # Número de muestras
        muestras_count = int(resultados.shape[0]) if not resultados.empty else 0
        st.metric("Muestras", muestras_count)
    with col2:
        # Promedio de las aproximaciones (que solo se muestra si se dió al botón)
        if not resultados.empty:
            promedio = resultados['Integral Estimada'].mean()
            st.metric("Promedio de aproximaciones", f"{promedio:.4f}")
        else:
            st.metric("Promedio de aproximaciones", "N/A")

# Ejecutamos la función main
if __name__ == "__main__":
    main()