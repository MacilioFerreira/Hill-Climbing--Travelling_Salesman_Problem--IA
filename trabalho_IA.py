# -*- coding: utf-8 -*-

import sys
import math
import numpy as np

# Para cada linha do arquivo lido, cria uma tupla do tipo (x,y) e retorna uma lista de tuplas
def lerArquivo(linhas):
    ln = []
    for linha in linhas:
        linha = linha[0:-1].split(' ')
        ln.append(linha)
    ln_tuplas = []
    for l in ln:
        i = 0
        while i < len(l):
            l[i] = float(l[i])
            l[i] = float(l[i])
            i += 1
        ln_tuplas.append(tuple(l))
        
    return ln_tuplas

# Calcula a distância euclidiana entre duas cidades...
def distancia(x,y):
    dist = 0
    i = 0
    while i < len(x):
        dist += math.pow((x[i] - y[i]), 2)
        i += 1
    return math.sqrt(dist)

def calculaMatriz(cidades):
    n = len(cidades)
    matriz = np.zeros((n,n))
    i = 0
    while i < n:
        j = 0
        while j < n:
            matriz[i][j] = (distancia(cidades[i], cidades[j]))
            j += 1
        i +=1

    return matriz

# Troca a posição de duas cidades em um estado
def operador1(estado, cidade1, cidade2):
    novo_estado = list(estado)
    indice1 = novo_estado.index(cidade1)
    indice2 = novo_estado.index(cidade2)
    cidade = estado[indice1]
    novo_estado[indice1] = novo_estado[indice2]
    novo_estado[indice2] = cidade
    return novo_estado

# Inverte as posições das cidades em um intervalo
def operador2(estado, cidade1, cidade2):
    novo_estado = list(estado)
    indice1 = novo_estado.index(cidade1)
    indice2 = novo_estado.index(cidade2)
    anterior = list(novo_estado[:indice1])
    posteior = list(novo_estado[(indice2+1):])
    trecho = list(novo_estado[indice1:(indice2+1)])
    trecho.reverse()
    return list(anterior + trecho + posteior)

# Calcula o custo total de um circuito
def calculaCusto(estado):
    custoPercurso = 0
    cidades = list(estado)
    matriz = calculaMatriz(cidades)
    i = 0
    tamanho = len(cidades)
    while i < tamanho-1:
        #custoPercurso += distancia(cidades[i], cidades[i+1])
        custoPercurso += matriz[i][i+1]
        i += 1
    return custoPercurso

# Gera os vizinhos do estado passado. De acordo com os operadores
def gerarVizinho(estado, op1=True):
    tamanho = len(estado)
    lista = []
    # Operador 1
    if op1:
        i = 0
        while i < tamanho:
            permu = []
            if i == (tamanho-1):
                perm = operador1(estado, estado[-1], estado[0])
            else:
                perm = operador1(estado, estado[i], estado[i+1])
            lista.append(perm)
            i += 1
    else:
        i = 0
        while i < tamanho:
            permu = []
            if i == (tamanho-1):
                perm = operador2(estado, estado[0], estado[-1])
            else:
                perm = operador2(estado, estado[i], estado[i+1])
            lista.append(perm)
            i += 1
    return lista


# Primeiro vizinho de maior custo do circuito.
# Pega o primeiro ou pega o melhor => Ele disse que pegasse o primeiro, vc está pegando o melhor
def maiorSucessor(vizinhos, randomizar=False):
    # Randomização da vizinhança
    if randomizar:
        p_rand = np.random.permutation(len(vizinhos))
        n_lista = []
        for e in p_rand:
            n_lista.append(vizinhos[e])
        vizinhos = list(n_lista)

    # Sem randomização
    #print vizinhos
    maior = vizinhos[0]
    custo_maior = calculaCusto(maior)
    i = 1
    while i < len(vizinhos):
        custo_vizinho = calculaCusto(vizinhos[i])
        if custo_maior <= custo_vizinho:
            # pega o melhor
            #maior = vizinhos[i]
            return vizinhos[i]
        i += 1
    return maior

# Algoritmo subida de encosta
def subidaEncosta(estado):
    estadoAtual = estado
    while True:
        vizinhos = gerarVizinho(estado)
        custoEstadoAtual = calculaCusto(estadoAtual)
        maior_sucessor = maiorSucessor(vizinhos, True)
        custo_sucessor = calculaCusto(maior_sucessor)
        print "Estado Atual: " + str(estadoAtual) + "\nCusto: " + str(custoEstadoAtual)
        if custo_sucessor <= custoEstadoAtual:
            return estadoAtual
        else:
            estadoAtual = maior_sucessor


# Principal
def main(arg):
    nome_arquivo = arg[0]
    arquivo = open(nome_arquivo, 'r')

    # Estado Incial 1
    estadoInicial1 = lerArquivo(arquivo.readlines())
    # Estado Incial 2
    #Criando o estado inicial c uma permutação aleatória das cidades
    aleatorio = np.random.permutation(len(estadoInicial1))
    aleatorio = aleatorio.tolist()
    estadoInicial2 = []
    for elemento in aleatorio:
        estadoInicial2.append(estadoInicial1[elemento])

    print "Estado Inicial: \n", estadoInicial1 , "\n"
    resultado = subidaEncosta(estadoInicial1)
    print "\nPonto Máximo: \n" + str(resultado)




if __name__ == '__main__':
    main(sys.argv[1:3])



# epic music oblivion olhar mais tarde
# Anuladas Poscomp = 30,38,40 e 47 == que eu tenha errado todas.. kkkk
