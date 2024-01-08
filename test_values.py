import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from io import BytesIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

def main():

    # Spécifiez l'URL de la page web que vous souhaitez scraper
    url = "https://www.eex.com/en/market-data/natural-gas/indices"  # Remplacez ceci par l'URL de votre choix

    # Téléchargez le contenu HTML de l'URL
    response = requests.get(url)

    # Vérifiez si la requête a réussi (statut 200)
    if response.status_code == 200:
        # Obtenez le contenu HTML de la réponse

        options = Options()
        options.add_argument("-headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(
            options=options,
        )

        # Chargement de la page
        driver.get(url)
        wait = WebDriverWait(driver, 100)

        cliq = wait.until(EC.presence_of_element_located((By.XPATH, "//body[1]/div[1]/div[2]/main[1]/div[1]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[3]/td[3]")))

        driver.implicitly_wait(100)
        # Faire défiler la page pour que l'élément soit visible
        driver.execute_script("arguments[0].click();", cliq)
        time.sleep(7)

        driver.implicitly_wait(100)

        updated_html = driver.page_source
        # Créez un objet BeautifulSoup
        driver.implicitly_wait(100)
        time.sleep(7)

        soup = BeautifulSoup(updated_html, "html.parser")

        # Utilisez le sélecteur CSS spécifié pour sélectionner la balise polyline
        time.sleep(7)
        svg_tag = soup.find("polyline")
        time.sleep(7)
        # Vérifiez si la balise polyline existe
        if svg_tag:
            print("jai trouve le svg")
            points_attribute = svg_tag.get('points')
            print(f"Points Attribute: {points_attribute}")

                # Split the points into individual coordinates
            coordinates = [tuple(map(float, point.split(','))) for point in points_attribute.split()]

                # Plot the graph for each polyline
            df = pd.DataFrame(coordinates, columns=['X', 'Y'])
            df = df[['Y', 'X']]
            # Convertir l'axe x en date
            start_date = datetime(2022, 12, 1)
            df['X'] = df['X'].apply(lambda x: start_date + timedelta(days=int(x)))

            # Définir les plages des axes
            price_range = [0, 160]
            date_range = [start_date, datetime.now() + timedelta(days=1)]
            # Utiliser Plotly Express pour créer le graphique
            fig = px.line(df, x='X', y='Y', labels={'X': 'Time', 'Y': 'Price (€)'}, title='Graphs over Time')

            fig.update_layout(xaxis=dict(range=date_range),yaxis=dict(range=price_range, autorange="reversed"),xaxis_title='Date', yaxis_title='Price (€)')
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig)

        else:
            print("Balise POLYLINE non trouvée dans le HTML.")

    else:
        print(f"Échec de la requête. Statut : {response.status_code}")


##ON RUN LE MAIN
if __name__ == "__main__":
    main()
