import streamlit as st
from selenium import webdriver
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def capture_screenshot_epex(url):

    options = Options()
    options.add_argument('-headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        options=options,
    )

    try:
        # Chargement de la page
        driver.get(url)
        driver.implicitly_wait(10)
        accept_cookie_button = driver.find_element(By.ID, "edit-acceptationbuttonmobile")
        #accept_cookie_button.click()
        driver.execute_script("arguments[0].click();", accept_cookie_button)
        # Recherche de l'élément contenant le graphique des prix
        #chart_container = driver.find_element(By.CLASS_NAME, "custom-tables 60min")
        wait = WebDriverWait(driver, 10)
        #element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'custom-tables 60min')))
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class=\'custom-tables 60min\']')))
        driver.set_window_size(3000, 2000)
        # Capture d'écran de l'élément contenant le graphique
        screenshot = element.screenshot_as_png

        # Affichage de l'image dans l'application Streamlit
        st.image(BytesIO(screenshot), caption='Graphique Evolution Prix Elec ')

    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")

    finally:
        # Fermeture du navigateur
        driver.quit()

def capture_screenshot_eex(url):

    options = Options()
    options.add_argument('-headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(
        options=options,
    )

    try:
        # Chargement de la page
        driver.get(url)
        wait = WebDriverWait(driver, 100)

        cliq = wait.until(EC.presence_of_element_located((By.XPATH, "//body[1]/div[1]/div[2]/main[1]/div[1]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[3]/td[3]")))

        driver.implicitly_wait(100)
        # Faire défiler la page pour que l'élément soit visible
        driver.execute_script("arguments[0].click();", cliq)

        driver.implicitly_wait(100)
        # Créez un objet BeautifulSoup
        driver.implicitly_wait(100)

        accept_cookie_button = driver.find_element(By.XPATH, "//body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/form[1]/input[2]")

        driver.implicitly_wait(100)
        driver.execute_script("arguments[0].click();", accept_cookie_button)
        time.sleep(6)


        #elem = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='mv-pane-surface']//*[name()='svg']")))
        elem = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[@class='mv-quote-inline-chart']//td")))

        driver.implicitly_wait(100)

        driver.set_window_size(3000, 2000)

        # Capture d'écran de l'élément contenant le graphique
        screenshot = elem.screenshot_as_png

        print(elem)

        driver.implicitly_wait(100)
        # Affichage de l'image dans l'application Streamlit
        st.image(BytesIO(screenshot), caption=' Prix GAZ EEX ')



    except Exception as e:
        st.error(f"Une erreur s'est produite : {str(e)}")
        logs = driver.get_log('browser')
        for log in logs:
            print(log)

    finally:
        # Fermeture du navigateur
        driver.quit()