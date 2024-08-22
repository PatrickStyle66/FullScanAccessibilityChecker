import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
driver = webdriver.Edge()
driver.set_window_position(-10000,0)
driver.switch_to.new_window('tab')
driver.switch_to.new_window('tab')
ScoresTable = {'Page':[],'Score':[]}
flag = True
def getPageScore(html):
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://accessmonitor.acessibilidade.gov.pt/')
    HtmlMode = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@data-rr-ui-event-key,"tab2")]')))
    HtmlMode.click()
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "html")))
    search.clear()
    if flag:
        driver.switch_to.window(driver.window_handles[0])
        pyperclip.copy(driver.page_source)
    else:
        pyperclip.copy(html)
    driver.switch_to.window(driver.window_handles[1])
    search.send_keys(Keys.CONTROL, 'v')
    #WebDriverWait(AccessDriver, 60)
    sendButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@id,"btn-html")]')))
    sendButton.click()
    try:
        score = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "svg")))
       # pageName = AccessDriver.find_element(By.CLASS_NAME,"resume_info_about_uri d-flex flex-column gap-4")
        #print(pageName.text)
        score = str(score.text).split('\n')[1]
        if not flag:
            driver.switch_to.window(driver.window_handles[2])
            ScoresTable['Page'].append(driver.title)
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
        driver.switch_to.window(driver.window_handles[0])
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
    driver.switch_to.window(driver.window_handles[0])
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
             driver.switch_to.window(driver.window_handles[2])
             driver.get(link)
             html = driver.page_source
             result = getPageScore(html)
             driver.switch_to.window(driver.window_handles[0])
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


site = input("digite a url a ser analisada:")
getWebsiteScores(site)