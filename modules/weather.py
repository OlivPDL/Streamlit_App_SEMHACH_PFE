import streamlit as st
import plotly.express as px
import requests
import pandas as pd


def display_weather_forecast(api_key,lat,lon):
    weather_df = get_weather_forecast(api_key, lat, lon)
# Create a Plotly figure for the weather forecast
    fig_weather = px.line(weather_df, x='Date et Heures', y='Temperature (°C)', labels={'Temperature (°C)': 'Temperature (°C)'}, title='Prévisions Températures Chevilly la Rue')
# Customize the layout if needed
    fig_weather.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=40, b=0), width=1300, height=500)
# Display the Plotly figure in Streamlit
    st.plotly_chart(fig_weather,use_container_width=True)


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


def display_weather_current(api_key,lat,lon):
    weather_df = get_weather_current(api_key, lat, lon)
# Create a Plotly figure for the weather forecast
    fig_weather = px.line(weather_df, x='Date et Heures', y='Temperature (°C)', labels={'Temperature (°C)': 'Temperature (°C)'}, title=' Températures Chevilly la Rue')
# Customize the layout if needed
    fig_weather.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=40, b=0), width=1900, height=350)
# Display the Plotly figure in Streamlit
    st.plotly_chart(fig_weather,use_container_width=True)


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