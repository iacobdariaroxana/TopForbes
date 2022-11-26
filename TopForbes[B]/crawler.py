import re
import time
import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import config_database


def insert_billionaires(billionaires_info):
    connection = None
    try:
        params = config_database()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        query = "DELETE FROM billionaires"
        cursor.execute(query)
        query = "INSERT INTO billionaires(rank,name,net_worth,age,country_of_citizenship,source,category) VALUES(%s,%s," \
                "%s,%s,%s,%s,%s) RETURNING id "
        cursor.executemany(query, billionaires_info)
        
        connection.commit()
        cursor.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if connection:
            connection.close()


def extract_billionaire_info(billionaires):
    billionaires_info = []
    for billionaire in billionaires:
        rank = billionaire.find_next('div', {'class': 'rank'}).text[:-1]
        name = billionaire.find_next('div', {'class': 'personName'}).text
        net_worth = billionaire.find_next('div', {'class': 'netWorth'}).text
        net_worth_number = re.search(r'\d+\.?\d*', net_worth)[0]
        age = billionaire.find_next('div', {'class': 'age'}).text
        if age == "N/A":
            age = None
        country_of_citizenship = billionaire.find_next('div', {'class': 'countryOfCitizenship'}).text
        source = billionaire.find_next('div', {'class': 'source'}).text
        category = billionaire.find_next('div', {'class': 'category'}).text
        billionaires_info.append((rank, name, net_worth_number, age, country_of_citizenship, source, category))
    return billionaires_info


def find_billionaires(url):
    browser = webdriver.Chrome()
    browser.get(url)
    cookies = browser.find_element(value="truste-consent-button")
    cookies.send_keys(Keys.ENTER)
    billionaires = []
    while len(billionaires) < 200:
        time.sleep(0.5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        billionaires = soup.find_all('div', {'class': 'table-row'})
    return billionaires


if __name__ == "__main__":
    forbes_url = 'https://www.forbes.com/billionaires'
    forbes_billionaires = find_billionaires(forbes_url)
    forbes_billionaires_info = extract_billionaire_info(forbes_billionaires)
    insert_billionaires(forbes_billionaires_info)
