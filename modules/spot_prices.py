import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta


def display_spot_prices(access_token):
        today = datetime.now()
        date_format = "%Y-%m-%dT00:00:00+02:00"
        start_date = today.strftime(date_format)
        end_date = (today + timedelta(days=1)).strftime(date_format)

        st.write(f"Prévisions du lendemain à partir de 14h")

        api_url = "https://digital.iservices.rte-france.com/open_api/wholesale_market/v2/france_power_exchanges"
        params = {}

        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            spot_prices_data = response.json()
            #print(spot_prices_data)

            start_dates = [entry['start_date'] for entry in spot_prices_data['france_power_exchanges'][0]['values']]
            prices = [entry['price'] for entry in spot_prices_data['france_power_exchanges'][0]['values']]
            volumes = [entry['value'] for entry in spot_prices_data['france_power_exchanges'][0]['values']]

    # Convert start_dates to datetime objects for better plotting
            start_dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z") for date in start_dates]

    # Create a Plotly figure
            #fig = px.line(x=start_dates, y=prices, labels={'x': 'Date et Heure', 'y': 'Prix du MWh en €'}, title='Prix Echange Electricité en France')
            fig = make_subplots(specs=[[{"secondary_y": True}]])

                # Add traces for prices and volumes
            fig.add_trace(go.Scatter(x=start_dates, y=prices, mode='lines', name='Prix du MWh en €'), secondary_y=False)
            fig.add_trace(go.Scatter(x=start_dates, y=volumes, mode='markers', name='Volume du Marché (MW)'), secondary_y=True)

    # Customize the layout if needed
            fig.update_layout(xaxis=dict(tickangle=45), margin=dict(l=0, r=0, t=40, b=0), width=1900, height=350)

    # Display the Plotly figure in Streamlit
            st.plotly_chart(fig,use_container_width=True)
            #on ajoute de l'espace entre les elements
            st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.error(f"Error fetching spot prices. Error code: {response.status_code}")