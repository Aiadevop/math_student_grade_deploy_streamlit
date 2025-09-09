# Funciones para cargar y procesar datos

# Validar los datos introducidos CSV o formulario
import pandas as pd

def validar_datos(datos):
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
            resultado[var] = datos[var]
        
        # Agregar información sobre las variables validadas
        resultado['_variables_validadas'] = variables_requeridas
        resultado['_validado'] = True
        
        # Crear DataFrame con las variables validadas
        df_validado = pd.DataFrame([resultado])
        
        return resultado, df_validado
        
    except Exception as e:
        raise ValueError(f"Error al validar datos: {str(e)}")

def cargar_datos_desde_url(url):
    """
    Cargar datos desde una URL (solo archivos CSV)
    """
    try:
        # Validar que la URL no esté vacía
        if not url or not url.strip():
            raise ValueError("La URL no puede estar vacía")
        
        # Validar que la URL termine en .csv
        if not url.lower().endswith('.csv'):
            raise ValueError("Solo se permiten archivos CSV. La URL debe terminar en .csv")
        
        # Hacer petición HTTP
        import requests
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        
        # Verificar que el content-type sea CSV
        content_type = response.headers.get('content-type', '').lower()
        if 'csv' not in content_type and 'text/plain' not in content_type:
            raise ValueError(f"El archivo no parece ser un CSV válido. Content-Type: {content_type}")
        
        # Cargar como CSV
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        
        return df, f"Datos CSV cargados desde: {url}"
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error al acceder a la URL: {str(e)}")
    except pd.errors.EmptyDataError:
        raise ValueError("El archivo CSV está vacío o no contiene datos válidos")
    except pd.errors.ParserError as e:
        raise ValueError(f"Error al parsear el archivo CSV: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error inesperado al cargar datos: {str(e)}")

def procesar_datos_desde_dataframe(df):
    """
    Procesar un DataFrame para extraer los datos necesarios para el modelo
    """
    try:
        # Mapear nombres de columnas comunes
        column_mapping = {
            'reading_score': ['reading score','reading_score', 'reading', 'read_score', 'lectura'],
            'writing_score': ['writing score','writing_score', 'writing', 'write_score', 'escritura'],
            'gender': ['gender', 'sex', 'genero', 'género'],
            'lunch': ['lunch', 'almuerzo', 'lunch_type'],
            'test_preparation_course': ['test preparation course','test_preparation_course', 'preparation', 'curso_preparacion'],
            'race_ethnicity_group_E': ['race_ethnicity_group_E', 'race', 'ethnicity', "race/ethnicity"],
            'parental_level_of_education_high_school': ['parental_level_of_education_high_school', 'parental_level_of_education', 'parental level of education', 'parent_education', 'educacion_padres']
        }
        
        # Buscar columnas que coincidan
        datos_extraidos = {}
        for key, posibles_nombres in column_mapping.items():
            columna_encontrada = None
            for nombre in posibles_nombres:
                if nombre in df.columns:
                    columna_encontrada = nombre
                    break
            
            if columna_encontrada is not None:
                # Tomar el primer valor del DataFrame
                valor = df[columna_encontrada].iloc[0]
                
                # Convertir valores categóricos a numéricos si es necesario
                if key in ['gender', 'lunch', 'test_preparation_course', 'race_ethnicity_group_E', 'parental_level_of_education_high_school']:
                    if isinstance(valor, str):
                        # Mapear valores de texto a números
                        if key == 'gender':
                            valor = 1 if valor.lower() in ['male', 'masculino', 'm'] else 0
                        elif key == 'lunch':
                            valor = 1 if valor.lower() in ['standard', 'estándar', 'estandar'] else 0
                        elif key == 'test_preparation_course':
                            valor = 1 if valor.lower() in ['completed', 'completado', 'yes', 'sí', 'si'] else 0
                        elif key == 'race_ethnicity_group_E':
                            valor = 1.0 if valor.lower() in ['group e', 'group E', 'grupo e', 'grupo E', 'e', 'yes', 'sí', 'si'] else 0.0
                        elif key == 'parental_level_of_education_high_school':
                            valor = 1.0 if valor.lower() in ['high school', 'secundaria', 'high_school'] else 0.0
                
                datos_extraidos[key] = valor
            else:
                raise ValueError(f"No se encontró la columna para {key}. Columnas disponibles: {list(df.columns)}")
        
        # Debug: Mostrar los datos extraídos
        print("🔍 DEBUG - Datos extraídos:")
        for key, value in datos_extraidos.items():
            print(f"  {key}: {value} (tipo: {type(value)})")
        
        return datos_extraidos
        
    except Exception as e:
        print(f"❌ ERROR en procesar_datos_desde_dataframe: {str(e)}")
        raise ValueError(f"Error al procesar datos del DataFrame: {str(e)}")
