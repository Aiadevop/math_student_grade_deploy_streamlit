# 📊 Aplicación de Predicción de Calificaciones Matemáticas - Versión Streamlit

Esta es la versión Streamlit de la aplicación de predicción de calificaciones matemáticas. Streamlit ofrece una interfaz web moderna y fácil de usar para aplicaciones de machine learning.

## 🌐 **Aplicación Desplegada**

**¡La aplicación está funcionando en Streamlit Cloud!**

🔗 **Enlace de la aplicación:** [https://mathstudentgradedeployapp-wfdbf9xz5ma8v8pmfhwb2m.streamlit.app/](https://mathstudentgradedeployapp-wfdbf9xz5ma8v8pmfhwb2m.streamlit.app/)

## 🚀 Características

- **Interfaz moderna**: Diseño limpio y responsive con Streamlit
- **Predicción en tiempo real**: Resultados instantáneos al hacer clic en el botón
- **Información detallada**: Sidebar con información del modelo y variables utilizadas
- **Validación de datos**: Verificación automática de rangos y tipos de datos
- **Métricas visuales**: Presentación clara de resultados con métricas y gráficos
- **Carga desde URL (CSV)**: Procesa un CSV remoto y genera predicciones para todas las filas
- **Descarga de resultados**: Exporta el DataFrame con la columna `math_score_predicted` en CSV
- **Despliegue en la nube**: Aplicación accesible desde cualquier dispositivo

## 📋 Requisitos

- Python 3.8 o superior
- Streamlit 1.28.0 o superior
- Las dependencias listadas en `requirements.txt`

## 🛠️ Instalación Local

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Aiadevop/math_student_grade_deploy_streamlit.git
cd math_student_grade_deploy_streamlit
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Verificar que el modelo esté disponible**:
   - El archivo `models/lin_reg_model_opt.pkl` debe estar presente

## 🚀 Ejecución Local

Para ejecutar la aplicación localmente:

```bash
streamlit run streamlit_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## ☁️ Despliegue en Streamlit Cloud

### ✅ **Aplicación ya desplegada**

La aplicación está actualmente desplegada en Streamlit Cloud con la siguiente configuración:

- **Repositorio:** [Aiadevop/math_student_grade_deploy_streamlit](https://github.com/Aiadevop/math_student_grade_deploy_streamlit)
- **Archivo principal:** `streamlit_app.py`
- **Versión de Python:** 3.8
- **Archivo de dependencias:** `requirements.txt`

### 🔧 **Configuración utilizada**

Los siguientes archivos están configurados para el despliegue:

- **`requirements.txt`** - Dependencias de Python
- **`runtime.txt`** - Versión de Python (3.8)
- **`.streamlit/config.toml`** - Configuración de Streamlit

## 📊 Uso de la Aplicación

1. **Acceder a la aplicación**:
   - Ve a: [https://mathstudentgradedeployapp-wfdbf9xz5ma8v8pmfhwb2m.streamlit.app/](https://mathstudentgradedeployapp-wfdbf9xz5ma8v8pmfhwb2m.streamlit.app/)

2. **Cargar datos desde URL (opcional)**:
   - Proporciona un enlace a un archivo `.csv` y pulsa "Cargar"
   - La app procesará cada fila, generará `math_score_predicted` y mostrará:
     - Vista de los datos originales
     - Vista de los datos con la columna `math_score_predicted`
     - Botón para descargar el CSV con predicciones

3. **Llenar el formulario** (si no usas URL):
   - Ingresa las puntuaciones de lectura y escritura (0-100)
   - Selecciona el género del estudiante
   - Elige el tipo de almuerzo
   - Indica si completó el curso de preparación
   - Selecciona el grupo étnico
   - Especifica el nivel educativo de los padres

4. **Obtener predicción**:
   - Haz clic en "🔮 Predecir Calificación Matemática"
   - La aplicación mostrará:
     - Calificación matemática predicha (0-100)
     - Confianza del modelo (87.2%)
     - Número de variables utilizadas
     - Resumen de los datos ingresados

## 🔧 Configuración del Proyecto

### Archivos de configuración

- **`requirements.txt`** - Dependencias principales del proyecto
- **`runtime.txt`** - Versión de Python para despliegue
- **`.streamlit/config.toml`** - Configuración específica de Streamlit

### Estructura del proyecto

```
formulario-educativo-streamlit/
├── streamlit_app.py          # Aplicación principal
├── requirements.txt          # Dependencias
├── runtime.txt              # Versión de Python
├── models/
│   └── lin_reg_model_opt.pkl # Modelo entrenado
├── src/                      # Código fuente (procesado de datos y modelo)
│   ├── data.py               # Carga desde URL y procesamiento de DataFrame
│   ├── model.py              # Carga del modelo y predicción
│   └── __init__.py
├── .streamlit/
│   └── config.toml          # Configuración de Streamlit
└── README.md                # Este archivo
```

## 📈 Características del Modelo

- **Tipo:** Regresión Lineal Optimizada
- **Precisión:** 87.2% (R² = 0.872)
- **Variables de entrada:** 7
- **Escala de calificaciones:** 0-100

### Variables utilizadas:
1. Género (Femenino/Masculino)
2. Tipo de almuerzo (Estándar/Gratuito)
3. Curso de preparación (Sí/No)
4. Puntuación de lectura (0-100)
5. Puntuación de escritura (0-100)
6. Grupo étnico E (Sí/No)
7. Nivel educativo padres (Secundaria/Otro)

## 🐛 Solución de Problemas

### Error: "No se pudo cargar el modelo"
- Verifica que el archivo `models/lin_reg_model_opt.pkl` esté presente
- Asegúrate de que las dependencias estén instaladas correctamente

### Error: "ModuleNotFoundError"
- Instala las dependencias: `pip install -r requirements.txt`
- Verifica que estés usando Python 3.8 o superior

### Error en Streamlit Cloud
- La aplicación está configurada correctamente para Streamlit Cloud
- Si hay problemas, verifica los logs en la configuración de la app

### Predicciones desde URL no aparecen
- Asegúrate de que la URL termine en `.csv`
- El archivo debe incluir columnas equivalentes a: `reading_score`, `writing_score`, `gender`, `lunch`, `test_preparation_course`, `race_ethnicity_group_E`, `parental_level_of_education_high_school`. La app admite nombres alternativos comunes (ver `src/data.py`).

## 📞 Soporte

Si tienes problemas con la aplicación:

1. **Aplicación desplegada:** Revisa si funciona en el enlace proporcionado
2. **Ejecución local:** Verifica que todas las dependencias estén instaladas
3. **Documentación:** Consulta la documentación de Streamlit: [docs.streamlit.io](https://docs.streamlit.io)

## 🎯 Próximas Mejoras

- [ ] Agregar gráficos de distribución de predicciones
- [ ] Implementar análisis de sensibilidad
- [ ] Agregar exportación de resultados
- [ ] Incluir más modelos de machine learning
- [ ] Agregar autenticación de usuarios
- [ ] Implementar historial de predicciones

## 🌟 **¡Aplicación Funcionando!**

La aplicación está **completamente operativa** y disponible en:
**https://mathstudentgradedeployapp-wfdbf9xz5ma8v8pmfhwb2m.streamlit.app/**

¡Disfruta usando tu aplicación de predicción de calificaciones matemáticas! 🎉

