def levenshtein(s1, s2):
    assert isinstance(s1, str), "s1 isn't a string"
    assert isinstance(s2, str), "s2 isn't a string"

    if len(s1) < len(s2):
        return levenshtein(s2, s1)

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

def corrigir_palavra(palavra, referencia):
    if levenshtein(palavra, referencia) <= 4:
        return referencia
    return palavra

def corrigir_frase(frase, referencia):
    palavras = frase.split()
    palavras_corrigidas = [corrigir_palavra(palavra, referencia) for palavra in palavras]
    return ' '.join(palavras_corrigidas)

frases = [
    "Eu comprei um remédio chamado Sapranelo ontem.",
    "Você já ouviu falar de Saranelo?",
    "O médico recomendou que eu tomasse Zarynelo.",
    "Estou usando Sarimela para tratar minha condição.",
    "Esqueci de tomar meu Sarymeli hoje de manhã."
]

referencia = "Saphnelo"

for frase in frases:
    frase_corrigida = corrigir_frase(frase, referencia)
    print(f"Frase original: {frase}")
    print(f"Frase corrigida: {frase_corrigida}")
    print()
