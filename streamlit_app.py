#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Streamlit para predicción de calificaciones matemáticas
Versión Streamlit de la aplicación Flask
"""

import streamlit as st
import pickle
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Intentar importar joblib para mejor compatibilidad
try:
    from joblib import load as joblib_load
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    st.warning("⚠️ joblib no disponible, usando pickle")

# Verificar que scikit-learn esté disponible
try:
    import sklearn
    SKLEARN_AVAILABLE = True
    # st.success(f"✅ scikit-learn disponible - versión: {sklearn.__version__}")
except ImportError:
    SKLEARN_AVAILABLE = False
    # st.error("❌ scikit-learn no está disponible.")
    # st.error("🔧 Problema de instalación en Streamlit Cloud")
    # st.info("💡 Soluciones:")
    # st.info("1. Verifica que requirements.txt esté en la raíz del proyecto")
    # st.info("2. Asegúrate de que la versión de Python sea 3.9+")
    # st.info("3. Revisa los logs de deployment en Streamlit Cloud")
    
    # Mostrar información de depuración
    # st.subheader("🔍 Información de Depuración")
    # st.code("""
    # Comandos para verificar en Streamlit Cloud:
    # pip list | grep scikit-learn
    # python -c "import sklearn; print(sklearn.__version__)"
    # """)

