import streamlit as st
import plotly.express as px
import requests
from datetime import datetime, timedelta

def afficher_texte_explicatif(nom_filiere):
    if nom_filiere == "AGGREGATED_CPC":
        return "Offre Agrégée (OA)."
    elif nom_filiere == "MDSETRF":
        return "Installations bénéficiant d'un contrat d'achat indexé aux prix de marché Trading Region France."
    elif nom_filiere == "MDSESTS":
        return "Installations bénéficiant d'un contrat d'achat indexé sur le tarif réglementé de fourniture de gaz STS."
    elif nom_filiere == "AGGREGATED_PROGRAMMABLE_FRANCE":
        return "Production des moyens programmables agrégée sur la France"
    elif nom_filiere == "AGGREGATED_NON_PROGRAMMABLE_FRANCE":
        return "Production des moyens dits fatals  agrégée sur la France."
    elif nom_filiere == "WIND":
        return "Production Eolien."
    elif nom_filiere == "SOLAR":
        return "Production Solaire."
    # Ajouter d'autres conditions au besoin

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

        explicatif_text = afficher_texte_explicatif(production_type)

        if explicatif_text is not None:
            title = f"Prévisions pour la Filière de Production : {explicatif_text}"
        else:
            title = "Prévisions pour la Filière de Production"


        fig.update_layout(
            title=title,
            xaxis_title="Date et Heure",
            yaxis_title="Production en MW",
            xaxis=dict(tickangle=45),
            margin=dict(l=0, r=0, t=40, b=0),
            width=1000,
            height=350,
            xaxis_tickformat='%Y-%m-%d %H:%M',
            xaxis_tickmode='linear',
            xaxis_dtick=2 * 60 * 60 * 1000,  # 2 hours in milliseconds
        )

        st.plotly_chart(fig,use_container_width=True)