#!/bin/bash

# Créez un dossier pour les pilotes et copiez le fichier geckodriver
mkdir drivers
cp geckodriver drivers/
chmod +x drivers/geckodriver

# Installez les dépendances Python depuis le fichier requirements.txt
pip install -r requirements.txt
