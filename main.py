import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
driver = webdriver.Edge()
AccessDriver = webdriver.Edge()
htmlDriver = webdriver.Edge()
ScoresTable = {'Page':[],'Score':[]}
flag = True
def getPageScore(html):
    AccessDriver.get('https://accessmonitor.acessibilidade.gov.pt/')
    HtmlMode = WebDriverWait(AccessDriver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@data-rr-ui-event-key,"tab2")]')))
    HtmlMode.click()
    search = WebDriverWait(AccessDriver, 10).until(EC.presence_of_element_located((By.ID, "html")))
    search.clear()
    if flag:
        pyperclip.copy(driver.page_source)
    else:
        pyperclip.copy(html)
    search.send_keys(Keys.CONTROL, 'v')
    #WebDriverWait(AccessDriver, 60)
    sendButton = WebDriverWait(AccessDriver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@id,"btn-html")]')))
    sendButton.click()
    try:
        score = WebDriverWait(AccessDriver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "svg")))
       # pageName = AccessDriver.find_element(By.CLASS_NAME,"resume_info_about_uri d-flex flex-column gap-4")
        #print(pageName.text)
        score = str(score.text).split('\n')[1]
        if not flag:
            ScoresTable['Page'].append(htmlDriver.title)
        print(f'score da página: {score}')
        return float(score)
    except:
        return 0

def getWebsiteScores(site):
    print("Iniciando Análise...")
    socialMedia = ['instagram', 'facebook', 'tiktok', 'youtube', 'youtu.be', 'cadastro.museus.gov.br',
                   'museus.cultura.gov.br', '.png', '.jpg', 'linkedin', 'mailto', 'wikipedia']
    unique = []
    try:
        driver.get(site)
        site = driver.current_url
        print(f'domínio real: {site}')
    except:
        print("Site não encontrado.")
        return

    ScoresTable['Page'].append('Início')
    points = 0
    count = 0
    result = getPageScore(site)
    ScoresTable['Score'].append(result)
    unique.append(site)
    print(result)
    if result != 0:
        points += result
        count += 1
    WebDriverWait(driver, 0.1)
    linkList = driver.find_elements(By.XPATH,f'//a[contains(@href, "{site}") or contains(@href, "#/") or contains(@href, "html") or contains(@href, "/view/") or contains(@href, "jsp") or starts-with(@href, "/")]')
    print(linkList)
    for item in linkList:
       try:
           global flag
           flag = False
           link = item.get_attribute('href')
           print(link)
           if link in unique:
               continue
           skip = False
           for social in socialMedia:
               if social in str(link).lower():
                   skip = True
           if not skip:
             htmlDriver.get(link)
             html = htmlDriver.page_source
             result = getPageScore(html)
             unique.append(link)
             ScoresTable['Score'].append(result)
             print(result)
             if result != 0:
                points += result
                count += 1

       except Exception as error:
           print(error)
           continue
    if count == 0:
        finalScore = 0
    else:
        finalScore = points / count
    print(f"Média: {finalScore}")
    print(f"Páginas Verificadas: {count}")
    print(ScoresTable)
    df = pd.DataFrame(data=ScoresTable)
    df2 = df.dropna()
    df2.to_csv('WebsiteScores.csv')
    driver.quit()
    AccessDriver.quit()

site = input("digite a url a ser analisada:")
getWebsiteScores(site)