#import matplotlib
import streamlit as st
import os
from selenium.webdriver import FirefoxOptions
import plotly.express as px
import requests
import base64
from datetime import datetime, timedelta
#import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image


def get_access_token(client_id, client_secret):
    auth_url = "https://digital.iservices.rte-france.com/token/oauth/"
    data = {"grant_type": "client_credentials"}

    credentials = f"{client_id}:{client_secret}"
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {credentials_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(auth_url, data=data, headers=headers)

    if response.status_code == 200:
        access_token_data = response.json()
        return access_token_data.get("access_token")
    else:
        st.error(f"Error fetching access token. Error code: {response.status_code}")

def get_weather_forecast(api_key, lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        forecast_data = []
        for forecast in data['list']:
            date_time = pd.to_datetime(forecast['dt_txt'])
            temperature = forecast['main']['temp'] - 273
            forecast_data.append({'Date et Heures': date_time, 'Temperature (°C)': temperature})

        df = pd.DataFrame(forecast_data)
        return df
    else:
        st.error(f"Error fetching weather data. Error code: {response.status_code}")

def display_spot_prices(access_token):
        today = datetime.now()
        date_format = "%Y-%m-%dT00:00:00+02:00"
        start_date = today.strftime(date_format)
        end_date = (today + timedelta(days=1)).strftime(date_format)

        #st.write(f"Start: {start_date}, End: {end_date}")

        api_url = "https://digital.iservices.rte-france.com/open_api/wholesale_market/v2/france_power_exchanges"
        params = {}

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            spot_prices_data = response.json()
            #print(spot_prices_data)

            start_dates = [entry['start_date'] for entry in spot_prices_data['france_power_exchanges'][0]['values']]
            prices = [entry['price'] for entry in spot_prices_data['france_power_exchanges'][0]['values']]

    # Convert start_dates to datetime objects for better plotting
            start_dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z") for date in start_dates]

    # Create a Plotly figure
            fig = px.line(x=start_dates, y=prices, labels={'x': 'Date et Heure', 'y': 'Prix du MWh en €'}, title='Prix Echange Electricité en France')

    # Customize the layout if needed
            fig.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=89, b=0))

    # Display the Plotly figure in Streamlit
            st.plotly_chart(fig)
            #on ajoute de l'espace entre les elements
            st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.error(f"Error fetching spot prices. Error code: {response.status_code}")

def display_weather_forecast(api_key,lat,lon):
    weather_df = get_weather_forecast(api_key, lat, lon)
# Create a Plotly figure for the weather forecast
    fig_weather = px.line(weather_df, x='Date et Heures', y='Temperature (°C)', labels={'Temperature (°C)': 'Temperature (°C)'}, title='Prévisions Températures Chevilly la Rue')
# Customize the layout if needed
    fig_weather.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=50, b=0))
# Display the Plotly figure in Streamlit
    st.plotly_chart(fig_weather)





def get_solar_forecasts(access_token):
    # Appel à l'API
    api_url = "https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts?production_type=SOLAR&type=D-1&start_date=2023-11-16T00:00:00%2B02:00&end_date=2023-11-18T00:00:00%2B02:00"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # Traitement des données des prévisions
        predictions_data = response.json()
        forecasts = predictions_data.get("forecasts", [])

        # Extraction des dates et des valeurs
        dates = []
        values = []
        for forecast in forecasts:
            for value in forecast.get("values", []):
                start_date = value.get("start_date")
                forecast_value = value.get("value")
                if start_date and forecast_value:
                    dates.append(datetime.fromisoformat(start_date))
                    values.append(forecast_value)

        return dates, values
    else:
        print(f"Échec de la demande de prévisions : {response.status_code}")
        return None, None



def plot_solar_forecasts(dates,values):
    # Récupération des prévisions solaires


    if dates and values:
        # Création du graphique Plotly
        fig = px.line(x=dates, y=values, labels={'x': 'Date and Time', 'y': 'MW'}, title='Prévisions Production Solaires en France')

        # Personnalisation de la mise en page si nécessaire
        fig.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=89, b=0))

        # Afficher le graphique Plotly Express dans Streamlit
        st.plotly_chart(fig)

        # Ajouter de l'espace entre les éléments
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.error("Les données des prix du marché sont vides.")

def get_predictions(access_token):
    today = datetime.now()
    date_format = "%Y-%m-%dT00:00:00+02:00"
    start_date = today.strftime(date_format)
    end_date = (today + timedelta(days=1)).strftime(date_format)

    api_url = "https://digital.iservices.rte-france.com/open_api/generation_forecast/v2/forecasts"
    params = {"production_type": "AGGREGATED_FRANCE", "type": "D-2", "start_date": start_date, "end_date": end_date}
    headers = {"Authorization": f"Bearer {access_token}"}
    predictions_response = requests.get(api_url, headers=headers)

    if predictions_response.status_code == 200:
        predictions_data = predictions_response.json()
        return predictions_data["forecasts"]
    else:
        st.error(f"Failed to request predictions: {predictions_response.status_code}")
        return None

