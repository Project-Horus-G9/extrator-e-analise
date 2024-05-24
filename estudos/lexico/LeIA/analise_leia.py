import json
from leia import SentimentIntensityAnalyzer

def main():
    
    print("Iniciando o programa")
    
    analyzer = SentimentIntensityAnalyzer()

    with open('tweets.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        print("Carregando os dados")
        
    lista_tokens = []
    
    for tweets in data['tweets']:
            
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
        
    with open('tokens.json', 'w', encoding='utf-8') as file:
        json.dump(lista_tokens, file, indent=4)
        
    print("Finalizando o programa")

if __name__ == '__main__':
    main()
   
