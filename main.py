import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import streamlit as st
driver = webdriver.Edge()
driver.set_window_position(-10000,0)
driver.set_window_size(1920,1080)
driver.switch_to.new_window('tab')
driver.switch_to.new_window('tab')
ScoresTable = {'Página':[],'Pontuação':[]}
flag = True
count, finalScore = 0, 0
placeholder = st.empty()
imagesList = {}
overviewList= {}
actions = ActionChains(driver)
def getPageScore(html):
    practicesList = []
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
        #driver.execute_script("window.scrollTo(0, 1200);")
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[contains(@class,"table table_primary ")]//tbody//tr')))
        for element in results:
            actions.move_to_element(element).perform()
            practicesList.append(element.screenshot_as_png)
        #for element in resultslist:
        #    practiceList.append(element.screenshot_as_png)
        # imagesList.append(practiceList)
        if flag:
            ScoresTable['Página'].append('Início')
            imagesList['Início'] = practicesList

        else:
            driver.switch_to.window(driver.window_handles[2])
            if driver.title in imagesList.keys():
                ScoresTable['Página'].append(driver.title + ' b')
                imagesList[driver.title + ' b'] = practicesList
            else:
                ScoresTable['Página'].append(driver.title)
                imagesList[driver.title] = practicesList

        print(f'score da página: {score}')
        return float(score)
    except:
        return 0

def getWebsiteScores(site):
    global count, finalScore, placeholder
    print("Iniciando Análise...")
    socialMedia = ['instagram', 'facebook', 'tiktok', 'youtube', 'youtu.be', 'cadastro.museus.gov.br',
                   'museus.cultura.gov.br', '.png', '.jpg', 'linkedin', 'mailto', 'wikipedia','.pdf']
    unique = []
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(site)
        site = driver.current_url
        print(f'domínio real: {site}')
    except:
        print("Site não encontrado.")
        driver.quit()
        return

    points = 0
    result = getPageScore(site)
    driver.switch_to.window(driver.window_handles[0])
    ScoresTable['Pontuação'].append(result)
    unique.append(site)
    print(result)
    if result != 0:
        points += result
        count += 1
    WebDriverWait(driver, 0.1)
    linkList = driver.find_elements(By.XPATH,f'//a[contains(@href, "{site}") or contains(@href, "#/") or contains(@href, "html") or contains(@href, "/view/") or contains(@href, "jsp") or starts-with(@href, "/")]')
    print(linkList)
    for item in linkList:
       placeholder.markdown(f"### :blue-background[Páginas analisadas: {count} :hourglass_flowing_sand: ]")
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
             ScoresTable['Pontuação'].append(result)
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
    return df2

@st.fragment
def imageSlider():
    sliderPlaceholder = st.empty()
    with sliderPlaceholder.container():
        image = st.selectbox("Página",imagesList.keys())
        for element in imagesList[image]:
            st.image(element)

def main():
    global placeholder
    st.title("Verificador de Acessibilidade")
    st.header("Digite o site a ser analisado")
    site = st.text_input("ex: https://site .com .br")
    print(site)
    if site and site != '':
        with st.spinner("Analisando Páginas...  (Pode demorar até 1 min por página)"):
            results = getWebsiteScores(site)
            if count > 0:
                st.header(f"Páginas Totais Analisadas: {count} :white_check_mark:")
            if finalScore != 0:
                if finalScore >= 8:
                    st.header(f"Média geral: :green[{finalScore:.2f}]")
                elif finalScore >= 6:
                    st.header(f"Média geral: :orange[{finalScore:.2f}]")
                else:
                    st.header(f"Média geral: :red[{finalScore:.2f}]")
                st.write(results)
                placeholder.empty()
                st.header("Relatório por página")

    if imagesList:
        imageSlider()


main()