def process_data(predictions):
    production_type_forecasts = {}

    for forecast in predictions:
        forecast_type = forecast.get("forecast_type_fr")
        sub_type = forecast.get("sub_type")
        production_type = forecast.get("production_type")
        values = forecast.get("values", [])

        if production_type not in production_type_forecasts:
            production_type_forecasts[production_type] = {
                "forecast_type": forecast_type,
                "sub_types": {},
            }

        if sub_type not in production_type_forecasts[production_type]["sub_types"]:
            production_type_forecasts[production_type]["sub_types"][sub_type] = {
                "dates": [],
                "values": [],
            }

        for value in values:
            start_date = value.get("start_date")
            forecast_value = value.get("value")
            if start_date and forecast_value:
                production_type_forecasts[production_type]["sub_types"][sub_type]["dates"].append(
                    datetime.fromisoformat(start_date)
                )
                production_type_forecasts[production_type]["sub_types"][sub_type]["values"].append(
                    forecast_value
                )

    return production_type_forecasts

def plot_forecasts(production_type_forecasts):
    for production_type, data in production_type_forecasts.items():
        forecast_type = data["forecast_type"]
        sub_types = data["sub_types"]

        fig = px.line()

        for sub_type, sub_data in sub_types.items():
            dates = sub_data["dates"]
            values = sub_data["values"]

            if dates and values:
                sorted_data = sorted(zip(dates, values), key=lambda x: x[0])
                dates, values = zip(*sorted_data)

                fig.add_trace(px.line(x=dates, y=values).data[0])

        title = f"Prévisions pour la Filière de Production : {production_type})"
        fig.update_layout(
            title=title,
            xaxis_title="Date et Heure",
            yaxis_title="Production en MW",
            xaxis=dict(tickangle=45),
            xaxis_tickformat='%Y-%m-%d %H:%M',
            xaxis_tickmode='linear',
            xaxis_dtick=2 * 60 * 60 * 1000,  # 2 hours in milliseconds
        )

        st.plotly_chart(fig)

def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()

def capture_screenshot_bourso(url, element_id):
    path_to_geckodriver = os.path.abspath("./drivers/geckodriver")
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    # Utilisation du webdriver pour Firefox
    options.add_argument(f"webdriver.gecko.driver={path_to_geckodriver}")
    driver = webdriver.Firefox(options=options)

    try:
        # Chargement de la page
        driver.get(url)
        driver.implicitly_wait(10)

        # Recherche de l'élément contenant le graphique des prix
        chart_container = driver.find_element(By.ID, element_id)

        # Capture d'écran de l'élément contenant le graphique
        screenshot = chart_container.screenshot_as_png

        # Affichage de l'image dans l'application Streamlit
        st.image(BytesIO(screenshot), caption='Graphique Evolution Prix du Gaz Naturel ')

    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")

    finally:
        # Fermeture du navigateur
        driver.quit()

def main():
    st.title("MVP PFE SEMHACH DASHBOARD")
    st.markdown("<br>", unsafe_allow_html=True)
#st.header("Electricity Exchange Prices in France")
    client_id = "1e0de31c-6c1a-4166-b0f8-d194bc163b13"
    client_secret = "3cb2bbf9-74ab-45b0-84e4-94d557321d37"
    access_token = get_access_token(client_id, client_secret)
    if access_token:
        display_spot_prices(access_token)
        #url2 = "https://www.eex.com/en/market-data/natural-gas/indices#%7B%22snippetpicker%22%3A%221053%22%7D"
        #capture_screenshot_eex(url2, element_id)
        api_key = '1a57c000e6a7972a8115a8e1aef41495'
        lat = 48.77
        lon = 2.36
        display_weather_forecast(api_key, lat, lon)
        url1 = "https://www.boursorama.com/bourse/matieres-premieres/cours/_NG/"
        # ID de l'élément contenant le graphique
        element_id = "overlay-eod_container1"
        capture_screenshot_bourso(url1, element_id)
        predictions = get_predictions(access_token)
        if predictions:
            production_type_forecasts = process_data(predictions)
            plot_forecasts(production_type_forecasts)

        dates, values = get_solar_forecasts(access_token)
        plot_solar_forecasts(dates,values)

##ON RUN LE MAIN
if __name__ == "__main__":
    main()
