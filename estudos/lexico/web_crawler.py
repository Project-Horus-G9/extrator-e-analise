import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from unidecode import unidecode

def search_twitter(term):
    driver = webdriver.Chrome()
    
    driver.get("https://x.com/login")
    time.sleep(8)
    username = driver.find_element(By.CLASS_NAME, "r-30o5oe")
    username.send_keys('shift534')
    username.send_keys(Keys.RETURN)
    time.sleep(5)

    password = driver.find_element(By.NAME, "password")
    password.send_keys('MIrai123@')
    password.send_keys(Keys.RETURN)
    time.sleep(5)
    
    driver.get("https://x.com/search?q=" + term)

    time.sleep(5)
    latest_tab = driver.find_element(By.LINK_TEXT, "Latest")
    latest_tab.click()
    
    time.sleep(5)
    
    tweets = []
    
    for i in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        bloco = soup.find_all('article', {'role': 'article'})
        
        for b in bloco:
            tweets.append(b)

    data = { 'tweets': [] }

    for tweet in tweets:
        tweet_text = tweet.find('div', {'lang': True})
        if tweet_text:
            texto = unidecode(tweet_text.get_text())
            texto = texto.replace('\n', ' ')
            texto = texto.replace('\r', ' ')
            texto = texto.replace('\t', ' ')
            texto = texto.replace('\"', ' ')
            texto = texto.strip()
            texto = ' '.join(texto.split())
            texto = ' '.join([x for x in texto.split() if 'http' not in x])

            data['tweets'].append({
                'text': texto
            })
        
    driver.close()
    
    return json.dumps(data, indent=4)


def main():
    print("Iniciando o programa")

    data = search_twitter('Energia Solar Brasil')

    with open('tweets.json', 'w') as f:
        f.write(data)

    print("Finalizando o programa")

if __name__ == '__main__':
    main()
