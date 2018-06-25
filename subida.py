# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

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

# Matriz de distâncias
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
        custoPercurso += matriz[i][i+1]
        i += 1
    return custoPercurso

# Gera os vizinhos do estado passado. De acordo com os operadores
def gerarVizinho(estado, operador):
    tamanho = len(estado)
    lista = []
    if operador == 1: # Operador 1
        i = 0
        while i < tamanho:
            permu = []
            if i == (tamanho-1):
                perm = operador1(estado, estado[-1], estado[0])
            else:
                perm = operador1(estado, estado[i], estado[i+1])
            lista.append(perm)
            i += 1
    else: # Operador 2
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


# Escolhe o primeiro melhor, ou seja, o primeiro vizinho com custo maior que o dele do circuito.
def maiorSucessor(estado, custoEstado, vizinhos, randomizar):
    # Randomização da vizinhança
    if randomizar:
        p_rand = np.random.permutation(len(vizinhos))
        n_lista = []
        for e in p_rand:
            n_lista.append(vizinhos[e])
        vizinhos = list(n_lista)
    # Sem randomização
    maior = estado
    custo_maior = custoEstado
    i = 1
    while i < len(vizinhos):
        custo_vizinho = calculaCusto(vizinhos[i])
        if custo_maior < custo_vizinho:
            return vizinhos[i]
        i += 1
    return maior

# Algoritmo subida de encosta
def subidaEncosta(estado, operador, aleatorio):
    passos = 1
    estadoAtual = estado
    while True:
        vizinhos = gerarVizinho(estado, operador)
        custoEstadoAtual = calculaCusto(estadoAtual)
        maior_sucessor = maiorSucessor(estado, custoEstadoAtual, vizinhos, aleatorio)
        custo_sucessor = calculaCusto(maior_sucessor)
        print "Estado Atual: " + str(estadoAtual) + "\nCusto: " + str(custoEstadoAtual) + str(passos)
        passos += 1
        if custo_sucessor <= custoEstadoAtual:
            return estadoAtual, passos
        else:
            estadoAtual = maior_sucessor

# Criando arquivo de saida
def gerarArquivo(tabela):
    arquivo = open("saida_1",'wb')
    for elemento in tabela:
        arquivo.write(str(elemento) + "\n")
    arquivo.close()

def calcularMedia(dicionario):
    dist = 0
    lista = dicionario.items()
    for chave in lista:
        i = 0
        while i < len(chave)-1:
            dist += chave[i] *chave[i+1]
            i += 1
    return dist/float(len(lista))

def plotarGrafico(medias):
    variacoes = [x for x in xrange(1,9)]
    plt.scatter(x=variacoes, y=medias,s=medias,c='g')
    plt.xlabel("Variacoes")
    plt.ylabel("Medias")
    plt.title("Distribuicao das Medias de acordo com as Variacoes")
    plt.axis([1,len(variacoes), 1, medias[-1]])
    plt.show()

# Principal
def main(arg):
    nome_arquivo = arg[0]
    arquivo = open(nome_arquivo, 'r')
    # Estado Incial 1
    estadoInicial1 = lerArquivo(arquivo.readlines())
    # Estado Incial 2, Criando o estado inicial c uma permutação aleatória das cidades
    aleatorio = np.random.permutation(len(estadoInicial1))
    aleatorio = aleatorio.tolist()
    estadoInicial2 = []
    for elemento in aleatorio:
        estadoInicial2.append(estadoInicial1[elemento])
    # Iterações => Dados do arquivo
    linhas = 40
    colunas = 8
    tabela = np.zeros((linhas,colunas))
    tabela = tabela.tolist()
    maximo = passos = 0
    # Distribuições separadas para a análise dos casos aleatórios. Onde v1 e v3 são não aleatórias
    v1 = 0
    v3 = 0
    dic2 = {}
    dic4 = {}
    dic5 = {}
    dic6 = {}
    dic7 = {}
    dic8 = {}
    j = 0
    while j < colunas:
        print "\nVariação %d " % (j+1)
        i = 0
        while i < linhas:
            print "\nIteração:  %d " % (i+1)
            if j == 0:
                maximo, passos = subidaEncosta(estadoInicial1, 1, False) # Não necessita qtd passos
                tabela[i][0] = maximo
                v1 = passos
            elif j == 1:
                maximo, passos = subidaEncosta(estadoInicial1, 1, True)
                tabela[i][1] = maximo
                if passos in dic2.keys():
                    dic2[passos] += 1
                else:
                    dic2[passos] = 1
            elif j == 2:
                maximo, passos = subidaEncosta(estadoInicial1, 2, False) # Não necessita qtd passos
                tabela[i][2] = maximo
                v3 = passos
            elif j == 3:
                maximo, passos = subidaEncosta(estadoInicial1, 2, True)
                tabela[i][3] = maximo
                if passos in dic4.keys():
                    dic4[passos] += 1
                else:
                    dic4[passos] = 1
            elif j == 4:
                maximo, passos = subidaEncosta(estadoInicial2, 1, False)
                tabela[i][4] = maximo
                if passos in dic5.keys():
                    dic5[passos] += 1
                else:
                    dic5[passos] = 1
            elif j == 5:
                maximo, passos = subidaEncosta(estadoInicial2, 1, True)
                tabela[i][5] = maximo
                if passos in dic6.keys():
                    dic6[passos] += 1
                else:
                    dic6[passos] = 1
            elif j == 6:
                maximo, passos = subidaEncosta(estadoInicial2, 2, False)
                tabela[i][6] = maximo
                if passos in dic7.keys():
                    dic7[passos] += 1
                else:
                    dic7[passos] = 1
            elif j == 7:
                maximo, passos = subidaEncosta(estadoInicial2, 2, True)
                tabela[i][7] = maximo
                if passos in dic8.keys():
                    dic8[passos] += 1
                else:
                    dic8[passos] = 1
            print "\n"
            i += 1
        j += 1

    #Medias
    medias = np.zeros(8)
    medias.tolist()
    medias[0] = v1
    medias[1] = calcularMedia(dic2)
    medias[2] = v3
    medias[3] = calcularMedia(dic4)
    medias[4] = calcularMedia(dic5)
    medias[5] = calcularMedia(dic6)
    medias[6] = calcularMedia(dic7)
    medias[7] = calcularMedia(dic8)
    # Gerando gráfico com as médias
    #plotarGrafico(medias)
    # Gerando o arquivo
    gerarArquivo(tabela)


if __name__ == '__main__':
    main(sys.argv[1:3])

