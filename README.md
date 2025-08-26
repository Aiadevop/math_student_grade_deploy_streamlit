# 📊 Aplicación de Predicción de Calificaciones Matemáticas - Versión Streamlit

Esta es la versión Streamlit de la aplicación de predicción de calificaciones matemáticas. Streamlit ofrece una interfaz web moderna y fácil de usar para aplicaciones de machine learning.

## 🚀 Características

- **Interfaz moderna**: Diseño limpio y responsive con Streamlit
- **Predicción en tiempo real**: Resultados instantáneos al hacer clic en el botón
- **Información detallada**: Sidebar con información del modelo y variables utilizadas
- **Validación de datos**: Verificación automática de rangos y tipos de datos
- **Métricas visuales**: Presentación clara de resultados con métricas y gráficos

## 📋 Requisitos

- Python 3.8 o superior
- Streamlit 1.28.0 o superior
- Las dependencias listadas en `requirements_streamlit.txt`

## 🛠️ Instalación

1. **Clonar el repositorio** (si no lo has hecho ya):
```bash
git clone <tu-repositorio>
cd formulario-educativo
```

2. **Instalar dependencias**:
```bash
pip install -r requirements_streamlit.txt
```

3. **Verificar que el modelo esté disponible**:
   - El archivo `app/models/lin_reg_model_opt.pkl` debe estar presente

## 🚀 Ejecución Local

Para ejecutar la aplicación localmente:

```bash
streamlit run streamlit_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## ☁️ Despliegue en Streamlit Cloud

### Opción 1: Streamlit Cloud (Recomendado)

1. **Crear cuenta en Streamlit Cloud**:
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub

2. **Desplegar la aplicación**:
   - Haz clic en "New app"
   - Selecciona tu repositorio
   - Establece:
     - **Main file path**: `streamlit_app.py`
     - **Python version**: 3.9 o superior

3. **Configurar variables de entorno** (si es necesario):
   - En la configuración de la app, puedes agregar variables de entorno

### Opción 2: Heroku

1. **Crear archivo `Procfile`**:
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Crear archivo `setup.sh`**:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"tu-email@ejemplo.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. **Desplegar en Heroku**:
```bash
heroku create tu-app-nombre
git add .
git commit -m "Agregar versión Streamlit"
git push heroku main
```

## 📊 Uso de la Aplicación

1. **Llenar el formulario**:
   - Ingresa las puntuaciones de lectura y escritura (0-100)
   - Selecciona el género del estudiante
   - Elige el tipo de almuerzo
   - Indica si completó el curso de preparación
   - Selecciona el grupo étnico
   - Especifica el nivel educativo de los padres

2. **Obtener predicción**:
   - Haz clic en "🔮 Predecir Calificación Matemática"
   - La aplicación mostrará:
     - Calificación matemática predicha (0-100)
     - Confianza del modelo (87.2%)
     - Número de variables utilizadas
     - Resumen de los datos ingresados

## 🔧 Configuración

### Archivo de configuración Streamlit

El archivo `.streamlit/config.toml` contiene la configuración personalizada:

- **Tema**: Colores personalizados para la aplicación
- **Servidor**: Configuración para despliegue
- **Navegador**: Configuración de estadísticas de uso

### Personalización

Puedes personalizar la aplicación modificando:

- **Colores**: Edita los valores en `config.toml`
- **CSS**: Modifica el CSS embebido en `streamlit_app.py`
- **Funcionalidad**: Agrega nuevas características en la función `main()`

## 📈 Ventajas de Streamlit

- **Desarrollo rápido**: Interfaz web con pocas líneas de código
- **Interactividad**: Widgets nativos y actualizaciones en tiempo real
- **Despliegue fácil**: Integración directa con Streamlit Cloud
- **Responsive**: Se adapta automáticamente a diferentes dispositivos
- **Comunidad activa**: Gran soporte y documentación

## 🔍 Diferencias con la versión Flask

| Característica | Flask | Streamlit |
|----------------|-------|-----------|
| **Interfaz** | HTML/CSS/JS personalizado | Widgets nativos |
| **Desarrollo** | Más código, más control | Menos código, más rápido |
| **Despliegue** | Más configuraciones | Más simple |
| **Interactividad** | JavaScript personalizado | Reactiva automática |
| **Mantenimiento** | Más complejo | Más simple |

## 🐛 Solución de Problemas

### Error: "No se pudo cargar el modelo"

1. Verifica que el archivo `lin_reg_model_opt.pkl` esté en la ubicación correcta
2. Asegúrate de que el archivo no esté corrupto
3. Revisa los permisos del archivo

### Error: "ModuleNotFoundError"

1. Instala todas las dependencias: `pip install -r requirements_streamlit.txt`
2. Verifica que estés usando la versión correcta de Python

### Error en Streamlit Cloud

1. Verifica que el archivo principal sea `streamlit_app.py`
2. Asegúrate de que todas las dependencias estén en `requirements_streamlit.txt`
3. Revisa los logs de despliegue en Streamlit Cloud

## 📞 Soporte

Si tienes problemas con la aplicación:

1. Revisa los logs de error en la consola
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el modelo esté disponible
4. Consulta la documentación de Streamlit: [docs.streamlit.io](https://docs.streamlit.io)

## 🎯 Próximas Mejoras

- [ ] Agregar gráficos de distribución de predicciones
- [ ] Implementar análisis de sensibilidad
- [ ] Agregar exportación de resultados
- [ ] Incluir más modelos de machine learning
- [ ] Agregar autenticación de usuarios

---

¡Disfruta usando tu aplicación de predicción de calificaciones matemáticas con Streamlit! 🎉

