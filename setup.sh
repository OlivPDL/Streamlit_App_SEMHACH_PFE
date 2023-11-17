#!/bin/bash

# Créez un dossier pour les pilotes et copiez le fichier geckodriver
mkdir drivers
cp geckodriver.exe drivers/
chmod +x drivers/geckodriver.exe

# Installez les dépendances Python depuis le fichier requirements.txt
pip install -r requirements.txt
