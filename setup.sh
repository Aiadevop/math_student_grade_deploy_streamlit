#!/bin/bash

# Instalar dependencias del sistema
apt-get update
apt-get install -y python3-dev build-essential

# Instalar dependencias de Python
pip install --upgrade pip
pip install -r requirements_streamlit.txt

# Verificar instalación
python -c "import sklearn; print('scikit-learn version:', sklearn.__version__)"
python -c "import joblib; print('joblib version:', joblib.__version__)"
python -c "import numpy; print('numpy version:', numpy.__version__)"
