#!/bin/bash

# Actualizar el sistema
apt-get update

# Instalar dependencias del sistema necesarias para scikit-learn
apt-get install -y python3-dev build-essential gcc g++ libblas-dev liblapack-dev libatlas-base-dev

# Actualizar pip
pip install --upgrade pip setuptools wheel

# Instalar numpy primero (versión compatible)
pip install numpy==1.21.6 --no-cache-dir

# Instalar scikit-learn (versión compatible)
pip install scikit-learn==1.0.2 --no-cache-dir

# Instalar el resto de dependencias
pip install -r requirements.txt --no-cache-dir

# Verificar instalación
echo "=== Verificando instalación ==="
python -c "import numpy; print('✅ numpy version:', numpy.__version__)"
python -c "import sklearn; print('✅ scikit-learn version:', sklearn.__version__)"
python -c "import joblib; print('✅ joblib version:', joblib.__version__)"
python -c "import pandas; print('✅ pandas version:', pandas.__version__)"
python -c "import streamlit; print('✅ streamlit version:', streamlit.__version__)"
