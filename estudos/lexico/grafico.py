# Sentimento positivo: compound >= 0.05
# Sentimento negativo: compound <= -0.05
# Sentimento neutro: (compound > -0.05) and (compound < 0.05)

import json
import matplotlib.pyplot as plt

with open('tokens.json', 'r') as f:
    data = json.load(f)

sentimentos = [entry['sentimento'] for entry in data]

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
