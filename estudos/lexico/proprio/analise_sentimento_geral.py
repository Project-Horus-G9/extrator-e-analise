import tokeniza as tk
import json
import sentimentos as sen
import unicodedata

def main():
    with open('tweets.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    lista_tokens = []
    
    for tweets in data['tweets']:
        text = tweets['text']
        lista_tokens.append(tk.tokeniza(text))
        
        
    palavras_negativas_sem_acento = []

    for palavra in sen.palavras_negativas:
        palavra_sem_acento = palavra.replace("ç", "c")
        palavra_sem_acento = ''.join((c for c in unicodedata.normalize('NFD', palavra_sem_acento) if unicodedata.category(c) != 'Mn'))
        palavras_negativas_sem_acento.append(palavra_sem_acento)    
    
    palavras_positivas_sem_acento = []
    
    for palavra in sen.palavras_positivas:
        palavra_sem_acento = palavra.replace("ç", "c")
        palavra_sem_acento = ''.join((c for c in unicodedata.normalize('NFD', palavra_sem_acento) if unicodedata.category(c) != 'Mn'))
        palavras_positivas_sem_acento.append(palavra_sem_acento)    
    
    n = 0
    p = 0

    for i in range(len(lista_tokens)):
        for j in range(len(lista_tokens[i])):
            if lista_tokens[i][j] in palavras_negativas_sem_acento:
                n=n+1
            elif lista_tokens[i][j] in palavras_positivas_sem_acento:
                p=p+1
               
    geral = p + n
    
    print("---------------------------------------")
    print("Sentimento geral a cerca do assunto: ")
    print("---------------------------------------")
    print(f"Positivo: {round((p/geral) * 100)}%")
    print(f"Negativo: {round((n/geral) * 100)}%")
    print("---------------------------------------")
        


    

if __name__ == '__main__':
    main()
   
