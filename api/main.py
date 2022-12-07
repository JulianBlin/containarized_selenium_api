from selenium import webdriver
from fastapi import FastAPI, HTTPException
from api.functions import return_population_by_country
from bs4 import BeautifulSoup
import time

app = FastAPI()

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
driver = webdriver.Chrome('./applications/chromedriver', options=chrome_opt)

@app.get("/get_population_by_country")
def get_population_by_country(continent = None):
    if continent is not None:
        continent = continent.title()

    continents_list = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania', None]

    if continent in continents_list:
        driver = webdriver.Chrome('./applications/chromedriver', options=chrome_opt)
        table_return = return_population_by_country(driver, continent)
        driver.close()
        return table_return.to_json(orient="records")
    else:
        raise HTTPException(
            status_code = 400,
            detail = "Continent is not declared as one of: Africa, Americas, Asia, Europe, Oceania"
        )


@app.get("/test")
def test():
    start_time = time.time()
    driver.get("https://joures.fr/collections/jouets-deveil/products/jouet-de-dentition-pepino-le-comcombre")
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    process_time = time.time() - start_time

    return soup.find('h1', 'product-title').text, process_time