# Configuración de la página
st.set_page_config(
    page_title="📊 Predicción de Calificaciones Matemáticas",
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

@st.cache_resource
def cargar_modelo():
    """
    Cargar el modelo entrenado lin_reg_model_opt
    """
    # Verificar que scikit-learn esté disponible
    if not SKLEARN_AVAILABLE:
        st.error("❌ scikit-learn no está disponible. No se puede cargar el modelo.")
        return None, None
    
    try:
        # Buscar el archivo del modelo en diferentes ubicaciones posibles
        posibles_rutas = [
            'app/models/lin_reg_model_opt.pkl',  # Primera opción: carpeta app/models
            'models/lin_reg_model_opt.pkl',      # Segunda opción: carpeta models
            'model/lin_reg_model_opt.pkl',
            'lin_reg_model_opt.pkl',             # Fallback: raíz del proyecto
            '../app/models/lin_reg_model_opt.pkl',
            '../models/lin_reg_model_opt.pkl',
            '../model/lin_reg_model_opt.pkl',
            '../lin_reg_model_opt.pkl'
        ]
        
        modelo = None
        ruta_modelo = None
        
        for ruta in posibles_rutas:
            if Path(ruta).exists():
                try:
                    # Intentar primero con joblib si está disponible
                    if JOBLIB_AVAILABLE:
                        try:
                            modelo = joblib_load(ruta)
                            ruta_modelo = ruta
                            return modelo, ruta_modelo
                        except Exception as joblib_error:
                            # st.warning(f"⚠️ joblib falló, intentando pickle: {str(joblib_error)}")
                            pass
                    
                    # Si joblib no funciona, intentar con pickle
                    with open(ruta, 'rb') as f:
                        # Intentar con diferentes protocolos de pickle
                        try:
                            modelo = pickle.load(f)
                        except Exception as pickle_error:
                            try:
                                f.seek(0)
                                modelo = pickle.load(f, encoding='latin1')
                            except Exception as pickle_error2:
                                # Intentar con protocolo más antiguo
                                try:
                                    f.seek(0)
                                    modelo = pickle.load(f, fix_imports=True, encoding='latin1')
                                except Exception as pickle_error3:
                                    raise pickle_error3
                    
                    ruta_modelo = ruta
                    return modelo, ruta_modelo
                    
                except Exception as load_error:
                    continue
        
        if modelo is None:
            # st.error("❌ No se pudo cargar el modelo desde ninguna ubicación")
            # st.warning("⚠️ Esto puede deberse a incompatibilidad de versiones entre numpy/scikit-learn")
            # st.info("💡 Solución: El modelo fue guardado con una versión diferente de numpy")
            # st.info("🔧 Intenta usar versiones más antiguas: numpy==1.21.6, scikit-learn==1.0.2")
            return None, None
        
    except Exception as e:
        # st.error(f"❌ Error al cargar el modelo: {str(e)}")
        # st.info(f"🔧 Sugerencia: Verifica que el modelo se guardó correctamente con pickle")
        return None, None

def validar_datos_formulario(datos):
    """
    Validar y preparar los datos del formulario
    """
    try:
        # Variables requeridas del formulario (en el orden correcto del modelo)
        variables_requeridas = [
            'gender', 'lunch', 'test_preparation_course', 
            'reading_score', 'writing_score', 'race_ethnicity_group_E', 
            'parental_level_of_education_high_school'
        ]
        
        # Verificar que todas las variables estén presentes
        for var in variables_requeridas:
            if var not in datos:
                raise ValueError(f"Variable faltante: {var}")
        
        # Validar y convertir las variables a float
        resultado = datos.copy()
        for var in variables_requeridas:
            resultado[var] = float(datos[var])
        
        # Agregar información sobre las variables validadas
        resultado['_variables_validadas'] = variables_requeridas
        resultado['_validado'] = True
        
        return resultado
        
    except Exception as e:
        raise ValueError(f"Error al validar datos: {str(e)}")

def hacer_prediccion(datos_validados, modelo):
    """
    Hacer predicción usando el modelo cargado
    """
    try:
        # Preparar datos para el modelo (en el orden correcto)
        variables_orden = [
            'gender', 'lunch', 'test_preparation_course', 
            'reading_score', 'writing_score', 'race_ethnicity_group_E', 
            'parental_level_of_education_high_school'
        ]
        
        datos_para_modelo = [datos_validados[var] for var in variables_orden]
        
        # Convertir datos a array numpy
        datos_array = np.array(datos_para_modelo).reshape(1, -1)
        
        # Hacer predicción
        prediccion = modelo.predict(datos_array)
        
        # Obtener el valor de la predicción (ya en escala original)
        math_score = float(prediccion[0])
        
        # Validar que el resultado esté en el rango válido (0-100)
        if math_score < 0:
            st.warning(f"⚠️ Predicción negativa detectada: {math_score}, estableciendo en 0")
            math_score = 0
        elif math_score > 100:
            st.warning(f"⚠️ Predicción mayor a 100 detectada: {math_score}, estableciendo en 100")
            math_score = 100
        
        # Usar la precisión real del modelo basada en validación cruzada
        # R² = 0.872151 (87.2% de precisión)
        confidence = 0.872151
        
        return {
            "math_score": round(math_score, 2),
            "confidence": round(confidence, 3) if confidence is not None else None,
            "model_info": {
                "type": type(modelo).__name__,
                "features_used": len(datos_para_modelo)
            }
        }
        
    except Exception as e:
        st.error(f"❌ Error en predicción: {str(e)}")
        raise

def main():
    """
    Función principal de la aplicación Streamlit
    """
    # Información de depuración (comentada para producción)
    # st.sidebar.header("🔧 Información de Depuración")
    # st.sidebar.info(f"📦 scikit-learn: {SKLEARN_AVAILABLE}")
    # st.sidebar.info(f"📦 joblib: {JOBLIB_AVAILABLE}")
    
    # Información adicional para Streamlit Cloud (comentada para producción)
    # st.sidebar.header("☁️ Streamlit Cloud Info")
    # st.sidebar.info("📁 Archivos de configuración:")
    # st.sidebar.info("✅ requirements.txt")
    # st.sidebar.info("✅ runtime.txt")
    # st.sidebar.info("✅ .streamlit/config.toml")
    
    # Información de versiones (comentada para producción)
    # st.sidebar.header("📦 Versiones")
    # try:
    #     import numpy as np
    #     st.sidebar.info(f"numpy: {np.__version__}")
    # except:
    #     st.sidebar.error("numpy: No disponible")
    
    # try:
    #     import sklearn
    #     st.sidebar.info(f"scikit-learn: {sklearn.__version__}")
    # except:
    #     st.sidebar.error("scikit-learn: No disponible")
    
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
            options=[("Femenino", 0), ("Masculino", 1)],
            format_func=lambda x: x[0],
            help="Selecciona el género del estudiante"
        )
        
        lunch = st.selectbox(
            "🍽️ Tipo de almuerzo",
            options=[("Estándar", 1), ("Gratuito/Reducido", 0)],
            format_func=lambda x: x[0],
            help="Selecciona el tipo de almuerzo del estudiante"
        )
    
    with col2:
        test_preparation_course = st.selectbox(
            "📚 Curso de preparación",
            options=[("No", 0), ("Completado", 1)],
            format_func=lambda x: x[0],
            help="Indica si el estudiante completó el curso de preparación"
        )
        
        race_ethnicity_group_E = st.selectbox(
            "🌍 Grupo étnico E",
            options=[("No", 0), ("Sí", 1)],
            format_func=lambda x: x[0],
            help="Indica si el estudiante pertenece al grupo étnico E"
        )
        
        parental_level_of_education_high_school = st.selectbox(
            "🎓 Nivel educativo de los padres",
            options=[("Otro nivel", 0), ("Solo Secundaria", 1)],
            format_func=lambda x: x[0],
            help="Indica si los padres solo tienen educación secundaria"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botón de predicción
    if st.button("🔮 Predecir Calificación Matemática", type="primary"):
        try:
            # Preparar datos
            datos = {
                'reading_score': reading_score,
                'writing_score': writing_score,
                'gender': gender[1],
                'lunch': lunch[1],
                'test_preparation_course': test_preparation_course[1],
                'race_ethnicity_group_E': race_ethnicity_group_E[1],
                'parental_level_of_education_high_school': parental_level_of_education_high_school[1]
            }
            
            # Validar datos
            datos_validados = validar_datos_formulario(datos)
            
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
            st.subheader("📋 Datos Ingresados")
            datos_mostrar = {
                "Puntuación de lectura": f"{reading_score}",
                "Puntuación de escritura": f"{writing_score}",
                "Género": gender[0],
                "Tipo de almuerzo": lunch[0],
                "Curso de preparación": test_preparation_course[0],
                "Grupo étnico E": race_ethnicity_group_E[0],
                "Nivel educativo padres": parental_level_of_education_high_school[0]
            }
            
            for key, value in datos_mostrar.items():
                st.write(f"**{key}:** {value}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
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

