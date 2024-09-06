import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import streamlit as st
import requests
driver = webdriver.Edge()
driver.set_window_position(-10000,0)
driver.set_window_size(1920,1080)
driver.switch_to.new_window('tab')
driver.switch_to.new_window('tab')
ScoresTable = {'Página':[],'Pontuação':[]}
flag = True
count, finalScore,pageCount = 0, 0, 0
placeholder = st.empty()
imagesList = {}
overviewList= {}
scoreList = {}
infoList = {}
repeatList = []
actions = ActionChains(driver)
def getPageScore(html):
    global Screenshots
    practicesList = []
    tableList = []
    info = []
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
        scoreImage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"d-flex flex-row mt-5 mb-5 justify-content-between container_uri_chart")]')))
        actions.move_to_element(scoreImage).perform()
        scoreImage = scoreImage.screenshot_as_png
        score = str(score.text).split('\n')[1]
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[contains(@class,"table table_primary ")]//tbody//tr')))
        infoElements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"size_container d-flex flex-column gap-4")]//div[contains(@class,"d-flex flex-column")]')))
        for element in infoElements:
            actions.move_to_element(element).perform()
            info.append(element.screenshot_as_png)
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//tr[contains(@class,"mobile_table")]')))
        actions.move_to_element(title).perform()
        title = title.screenshot_as_png
        tableList.append(title)
        tableElements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//table[contains(@class,"table table-bordereds table-alternative ")]//tbody//tr')))
        for element in tableElements:
            actions.move_to_element(element).perform()
            tableList.append(element.screenshot_as_png)
        for element in results:
            actions.move_to_element(element).perform()
            practicesList.append(element.screenshot_as_png)
        if flag:
            ScoresTable['Página'].append('Início')
            imagesList['Início'] = practicesList
            scoreList['Início'] = scoreImage
            overviewList['Início'] = tableList
            infoList['Início'] = info
        else:
            driver.switch_to.window(driver.window_handles[2])
            if driver.title in imagesList.keys():
                repeatList.append(driver.title)
                repeat = repeatList.count(driver.title) + 1
                repeatTitle =f'{driver.title}-{repeat}'
                ScoresTable['Página'].append(repeatTitle)
                imagesList[repeatTitle] = practicesList
                scoreList[repeatTitle] = scoreImage
                overviewList[repeatTitle] = tableList
                infoList[repeatTitle] = info
            else:
                ScoresTable['Página'].append(driver.title)
                imagesList[driver.title] = practicesList
                scoreList[driver.title] = scoreImage
                overviewList[driver.title] = tableList
                infoList[driver.title] = info

        print(f'score da página: {score}')
        return float(score)
    except Exception as error:
        print(error)
        return 0

def getLinkFromElement(item):
    try:
        return item.get_attribute("href")
    except:
        pass

def searchThroughWebsite(linkList,site):
    global placeholder,pageCount
    RejectList = ['instagram', 'facebook', 'tiktok', 'youtube', 'youtu.be', 'cadastro.museus.gov.br',
                   'museus.cultura.gov.br', '.png', '.jpg', 'linkedin', 'mailto', 'wikipedia', '.pdf', 'twitter','.webp']
    for link in linkList:
        try:
            req = requests.get(link)
        except:
            continue
        if req.status_code == 200 and link != site:
            driver.get(link)
            try:
                elementList = WebDriverWait(driver, 1).until(
                    EC.presence_of_all_elements_located((By.XPATH,
                                                         f'//a[contains(@href, "{site}") or contains(@href, "#/") or contains(@href, "jsp") or starts-with(@href, "/")]')))
            except:
                continue
            referenceList = list(set(map(getLinkFromElement, elementList)))
            referenceList.extend(linkList)
            referenceList = list(set(referenceList))
            for item in referenceList:
                skip = False
                for reject in RejectList:
                    if reject in item.lower():
                        skip = True
                if skip:
                    continue
                if item not in linkList:
                    linkList.append(item)
            print(f'links encontrados:{len(referenceList)} links assimilados: {len(linkList)}')
            pageCount = len(linkList)
            placeholder.markdown(f"### :blue-background[Páginas encontradas: {pageCount + 1}     Páginas analisadas: {count} :hourglass_flowing_sand: ]")
    return linkList

def getWebsiteScores(site):
    global count, finalScore, placeholder
    print("Iniciando Análise...")

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
    unique.append(site)
    print(result)
    if result != 0:
        ScoresTable['Pontuação'].append(result)
        points += result
        count += 1
    WebDriverWait(driver, 0.1)
    elementList = driver.find_elements(By.XPATH,f'//a[contains(@href, "{site}") or contains(@href, "#/") or contains(@href, "html") or contains(@href, "jsp") or starts-with(@href, "/")]')
    print(elementList)
    linkList = list(set(map(getLinkFromElement,elementList)))
    driver.switch_to.window(driver.window_handles[2])
    linkList = searchThroughWebsite(linkList,site)
    driver.switch_to.window(driver.window_handles[0])
    for item in linkList:
       placeholder.markdown(f"### :blue-background[Páginas encontradas: {pageCount + 1}     Páginas analisadas: {count} :hourglass_flowing_sand: ]")
       try:
           global flag
           flag = False
           link = item
           print(link)
           if link in unique:
               continue
           driver.switch_to.window(driver.window_handles[2])
           driver.get(link)
           html = driver.page_source
           result = getPageScore(html)
           driver.switch_to.window(driver.window_handles[0])
           unique.append(link)
           if result != 0:
               ScoresTable['Pontuação'].append(result)
               print(result)
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
    global Screenshots
    sliderPlaceholder = st.empty()
    with sliderPlaceholder.container():
        image = st.selectbox("Página", imagesList.keys())
        left_co, cent_co, last_co = st.columns(3)
        with left_co:
            for element in infoList[image]:
                st.image(element)
        with cent_co:
            st.image(scoreList[image],use_column_width=False)
        for element in overviewList[image]:
            st.image(element)
        for element in imagesList[image]:
            st.image(element)


def main():
    global placeholder
    st.title("Verificador de Acessibilidade")
    st.header("Digite o site a ser analisado")
    site = st.text_input("ex: https://site .com .br")
    print(site)
    if site and site != '':
        with st.spinner("Analisando Páginas...  "):
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