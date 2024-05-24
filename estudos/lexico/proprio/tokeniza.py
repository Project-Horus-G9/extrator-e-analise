TESTE = False
OPERADORES = "%*/+-!^="
DIGITOS = "0123456789"
PONTO = "."
FLOATS = DIGITOS + PONTO
LETRAS  = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ABRE_FECHA_PARENTESES = "()"

OPERADOR   = 1 
NUMERO     = 2 
VARIAVEL   = 3 
PARENTESES = 4 

BRANCOS    = [' ', '\n', '\t', '\v', '\f', '\r']
COMENTARIO = "#"

def tokeniza(exp):
    tokens = []
    termo = ''
    
    i = 0
    while i < len(exp):
        char = exp[i]
        
        if char == COMENTARIO:
            break
        
        if char in BRANCOS:
            if termo:
                tokens.append(termo)
                termo = ''
            i += 1
            continue
        
        if char in OPERADORES or char in ABRE_FECHA_PARENTESES:
            if termo:
                tokens.append(termo)
                termo = ''
            tokens.append(char)
            i += 1
            continue
        
        if char in DIGITOS or char in LETRAS or char == PONTO:
            termo += char
            i += 1
            continue
        
        i += 1
    
    if termo:
        tokens.append(termo)
    
    for j in range(len(tokens)):
        token = tokens[j]
        if all(c in FLOATS for c in token):
            try:
                tokens[j] = float(token)
            except ValueError:
                pass
    
    return tokens