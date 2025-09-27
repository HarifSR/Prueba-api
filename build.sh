#!/usr/bin/env bash
# exit on error
set -o errexit

# Actualiza e instala dependencias del sistema con sudo
sudo apt-get update
sudo apt-get install -y gnupg curl

# Agrega el repositorio de Microsoft
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
curl -fsSL https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Instala el driver de SQL Server
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Instala las dependencias de Python
pip install -r requirements.txt