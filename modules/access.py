
import streamlit as st
import requests
import base64


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