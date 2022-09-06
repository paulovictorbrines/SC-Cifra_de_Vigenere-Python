# Alunos:
    # Paulo Victor França de Souza - 20/0042548;
    # Thais Fernanda de Castro Garcia - 20/0043722.

# Disciplina:
    # Dep. Ciência da Computação - Universidade de Brasília (UnB),
    # CIC0201 - Segurança Computacional (2022.1).
    # Prof. João José Costa Gondim - Turma 1.

# Implementação:
    # Cifrador/decifrador e ataque de recuperação de senha por análise de frequência.

##############################################################################################################################################

from calendar import c
from string import ascii_uppercase
from unicodedata import normalize
import string
from functools import reduce
from unittest import result

##############################################################################################################################################

alfabeto_letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letra_para_numero = dict(zip(alfabeto_letras, range(len(alfabeto_letras)))) # Dicionario de correspondecia entre caracteres e números.
numero_para_letra = dict(zip(range(len(alfabeto_letras)), alfabeto_letras)) # Dicionario de correspondecia entre números e caracteres.

def tratamento(mensagem): # Tratamento da mensagem.
    mensagem = mensagem.replace(' ','') # Tira os espaços.
    mensagem = mensagem.upper() # Transforma em maiúscula.
    mensagem = ''.join([i for i in mensagem if not i.isdigit()])  # Tira qualquer número da mensagem.
    mensagem = mensagem.translate(str.maketrans('','',string.punctuation)) # Tira qualquer acentuação.
    return mensagem

def ajusta_chave(mensagem, chave): # Repete a chave até ficar do tamanho da mensagem.
    chave = list(chave) 
    if len(mensagem) == len(chave): 
        return(chave) 
    else: 
        for i in range(len(mensagem) - len(chave)): 
            chave.append(chave[i % len(chave)]) 
    return("".join(chave)) 

##############################################################################################################################################

def cifra(mensagem, chave): # Cifração com base na cifra de vigenere.
    mensagem_cifrada = []

    for i,c in enumerate(mensagem):
        numero = (letra_para_numero[c] + letra_para_numero[chave[i]]) % len(alfabeto) # Operação (Pi + Ki) % tamanho do alfabeto
        mensagem_cifrada.append(numero_para_letra[numero]) # Converte os números para letras
    return("".join(mensagem_cifrada))

##############################################################################################################################################
 
def decifra(mensagem_cifrada, chave, alfabeto): # Decifração com base na cifra de vigenere.
    resultado = []
    pulos = 0
    for i,c in enumerate(mensagem_cifrada):
        if c not in alfabeto:
            resultado.append(c)
            pulos += 1
            continue

        numero = (letra_para_numero[c] - letra_para_numero[chave[(i - pulos) % len(chave)]]) % len(alfabeto) # Operação (Pi - Ki) % tamanho do alfabeto
        resultado.append(numero_para_letra[numero]) # Converte os números para letras
    return("" . join(resultado))

##############################################################################################################################################

frequencia_ingles = [('A', 8.167), ('B', 1.492), ('C', 2.782), ('D', 4.253), # Frequência de cada letra do alfabeto em inglês
            ('E', 12.702), ('F', 2.228), ('G', 2.015), ('H', 6.094),
            ('I', 6.966), ('J', 0.153), ('K', 0.772), ('L', 4.025),
            ('M', 2.406), ('N', 6.749), ('O', 7.507), ('P', 1.929),
            ('Q', 0.095), ('R', 5.987), ('S', 6.327), ('T', 9.056),
            ('U', 2.758), ('V', 0.978), ('W', 2.360), ('X', 0.150),
            ('Y', 1.974), ('Z', 0.074)]
frequencia_portugues = [('A', 14.63), ('B', 1.04), ('C', 3.88), ('D', 4.99), # Frequência de cada letra do alfabeto em português
            ('E', 12.57), ('F', 1.02), ('G', 1.30), ('H', 1.28),
            ('I', 6.18), ('J', 0.40), ('K', 0.02), ('L', 2.78),
            ('M', 4.74), ('N', 5.05), ('O',10.73), ('P', 2.52),
            ('Q', 1.20), ('R', 6.53), ('S', 7.81), ('T', 4.34),
            ('U', 4.63), ('V', 1.67), ('W', 0.01), ('X', 0.47),
            ('Y', 0.01), ('Z', 0.47)]

def encontra_espacos(mensagem, trigama):
    dist = []
    ender_inicial = -1
    for _ in range(mensagem.count(trigama)):
        ender_antigo = ender_inicial
        ender_inicial = mensagem.index(trigama, ender_inicial + 1)
        dist.append(ender_inicial - ender_antigo)

    return dist

