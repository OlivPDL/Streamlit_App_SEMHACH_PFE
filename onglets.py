import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def display_weather_current(api_key,lat,lon):
    weather_df = get_weather_current(api_key, lat, lon)
# Create a Plotly figure for the weather forecast
    fig_weather = px.line(weather_df, x='Date et Heures', y='Temperature (°C)', labels={'Temperature (°C)': 'Temperature (°C)'}, title=' Températures Chevilly la Rue')
# Customize the layout if needed
    fig_weather.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=40, b=0), width=1000, height=400)
# Display the Plotly figure in Streamlit
    st.plotly_chart(fig_weather)


def get_weather_current(api_key, lat, lon):
    url = f'http://my.meteoblue.com/packages/basic-1h_basic-day?lat={lat}&lon={lon}&apikey={api_key}'
    response = requests.get(url)
    forecast_data = []
    if response.status_code == 200:
        data = response.json()

        times = data['data_1h']['time']
        temperatures = data['data_1h']['temperature']

        min_length = min(len(times), len(temperatures))

        for i in range(min_length):
            time = times[i]
            temp = temperatures[i]
            forecast_data.append({'Date et Heures': time, 'Temperature (°C)': temp})

        df = pd.DataFrame(forecast_data)
        return df
    else:
        st.error(f"Error fetching weather data. Error code: {response.status_code}")

def main():
    st.set_page_config(layout="wide")
    st.title('Mon application')

    # Créer les onglets
    titres_onglets = ['Sujet A', 'Sujet B', 'Sujet C']
    onglet1, onglet2, onglet3 = st.tabs(titres_onglets)

    # Ajouter du contenu à chaque onglet
    with onglet1:
        st.header('Sujet A')
        api_key = 'ZvHuOzV0QcNg7XsJ'
        lat = 48.77
        lon = 2.36
        display_weather_current(api_key, lat, lon)

    with onglet2:
        st.header('Sujet B')
        st.write('Contenu du sujet B')

    with onglet3:
        st.header('Sujet C')
        st.write('Contenu du sujet C')


##ON RUN LE MAIN
if __name__ == "__main__":
    main()
