import streamlit as st
from modules import display_weather_forecast,get_access_token, display_spot_prices,capture_screenshot_epex,capture_screenshot_eex,plot_forecasts,get_predictions,process_data,display_weather_current

def main():
    st.set_page_config(page_title="PFE MVP SEMHACH DASHBOARD",layout="wide")
    # Contenu des onglets
    titres_onglets = ['Météo', 'Filières de Production', 'Prix Spot Elec','Prix PEG Gaz']
    onglet1, onglet3, onglet2, onglet4 = st.tabs(titres_onglets)

     # Ajouter du contenu à chaque onglet
    with onglet1:

        #st.header('Météo Prévision 4 jours pas 3h')
        #api_key = '1a57c000e6a7972a8115a8e1aef41495'
        #lat = 48.77
        #lon = 2.36
        #display_weather_forecast(api_key, lat, lon)
        st.header('Prévision Météo Pas 1h')
        api_key = 'ZvHuOzV0QcNg7XsJ'
        lat = 48.77
        lon = 2.36
        #display_weather_current(api_key, lat, lon)

    with onglet2:
        st.header('Prévision Prix Electricité EPEX Spot & NordPool')
        client_id = "1e0de31c-6c1a-4166-b0f8-d194bc163b13"
        client_secret = "3cb2bbf9-74ab-45b0-84e4-94d557321d37"
        access_token = get_access_token(client_id, client_secret)

        if access_token:
            display_spot_prices(access_token)
        url2 = "https://www.epexspot.com/en/market-data?market_area=FR&trading_date=2023-11-23&delivery_date=2023-11-24&underlying_year=&modality=Auction&sub_modality=DayAhead&technology=&product=60&data_mode=table&period=&production_period="
        capture_screenshot_epex(url2)

    with onglet4:
            st.header('Prix PEG GAZ EEX')
            client_id = "1e0de31c-6c1a-4166-b0f8-d194bc163b13"
            client_secret = "3cb2bbf9-74ab-45b0-84e4-94d557321d37"
            access_token = get_access_token(client_id, client_secret)

            if access_token:
                url3 = "https://www.eex.com/en/market-data/natural-gas/indices"
                capture_screenshot_eex(url3)

    with onglet3:
        st.header('Prévision de Production par filière niveau National')
        st.write("Prévisions de production (J-3,J-2, J-1 et Infra J) en MW pour les filières (agrégée France, éolien, solaire, installations bénéficiant de l’Obligation d'achat avec EDF). Les données proviennent de programmes de production, d’estimations de production reçues ou directement d'estimations élaborées par RTE.")
        predictions = get_predictions(access_token)
        if predictions:
            production_type_forecasts = process_data(predictions)
            plot_forecasts(production_type_forecasts)

##ON RUN LE MAIN
if __name__ == "__main__":
    main()