def encontra_tamanho_chave(mensagem, max_chave): # Encontra trigramas repetidos.
    mensagem = ''.join([i for i in mensagem.upper() if i in alfabeto_letras])
    trigramas_repetidos = []
    trigama = ''
    for i in range(len(mensagem) - 3):
        trigama = mensagem[i:i+3]
        if mensagem.count(trigama) > 1:
            trigramas_repetidos.append(trigama)
            trigama = ''

    trigramas_ordenados = sorted(set(trigramas_repetidos), key=lambda trigama: mensagem.count(trigama), reverse=True) # Encontrando o possível tamanho da chave.

    trigramas_espaco = {trigama: encontra_espacos(mensagem, trigama) for trigama in trigramas_ordenados}
    todas_dist = reduce(lambda x, y: x+y, trigramas_espaco.values())
    
    ranking_espacos = [[i, len([dist for dist in todas_dist if dist%i==0])] for i in range(3, max_chave)] # Gera pares de tamanho de chave possíveis.
    possiveis_2_chaves = sorted(ranking_espacos, key=lambda x:x[1], reverse=True)[0:2]

    if possiveis_2_chaves[1][0] > possiveis_2_chaves[0][0] and possiveis_2_chaves[1][1]*1.2 > possiveis_2_chaves[0][1]:
        return possiveis_2_chaves[1][0]
    else:
        return possiveis_2_chaves[0][0]

def encontra_topos(frequencia):
    frequencia_ordenada = sorted(frequencia, reverse=True)
    return [frequencia.index(i) for i in frequencia_ordenada[:10]]


def encontra_chave(mensagem, tamanho_chave, frequencia):
    frequencia_topos = set(encontra_topos(frequencia))

    mensagem = ''.join([i for i in mensagem.upper() if i in alfabeto_letras])
    chave = ''
    while len(chave) != tamanho_chave:
        ender_chave = len(chave)
        fluxo = ''.join([mensagem[i + ender_chave] for i in range(0, len(mensagem) - tamanho_chave, tamanho_chave)])
        
        chave_baseada_freq = dict() # Calcula a frequência de todas chaves do par de chave e tamanho da interseção.

        options = []
        for decifra_letra in alfabeto_letras:
            decifra_fluxo = decifra(fluxo, decifra_letra, alfabeto_letras)
            chave_baseada_freq[decifra_letra] = {letra: decifra_fluxo.count(letra)/len(decifra_fluxo) for letra in alfabeto_letras}

        chave_letra_topos = dict() # Encontra a chave comparando com o máximo 5 da frequência.
        for letra in chave_baseada_freq:
            chave_letra_topos[letra] = encontra_topos(list(chave_baseada_freq[letra].values()))

        chave+=max(chave_letra_topos, key=lambda letra: len(list(frequencia_topos.intersection(chave_letra_topos[letra])))) # Pega a letra com o máximo de melhores interseções entre a frequência real.

    return chave

def ataque(msg, alfabeto, max_chave):
    tamanho_chave = encontra_tamanho_chave(msg, max_chave)
    chave = encontra_chave(
        mensagem=msg,
        tamanho_chave=tamanho_chave,
        frequencia=[i[1] for i in alfabeto]
    )
    return chave


def alfabeto_por_idioma(idioma):
    return frequencia_portugues if idioma == 2 else frequencia_ingles

##############################################################################################################################################1

if __name__ == "__main__": 
    while True:
        print("###############################")
        print("# Cifrar, Decifrar ou Ataque? #")
        print("###############################")
        opcao = (input("  > ")).lower()
        print()

        if opcao[0] == "c":
            alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            mensagem = tratamento(input("# Insira a mensagem:\n  > "))
            chave = tratamento(ajusta_chave(mensagem, input("# Insira a chave:\n  > ")))

            mensagem_cifrada = cifra(mensagem,chave) 

            print("\n>> Mensagem cifrada:", mensagem_cifrada) 

        elif opcao[0] == "d":
            alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            mensagem_cifrada = tratamento(input("# Insira a mensagem cifrada:\n  > "))
            chave = tratamento(ajusta_chave(mensagem_cifrada, input("# Insira a chave:\n  > ")))

            mensagem_decifrada = decifra(mensagem_cifrada,chave,alfabeto) 

            print("\n>> Mensagem decifrada:", mensagem_decifrada) 

        else:
            opcao = (input("# Idioma inglês ou português?:\n  > ")).lower()
            if ((opcao[0] == "i")):
                idioma=1
            else:
                idioma=2
            
            max_chave = 20 # Tamanho máximo possível da chave.
            msg_cifrada_ataque = input('# Digite a mensagem cifrada:\n  > ')
            alfabeto = alfabeto_por_idioma(idioma)
            chave_provavel = ataque(msg_cifrada_ataque, alfabeto, max_chave)

            print(">> Possível chave: ")

            for x in chave_provavel: print(x, end='')
            print()
            
            msg_obtida_ataque = decifra(msg_cifrada_ataque.upper(), chave_provavel, [i[0] for i in alfabeto])
            print("\n>> Mensagem decifrada:\n", msg_obtida_ataque)

        input()
    
    