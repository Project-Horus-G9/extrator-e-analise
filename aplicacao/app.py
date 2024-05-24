import json

# web crawling
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from unidecode import unidecode

# lexico
from leia import SentimentIntensityAnalyzer

# grafico
import matplotlib.pyplot as plt

class App:
    def __init__(self):
        pass
        
    def get_base(self):
        with open('aplicacao/config/base.json') as f:
            self.base = json.load(f)

    def levenshtein(self, s1, s2):
        assert isinstance(s1, str), "s1 isn't a string"
        assert isinstance(s2, str), "s2 isn't a string"

        if len(s1) < len(s2):
            return self.levenshtein(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
    
    def corrigir_palavra(self, palavra):
        for palavra_base in self.base['palavroes']:
            if self.levenshtein(palavra, palavra_base) <= 3:
                print(f"Palavra retirada: {palavra}")
                return ''
            return palavra
    
    def corrigir_frase(self, frase):
        palavras = frase.split()
        palavras_corrigidas = [self.corrigir_palavra(palavra) for palavra in palavras]
        return ' '.join(palavras_corrigidas)
    
    def search_twitter(self, term):
        driver = webdriver.Chrome()
        
        driver.get("https://x.com/login")
        time.sleep(3)
        username = driver.find_element(By.CLASS_NAME, "r-30o5oe")
        username.send_keys('shift534')
        username.send_keys(Keys.RETURN)
        time.sleep(3)

        password = driver.find_element(By.NAME, "password")
        password.send_keys('MIrai123@')
        password.send_keys(Keys.RETURN)
        time.sleep(3)
        
        driver.get("https://x.com/search?q=" + term)

        time.sleep(5)
        latest_tab = driver.find_element(By.LINK_TEXT, "Latest")
        latest_tab.click()
        
        time.sleep(5)
        
        tweets = []
        
        for i in range(10):
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
        
        with open('aplicacao/config/tokens.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        with open('aplicacao/config/tokens.json') as f:
            self.tokens = json.load(f)
        
    def lexico(self):
        
        analyzer = SentimentIntensityAnalyzer()
            
        lista_tokens = []
        
        for tweets in self.tokens_tratados['tweets']:
                
            text = tweets['text']
            score = analyzer.polarity_scores(text)
            
            tokens = {
                'tweet': text,
                'sentimento': {
                    'negativo': score['neg'],
                    'neutro': score['neu'],
                    'positivo': score['pos'],
                    'composicao': score['compound']
                }
            }
            
            lista_tokens.append(tokens)
            
        with open('aplicacao/config/tokens_lexico.json', 'w', encoding='utf-8') as file:
            json.dump(lista_tokens, file, indent=4)
            
        with open('aplicacao/config/tokens_lexico.json') as f:
            self.tokens_lexico = json.load(f)
        
    def exibir_grafico(self):
        sentimentos = [entry['sentimento'] for entry in self.tokens_lexico]

        sentimentos_classificados = []
        for sentimento in sentimentos:
            compound = sentimento['composicao']
            if compound >= 0.05:
                sentimento_classificado = 'Positivo'
            elif compound <= -0.05:
                sentimento_classificado = 'Negativo'
            else:
                sentimento_classificado = 'Neutro'
            sentimentos_classificados.append(sentimento_classificado)

        contagem = {'Positivo': 0, 'Negativo': 0, 'Neutro': 0}
        for sentimento_classificado in sentimentos_classificados:
            contagem[sentimento_classificado] += 1

        categorias = list(contagem.keys())
        valores = list(contagem.values())

        plt.bar(categorias, valores, color=['green', 'red', 'blue'])
        plt.xlabel('Sentimento')
        plt.ylabel('Número de Tweets')
        plt.title('Distribuição de Sentimentos')
        plt.show()
    
    def run(self):
        
        self.get_base()
        
        self.search_twitter('Energia Solar Brasil')
        
        frases_tratadas = {
            'tweets': []
        }
        
        for frase in self.tokens['tweets']:
            frases_tratadas['tweets'].append({
                'text': self.corrigir_frase(frase['text'])
            })
        
        with open('aplicacao/config/tokens_tratados.json', 'w') as f:
            json.dump(frases_tratadas, f, indent=4)
            
        with open('aplicacao/config/tokens_tratados.json') as f:
            self.tokens_tratados = json.load(f)
        
        self.lexico()

        self.exibir_grafico()        
    
def main():
    app = App()
    
    app.run()
    
if __name__ == '__main__':
    
    main()   
    