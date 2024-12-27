import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Edge()
table = {'Museum':[], 'Website':[]}
MuseusBR = 'https://cadastro.museus.gov.br/museus?order=DESC&orderby=meta_value&metakey=222&view_mode=masonry&perpage=12&paged=1&fetch_only=thumbnail%2Ccreation_date%2Ctitle%2Cdescription&fetch_only_meta=&taxquery%5B0%5D%5Btaxonomy%5D=tnc_tax_275&taxquery%5B0%5D%5Bterms%5D%5B0%5D=58&taxquery%5B0%5D%5Bcompare%5D=IN&taxquery%5B1%5D%5Btaxonomy%5D=tnc_tax_270&taxquery%5B1%5D%5Bterms%5D%5B0%5D=24&taxquery%5B1%5D%5Bcompare%5D=IN'
def getMuseumsSite():
    print("Iniciando busca...")
    driver.get(MuseusBR)
    pages = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//a[(@role = 'button') and (@class = 'pagination-link')]")))
    pages = pages[-1].text
    for _ in range(int(pages)):
        time.sleep(3)
        museums = driver.find_elements(By.CLASS_NAME, "tainacan-masonry-item")
        for museum in museums:
            req = requests.get(museum.get_attribute('href'))
            if req.status_code == 200:
                print('Requisição bem sucedida!')
                content = req.content
            soup = BeautifulSoup(content, 'html.parser')
            try:
                link = soup.find(name='blockquote').find(name='a')['href']
                name = soup.find(name='h1', attrs={'class': 'page-title'}).get_text()
                table['Museum'].append(name)
                table['Website'].append(link)
                print(f'{name}\n{link}')
            except:
                link = soup.find(name='a', attrs={'target': '_blank'})['href']
                name = soup.find(name='h1', attrs={'class': 'page-title'}).get_text()
                print(f'{name}\n{link}')
                table['Museum'].append(name)
                table['Website'].append(link)
        print('\n')
        try:
            next = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[(@role = 'button') and (@class = 'pagination-link pagination-next pagination-next')]")))
            driver.execute_script("window.scrollTo(0, 2800);")
            time.sleep(0.5)
            next.click()
            print("clicked!")
        except:
            pass
    df = pd.DataFrame(data=table)
    df.to_csv('MuseumsWebsites.csv')

getMuseumsSite()