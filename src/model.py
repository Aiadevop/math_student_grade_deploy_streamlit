# Entrenamiento, carga y predicción de modelos
import streamlit as st
import pickle
import numpy as np
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

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
            'models/lin_reg_model_opt.pkl',      # Segunda opción: carpeta models
            '../models/lin_reg_model_opt.pkl',
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


def hacer_prediccion(datos_extraidos, modelo):
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
        
        datos_para_modelo = [datos_extraidos[var] for var in variables_orden]
        
        # Debug: Mostrar los datos que van al modelo
        print("🔍 DEBUG - Datos que van al modelo:")
        for i, (var, valor) in enumerate(zip(variables_orden, datos_para_modelo)):
            print(f"  {i+1}. {var}: {valor} (tipo: {type(valor)})")
        
        print(f"📊 Lista completa de datos: {datos_para_modelo}")
        print(f"📊 Tipos de datos: {[type(d) for d in datos_para_modelo]}")
        
        # Convertir datos a array numpy
        datos_array = np.array(datos_para_modelo).reshape(1, -1)
        
        print(f"🔢 Array numpy resultante: {datos_array}")
        print(f"🔢 Shape del array: {datos_array.shape}")
        print(f"🔢 Dtype del array: {datos_array.dtype}")
        
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