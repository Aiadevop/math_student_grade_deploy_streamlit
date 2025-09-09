#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Streamlit para predicción de calificaciones matemáticas
Versión Streamlit de la aplicación Flask
"""

import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en el sys.path para importar `src`
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')


# Configuración de la página
st.set_page_config(
    page_title="Predicción de Calificaciones Matemáticas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .prediction-box {
        background-color: #1F77AA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #1F77AA;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .form-container {
        background-color: #1F77AA;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)



from src.model import cargar_modelo, hacer_prediccion
from src.data import validar_datos, cargar_datos_desde_url, procesar_datos_desde_dataframe


# Función principal de la aplicación Streamlit
def main():    
    # Título principal
    st.markdown('<h1 class="main-header">📊 Predicción de Calificaciones Matemáticas</h1>', unsafe_allow_html=True)
    
    # Cargar modelo
    modelo, ruta_modelo = cargar_modelo()
    
    if modelo is None:
        st.error("❌ No se pudo cargar el modelo. Por favor, verifica que el archivo del modelo esté disponible.")
        return
    
    # Sidebar con información del modelo
    with st.sidebar:
        st.header("ℹ️ Información del Modelo")
        st.info(f"**Tipo:** {type(modelo).__name__}")
        st.info(f"**Ruta:** {ruta_modelo}")
        st.info("**Precisión:** 87.2% (R² = 0.872)")
        
        st.header("📋 Variables del Modelo")
        variables = [
            "Género", "Tipo de almuerzo", "Curso de preparación",
            "Puntuación de lectura", "Puntuación de escritura",
            "Grupo étnico E", "Nivel educativo padres"
        ]
        for i, var in enumerate(variables, 1):
            st.write(f"{i}. {var}")
    
    # Formulario principal
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.header("📝 Formulario de Predicción")
    
    # Opción para cargar datos desde URL
    st.subheader("🌐 Cargar datos desde URL (Opcional)")
    url_datos = st.text_input(
        "🔗 URL del archivo CSV",
        placeholder="https://raw.githubusercontent.com/.../datos.csv",
        help="Ingresa la URL de un archivo CSV con los datos del estudiante. Solo se permiten archivos .csv"
    )
    
    # Botón para cargar datos desde URL
    datos_desde_url = None
    if st.button("📥 Cargar datos desde URL", disabled=not url_datos):
        try:
            with st.spinner("Cargando datos desde URL..."):
                df, mensaje = cargar_datos_desde_url(url_datos)
                datos_desde_url = procesar_datos_desde_dataframe(df)
                st.success(f"✅ {mensaje}")
                st.info(f"📊 Se cargaron {len(df)} filas de datos")
                
                # Mostrar preview de los datos cargados
                with st.expander("👁️ Ver datos cargados"):
                    st.dataframe(df.head())
                    
        except Exception as e:
            st.error(f"❌ Error al cargar datos: {str(e)}")
    
    st.markdown("---")
    st.subheader("✏️ Ingresar datos manualmente")
    
    # Crear columnas para el formulario
    col1, col2 = st.columns(2)
    
    with col1:
        reading_score = st.number_input(
            "📖 Puntuación de lectura (0-100)",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=0.1,
            help="Ingresa la puntuación de lectura del estudiante"
        )
        
        writing_score = st.number_input(
            "✍️ Puntuación de escritura (0-100)",
            min_value=0.0,
            max_value=100.0,
            value=82.0,
            step=0.1,
            help="Ingresa la puntuación de escritura del estudiante"
        )
        
        gender = st.selectbox(
            "👤 Género",
            options=[("Femenino", 'female'), ("Masculino", 'male')],
            format_func=lambda x: x[0],
            help="Selecciona el género del estudiante"
        )
        
        lunch = st.selectbox(
            "🍽️ Tipo de almuerzo",
            options=[("Estándar", 'standard'), ("Gratuito/Reducido", 'free/reduced')],
            format_func=lambda x: x[0],
            help="Selecciona el tipo de almuerzo del estudiante"
        )
    
    with col2:
        test_preparation_course = st.selectbox(
            "📚 Curso de preparación",
            options=[("No", 'none'), ("Completado", 'completed')],
            format_func=lambda x: x[0],
            help="Indica si el estudiante completó el curso de preparación"
        )
        
        race_ethnicity_group_E = st.selectbox(
            "🌍 Grupo étnico E",
            options=[("No", 'group'), ("Sí", 'group E')],
            format_func=lambda x: x[0],
            help="Indica si el estudiante pertenece al grupo étnico E"
        )
        
        parental_level_of_education_high_school = st.selectbox(
            "🎓 Nivel educativo de los padres",
            options=[("Otro nivel", 'other'), ("Solo Secundaria", 'high school')],
            format_func=lambda x: x[0],
            help="Indica si los padres solo tienen educación secundaria"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón de predicción
    if st.button("🔮 Predecir Calificación Matemática", type="primary"):
        try:
            # Usar datos desde URL si están disponibles, sino usar datos del formulario
            if datos_desde_url is not None:
                datos = datos_desde_url
                st.info("📥 Usando datos cargados desde URL")
            else:
                # Preparar datos del formulario manual
                datos_formulario = {
                    'reading_score': reading_score,
                    'writing_score': writing_score,
                    'gender': gender[1],
                    'lunch': lunch[1],
                    'test_preparation_course': test_preparation_course[1],
                    'race_ethnicity_group_E': race_ethnicity_group_E[1],
                    'parental_level_of_education_high_school': parental_level_of_education_high_school[1]
                }
                st.info("✏️ Usando datos del formulario manual")
                
                # Crear DataFrame temporal para procesar los datos del formulario
                df_temporal = pd.DataFrame([datos_formulario])
                
                # Procesar datos del formulario usando la misma función que los datos de URL
                datos = procesar_datos_desde_dataframe(df_temporal)
            
            # Validar datos
            datos_validados, df_validado = validar_datos(datos)
            
            # Hacer predicción
            resultado_prediccion = hacer_prediccion(datos_validados, modelo)
            
            # Mostrar resultados
            st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
            st.header("🎯 Resultado de la Predicción")
            
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📊 Calificación Matemática Predicha",
                    value=f"{resultado_prediccion['math_score']}/100",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="🎯 Confianza del Modelo",
                    value=f"{resultado_prediccion['confidence']*100:.1f}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label="📈 Variables Utilizadas",
                    value=resultado_prediccion['model_info']['features_used'],
                    delta=None
                )
            
            # Información adicional
            st.subheader("📋 Datos Utilizados para la Predicción")
            
            if datos_desde_url is not None:
                # Mostrar datos cargados desde URL
                datos_mostrar = {
                    "Puntuación de lectura": f"{datos_validados['reading_score']}",
                    "Puntuación de escritura": f"{datos_validados['writing_score']}",
                    "Género": "Masculino" if datos_validados['gender'] == 1 else "Femenino",
                    "Tipo de almuerzo": "Estándar" if datos_validados['lunch'] == 1 else "Gratuito/Reducido",
                    "Curso de preparación": "Completado" if datos_validados['test_preparation_course'] == 1 else "No",
                    "Grupo étnico E": "Sí" if datos_validados['race_ethnicity_group_E'] == 1 else "No",
                    "Nivel educativo padres": "Solo Secundaria" if datos_validados['parental_level_of_education_high_school'] == 1 else "Otro nivel"
                }
                st.info("📥 Datos cargados desde URL")
            else:
                # Mostrar datos del formulario manual
                datos_mostrar = {
                    "Puntuación de lectura": f"{reading_score}",
                    "Puntuación de escritura": f"{writing_score}",
                    "Género": gender[0],
                    "Tipo de almuerzo": lunch[0],
                    "Curso de preparación": test_preparation_course[0],
                    "Grupo étnico E": race_ethnicity_group_E[0],
                    "Nivel educativo padres": parental_level_of_education_high_school[0]
                }
                st.info("✏️ Datos ingresados manualmente")
            
            for key, value in datos_mostrar.items():
                st.write(f"**{key}:** {value}")
            
            # Mostrar DataFrame validado
            # st.subheader("📊 Datos Validados (DataFrame)")
            # with st.expander("👁️ Ver DataFrame validado"):
            #     st.dataframe(df_validado)
            #     st.info(f"📈 DataFrame con {len(df_validado)} fila(s) y {len(df_validado.columns)} columna(s)")
            
            # st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error al realizar la predicción: {str(e)}")
    
    # Información adicional en la parte inferior
    st.markdown("---")
    st.subheader("ℹ️ Información del Modelo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Características del Modelo:**
        - Tipo: Regresión Lineal Optimizada
        - Precisión: 87.2% (R² = 0.872)
        - Variables de entrada: 7
        - Escala de calificaciones: 0-100
        """)
    
    with col2:
        st.info("""
        **Variables Utilizadas:**
        1. Género (Femenino/Masculino)
        2. Tipo de almuerzo (Estándar/Gratuito)
        3. Curso de preparación (Sí/No)
        4. Puntuación de lectura (0-100)
        5. Puntuación de escritura (0-100)
        6. Grupo étnico E (Sí/No)
        7. Nivel educativo padres (Secundaria/Otro)
        """)

if __name__ == "__main__":
    main()
