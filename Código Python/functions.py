# Biblioteca de Funcionalidades do Projeto

from decimal import ROUND_DOWN, ROUND_FLOOR, ROUND_UP
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
from sklearn.cluster import KMeans 
import skimage.color
import cv2
from scipy import misc
from skimage.color import rgb2gray
from skimage import color
import skimage.metrics
from sklearn.metrics import mean_squared_error
from PIL import Image
from scipy import ndimage
import functions as fun
import time
from skimage.feature import hog
from skimage import exposure
import pandas as pd
import csv
import statistics as st
import math
import mysql.connector
from mysql.connector import Error
import oci
import boto3
import os
import logging
from botocore.exceptions import ClientError

#Variáveis de configuração
path = ''

## Autenticação para Conexão Autonomous Database
PYTHON_USERNAME="ver conta na cloud"
PYTHON_PASSWORD="ver conta na cloud"
PYTHON_CONNECTSTRING='ver conta na cloud'

## Funções ...

def kmeans (num_clusters,img):

    # Redimensiona a imagem, formando um array onde cada linha é um
    # pixel e cada coluna é um atributo (cores do pixel)
    data = img.reshape(img.shape[0]*img.shape[1], 3)
    
    # Cria instância da classe KMeans e ajusta aos dados
    km = KMeans(n_clusters=num_clusters)
    km.fit(data)

    # Imprime os valores finais obtidos para as sementes
    # print(km.cluster_centers_)

    # Obtém o rótulo de cada pixel. labels é um array 1D de tamanho
    # igual ao número de pixels na imagem
    labels = km.predict(data)

    # Redimensiona o array labels para o mesmo número de linhas
    # e colunas do array img
    img_labels = labels.reshape(img.shape[:2])
    
    return km, labels, img_labels

def exibeRotulos (num_clusters, img_labels, img_ref):

    # Montagem de uma matriz nos mesmo padrão da imagem de referência
    # Retirado o canal 2 por não funcionar com a função "ndi.binary_closing" Fechamento binário
    img_labels_closed = np.zeros((num_clusters, img_ref.shape[0], img_ref.shape[1]))
        
    # Primeiro executada a operação de fechamento em cada rótulo identificado, para eliminar buracos
    for label in range(num_clusters):
        img_mask = img_labels==label
        img_labels_closed[label] = ndi.binary_closing(img_mask, iterations=10)

    # Percorre todos os rótulos, de acordo com o número de clusters, e efetua a plotagem
    for label in range(num_clusters):
        plt.figure(figsize=[10,10])
        plt.imshow(img_labels_closed[label])
        plt.title('Label K-Means ' + str(label))
    
    return img_labels_closed

def reconstruirMatrizPixelsReferencia (img_ref,img_segmentada, flag, val_lin_win=0, val_2_lin_win=0, val_col_win =0, val_2_col_win=0): 
    
    ## Flag = 'IMG_SEGMENTADA' OU 'IMG_FINAL'
    ## Parâmetros de janelamento possuem o valor padrão ='0'
    ## (700,2700) (1350,2700) imagem maior | (500,2000) (1050,2100) Imagem menor 
    
    # Obter dados da imagem de referência
    altura, largura, canais = img_ref.shape
    
    # Criar a matriz para reconstrução da imagem segmentada
    matriz_reconst = np.zeros_like(img_ref)
    # Percorrer a imagem segmentada
    # Em cada posição = "1" substitui pelo pixel de referência

    if (flag == 'IMG_SEGMENTADA'): 
        for lin in range(0, altura):
            for col in range(0, largura):
                if (img_segmentada[lin][col] == 1):
                    matriz_reconst[lin][col]=img_ref[lin][col]
                else:
                    matriz_reconst[lin][col] = 255

    if(flag == 'IMG_FINAL'):
        for lin in range(0, altura):
            for col in range(0, largura):
                matriz_reconst[lin][col] = 255 # coloca em todas as posições da matriz o valor de 255 (fundo branco)                      

        for lin in range(val_lin_win,val_2_lin_win): # percorre no intervalo definido na janela (linha)
            for col in range(val_col_win,val_2_col_win): # percorre no intervalo definido na janela (coluna)
                if (img_segmentada[lin][col] == 1):
                    matriz_reconst[lin][col]=img_ref[lin][col]
                else:
                    matriz_reconst[lin][col] = 255
                
    return matriz_reconst

def reconstruirCoresViaCentroides (num_clusters, img_ref, km, img_labels):

    # Para cada canal, substituímos os pixels brancos da imagem segmentada
    # pelo valor do centróide do respectivo cluster
    img_reconst = np.zeros_like(img_ref)
    for label in range(num_clusters):
        img_mask = img_labels==label

        # A linha abaixo possui o significado: para cada pixel em
        # img_reconst onde img_mask é True, coloque o valor RGB do 
        # centróide do cluster possuindo índice label
        img_reconst[img_mask] = km.cluster_centers_[label]

    return img_reconst

def imprimirGraficoCentroidesKmeans(img_ref, km, labels):
    
    data = img_ref.reshape(img_ref.shape[0]*img_ref.shape[1], 3)

    plt.scatter(data[:, 0], data[:,1], s = 3, c = labels)
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s = 50, c = 'red',label = 'Centroides')
    plt.title('Clusters e Centroides')
    plt.xlabel('Comprimento')
    plt.ylabel('Largura')
    plt.legend()
    plt.figure(figsize=[45,45])
    plt.show()
    
    return 'Gráfico gerado com sucesso!!'

def reconstruct_img_from_lab(img, img_labels, cluster_centers, num_clusters):
    '''Reconstrói a imagem RGB a partir do resultado da segmentação k-médias. 
        Os parâmetros de entrada são o canal L da imagem no espaço Lab (img_L), 
        um array 2D contendo em cada posição o rótulo do pixel (img_labels) e 
        a cor, nos canais a e b, associada a cada rótulo (cluster_centers)'''

    img_reconst = np.zeros((img.shape[0], img.shape[1], 3))
    for label in range(num_clusters):
        ind = np.nonzero(img_labels==label)
                
        # Cálculo de um valor médio do canal L para associar 
        # a cada cluster
        avg_lightness = np.mean(img[ind[0],ind[1]])
        img_reconst[ind[0], ind[1], 0] = avg_lightness
        img_reconst[ind[0], ind[1], 1] = cluster_centers[label][0]
        img_reconst[ind[0], ind[1], 2] = cluster_centers[label][1]
        plt.figure(cluster_centers[label][0])
    img_rgb = skimage.color.lab2rgb(img_reconst)
    img_rgb = img_reconst

    return img_rgb

def salvarImagemDiscoRGB(img_entrada, img_saida): # imagem de saída deve vir no formato 'nome_imagem.jpg'
    imagem = cv2.cvtColor(img_entrada, cv2.COLOR_BGR2RGB)
    cv2.imwrite(img_saida,imagem)
    return 'Arquivo Salvo com sucesso!!'

def salvarImagemSegmentadaDisco (img_entrada, img_saida): # imagem de saída deve vir no formato 'nome_imagem.jpg'
    cv2.imwrite(img_saida,img_entrada)
    return 'Arquivo Salvo com sucesso!!'    

def gravarArquivoCSV(valor, arq_saida):
    f = open(str(fun.path) + str(arq_saida) , 'w', newline='', encoding='utf-8')
    # Criar o objeto de gravação
    w = csv.writer(f)
    # Gravar a matriz
    w.writerow(valor)
    # Fechamento do arquivo
    f.close()
    return "Arquivo CSV gravado com sucesso em " + str(fun.path) + str(arq_saida)

def salvarMatrizArquivoCSV (matriz, arq_saida):  
    altura, largura = matriz.shape

    # criar o arquivo
    f = open(str(path) + str(arq_saida) , 'w', newline='', encoding='utf-8')
    # Criar o objeto de gravação
    w = csv.writer(f)
    try:
        # Gravar a matriz
        for i in range(largura):
            for j in range(altura):
                w.writerow(matriz[j])
        # Fechamento do arquivo
        f.close()
    except:
        print("Falha em Salvar o arquivo")
    
    return "Arquivo CSV gravado com sucesso em " + str(path) + str(arq_saida)

def gravarArquivoCSV(text, arq_saida):
    f = open(str(path) + str(arq_saida) , 'w', newline='', encoding='utf-8')
    # Criar o objeto de gravação
    w = csv.writer(f)
    # Gravar a matriz
    w.writerow(text)
    # Fechamento do arquivo
    f.close()
    
    return "Arquivo CSV gravado com sucesso em " + str(path) + str(arq_saida)

def separaCanaisCoresPlotaGrafico(img, titulo):
    canais= cv2.split(img)
    cores= ("b", "g", "r")
    plt.figure()
    plt.title(titulo)
    plt.xlabel("Intensidade")
    plt.ylabel("Número de Pixels")
    for (canal, cor) in zip(canais, cores):
    #Este loop executa 3 vezes, uma para cada canal
        hist = cv2.calcHist([canal], [0], None, [256], [0, 256])
        plt.plot(hist)
        plt.xlim([0, 256])
        # Calcula o valor de Pico para cada Canal
        ymax = max(hist)
        xmax, _ = np.where(hist == ymax)
        if (cor == "b"):
            print('Valor de Pico - Canal Azul:')
        if (cor == "g"):
            print('Valor de Pico - Canal Verde:')
        if (cor == "r"):
            print('Valor de Pico - Canal Vermelho:')
        print(ymax, xmax)
    plt.show()
    
    return 'Gráfico Plotado com sucesso!!'

def plotaGraficoCanaisImagem(img):
    img_red = img[:,:,0]     # Canal vermelho
    img_green = img[:,:,1]   # Canal verde
    img_blue = img[:,:,2]    # Canal azul

    plt.figure(figsize=[35, 35])
    plt.subplot(1, 3, 1)
    plt.imshow(img_red, 'gray', vmin=0, vmax=255)  # vmin define o valor associado ao preto e vmax o valor da cor branca
    plt.title('Vermelho')
    plt.subplot(1, 3, 2)
    plt.imshow(img_green, 'gray', vmin=0, vmax=255)
    plt.title('Verde')
    plt.subplot(1, 3, 3)
    plt.imshow(img_blue,'gray', vmin=0, vmax=255)
    plt.title('Azul')
    
    return img_red, img_green, img_blue


def imprimirHistogramasPorCanalRGB(img):

    img_red = img[:,:,0]     # Canal vermelho
    img_green = img[:,:,1]   # Canal verde
    img_blue = img[:,:,2]    # Canal azul
        
    # Histogramas individuais por canal (RGB)

    plt.figure(figsize=[15, 5])
    plt.subplot(1, 3, 1)
    hist_r= plt.hist(img_red)
    plt.title('Canal Vermelho')
    plt.subplot(1, 3, 2)
    hist_r= plt.hist(img_green)
    plt.title('Canal Verde')
    plt.subplot(1, 3, 3)
    hist_r= plt.hist(img_blue)
    plt.title('Canal Azul')
    return 'Gráfico plotado com sucesso!!'

def gravarMatrizImagemArquivoRGB(img, nomeArquivo): # o parâmetro "nome arquivo" deve ser no formato 'nome_arquivo.jpg'
    #Gravar a matriz completa da Imagem original em Arquivo
    # Para facilitar a visualização dos dados
    text = ''
    for row in img:
        for e in row:
            text += '({}, {}, {}) '.format(e[0], e[1], e[2])
        text += '\n'

    # Grava a String em arquivo
    with open(nomeArquivo, 'w') as f:
        f.write(text)
    return 'Arquivo gravado com sucesso!!'

def gravarMatrizImagemArquivo(img, nomeArquivo): # o parâmetro "nome arquivo" deve ser no formato 'nome_arquivo.jpg'
    #Gravar a matriz completa da Imagem original em Arquivo
    # Para facilitar a visualização dos dados
    text = ''
    for row in img:
        for e in row:
            text += '({}) '.format(e)
        text += '\n'

    # Grava a String em arquivo
    with open(nomeArquivo, 'w') as f:
        f.write(text)
    return 'Arquivo gravado com sucesso!!'

def detectarBordasCanny (img,lim1, lim2):
    borda = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(borda,lim1,lim2)
    return canny

def caracteristicasImagem (img): # buscar outras funções para completar
    global larguraImgOriginal
    global alturaImgOriginal
    global numCanaisImgOriginal
    global totalPixelsImgOriginal

    larguraImgOriginal = img.shape[1]
    alturaImgOriginal = img.shape[0]
    numCanaisImgOriginal = img.shape[2]
    totalPixelsImgOriginal = img.size
        
    print("Tipo de dados:" +str(img.dtype))
    print("Largura: {} pixels".format(larguraImgOriginal))
    print("Altura: {} pixels".format(alturaImgOriginal))
    print("Canais: {}".format(numCanaisImgOriginal))
    print("Número de elementos do array:" + str(totalPixelsImgOriginal))

    return larguraImgOriginal, alturaImgOriginal, numCanaisImgOriginal, totalPixelsImgOriginal

def elbow (img):
    wcss = []
    data = img.reshape(img.shape[0]*img.shape[1], 3)
    for i in range(1, 11):
        kmeans = KMeans(n_clusters = i, init = 'random')
        kmeans.fit(data)
        print (i,kmeans.inertia_)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1, 11), wcss)
    plt.title('O Metodo Elbow')
    plt.xlabel('Numero de Clusters')
    plt.ylabel('Soma dos quadrados do cluster') 
    return 'Gráfico gerado com sucesso!!'

def crop_image(img_disco,left,top,right,bottom): # formato da "img_disco.jpg"
    
    # Abrir a imagem gravada em disco
    im = Image.open(img_disco)
    
    # Imagem cortada de acordo com a dimensão
    img_crop = im.crop((left, top, right, bottom))

    return img_crop


def threshold(img, th1, th2):
    
    largura, altura = img.shape
    # Submeter ao primeiro limiar
    for lin in range(largura):
        for col in range(altura):
            if (img[lin,col]<th1):
                img[lin,col]=255           
    # Resultante
    img_th = img

    #Submeter ao segundo limiar
    for lin in range(largura):
        for col in range(altura):
            if (img_th[lin,col]>th2):
                img_th[lin,col]=255            
        
    return img_th


def histogramaImagem(img,num_bins):
    #num_bins => Número de caixas no histograma
    bin_size = 256/num_bins   # Tamanho de cada caixa

    hist = np.zeros(num_bins)
    num_rows, num_cols = img.shape
    for row in range(num_rows):
        for col in range(num_cols):
            bin_index = img[row, col]/bin_size
            bin_index = int(bin_index)
            hist[bin_index] += 1

    # Cálculo do intervalo de cada caixa, utilizando a função linspace do numpy      
    bins_values = np.linspace(0, 256, num_bins)    
    plt.bar(bins_values, hist, bin_size, edgecolor='k')
    return 'Histograma gerado com sucesso!!'

def binarizarImagem(img, th1, th2):
    largura, altura = img.shape
    for lin in range(0,largura):
        for col in range(0,altura):
         if(img[lin][col]>= th1 and img[lin][col]<= th2):
            img[lin][col] = 1
        else:
            img[lin][col] = 0
    
    return img

def simularDoencaFolha(img1, img2, img_ref): # entrada com matrizes de mesmo tamanho
    # Imagem com a doença
    linha, coluna = img1.shape
    # Imagem de referência
    linha2, coluna2, canais = img2.shape
    img_comp = img2[:,:,1].copy()

    # Atribuir os pixels coloridos da imagem 1 para a imagem 2
    for lin in range(linha2):
        for col in range(coluna2):
            if (img1[lin, col] != 255) & (img_comp[lin, col] >= 240):
              img2[lin, col] = img_ref[2258,1710]
    
    return img2

def calcularLimiares(vetorSemente, variavelOperacao, sigma, peso1=10, peso2=90): 
    # Variável operação: 1: variância polulacional; 2:variância amostral, 3:média aritmética, 4:mediana, 5:média ponderada

    if sigma >2:
        print("Erro no valor de sigma. São aceitos os valores 1 ou 2!!")
        return 0, 0, 0, 0, 0, 0

    if variavelOperacao >5:
        print("Erro no valor da Operação. São aceitos os valores de 1 até 4!!")
        return 0, 0, 0, 0, 0, 0
    
    elif (variavelOperacao ==1):
        global op
        valor = st.pvariance(vetorSemente)
        op = "variância populacional"

    elif (variavelOperacao ==2):
        valor = st.variance(vetorSemente)
        op = "variância amostral"

    elif (variavelOperacao ==3):
        valor = st.mean(vetorSemente)
        op = "média"

    elif (variavelOperacao ==4):
        valor = st.median(vetorSemente)
        op = "mediana"

    elif (variavelOperacao ==5):
        valor1 = 0
        valor2 = 0
        
        for i in range(0,3):
            valor1+=vetorSemente[i]*(peso1/3)
            # print(valor1) # conferir os valores 
        for j in range(3,20):
            valor2+=vetorSemente[j]*(peso2/17)
            # print(valor2) # conferir os valores
            
        valor = (valor1+valor2)/(peso1+peso2)
        op = "média ponderada"
    global var, th1, th2, dp
    var = st.pvariance(vetorSemente)
    dp = np.sqrt(var)
    th1 = math.floor(valor - sigma*dp)
    th2 = math.ceil(valor + sigma*dp)
    data = [th1, int(th1+(th2-th1)/2), th2]
    
    return th1, th2, dp, op, var, valor

def calcularJanela(coord_x,coord_y,tamanho):
    # Esta função calcula uma janela dinâmica a partir de um ponto central c/ (cordenadas x e y) informadas;
    # Implementa a ideia de construir retas perpendiculares a partir do ponto central;
    # O último ponto de cada reta é utilizado para construir a janela;
    # É passado o tamanho em pixels para construir cada reta;
    # Coordenadas 1 de saída (coluna) deverá ser: y(D,B); 
    # Coordenadas 2 de saída (coluna) deverá ser: y(D,A); 

    # Inicialização das listas
    lista_ax, lista_ay, lista_bx, lista_by, lista_dx, lista_dy = [], [], [], [], [], []

    # Aumentar X e Y de acordo com o "tamanho"
    lista_ax = list(range(coord_x, coord_x + tamanho,1))
    lista_ay = list(range(coord_y, coord_y + tamanho,1))
    # Diminuir X e Y de acordo com o "tamanho"
    lista_bx = list(range(coord_x, coord_x - tamanho,-1)) # valor "-1" obter valores decrescentes no "range"
    lista_by = list(range(coord_y, coord_y - tamanho,-1))
    # Diminuir X e aumentar Y de acordo com o "tamanho"
    lista_dx = list(range(coord_x, coord_x - tamanho,-1))
    lista_dy = list(range(coord_y, coord_y + tamanho,1))
    
    # retorna o último elemento de cada lista
    return lista_dx.pop(), lista_ax.pop(), lista_dy.pop(), lista_by.pop()


def calcularVizinhanca(imagem, corPixelReferencia, val_lin_win=0, val_2_lin_win=0, val_col_win =0, val_2_col_win=0):
    # Armazenamento de dados da janela
    dados = []
    # Flag auxiliar
    flag =1
    # Armazenamento do resultado para gravar em arquivo
    text = ''
    # Percorrer a imagem (todos os pixels) de acordo com sua vizinhança;
    # Escolher a 
    for x in range(val_lin_win, val_2_lin_win):
        for y in range(val_col_win, val_2_col_win):
            
            if(imagem[x,y]) == corPixelReferencia:
                # Janela 5x5 de dados a partir do pixel a ser analisado
                dados = [imagem[x,y], imagem[x,y+1], imagem[x,y-1], imagem[x,y+2], imagem[x,y-2], \
                        imagem[x+1,y], imagem[x+1,y+1], imagem[x+1,y-1], imagem[x+1,y+2], imagem[x+1,y-2], \
                        imagem[x+2,y], imagem[x+2,y+1], imagem[x+2,y-1], imagem[x+2,y+2], imagem[x+2,y-2], \
                        imagem[x-1,y], imagem[x-1,y+1], imagem[x-1,y-1], imagem[x-1,y+2], imagem[x-1,y-2], \
                        imagem[x-2,y], imagem[x-2,y+1], imagem[x-2,y-1], imagem[x-2,y+2], imagem[x-2,y-2]]                    
            
                # Conversão de "dados" (String para Inteiro)
                global sementes, erro
                sementes = list(map(int, dados))

                # Calcular a mediana e desvio padrão dos dados com a função de cálculo de limiares
                th1, th2, dp, op, var, valor = fun.calcularLimiares(sementes,4,1)

                # Calcular o Erro com base nos valores de desvio padrão e mediana
                erro = (dp*100)/valor
                
                # Condição para armazenar o primeiro valor do erro para depois ser comparado
                if flag == 1:
                    result_erro = erro
                    flag+=1
                    coordenada_x = imagem[x]
                    coordenada_y = imagem[y]
                
                if flag >1 and erro < result_erro and valor == corPixelReferencia:
                    result_sementes = sementes
                    result_erro = erro
                    coordenada_x = y
                    coordenada_y = x
                    result_valor =  valor
                    text+= "sementes: " + str(result_sementes) + " - Coordenadas: " + " x= " + str(coordenada_x) + " y= " + str(coordenada_y) + " - Erro calculado: " \
                            + str(result_erro) +  " - Valor de Mediana: " + str(result_valor) + "\n"

    # Inserir os resultados finais do processamento
    text+= "\n\n==================================================================================\n\n"
    text+= "Sementes Selecionadas (finais): " + str(result_sementes) + "\n" + "Coordenadas selecionadas (finais): " + " x= " + str(coordenada_x) + " y= " + str(coordenada_y,)\
            + "\n" + "Erro calculado (final): " + str(result_erro) + " - Mediana (final): " + str(result_valor)
    text+= "\n\n=================================================================================="

    return coordenada_x, coordenada_y, result_erro, text

# ----------------------------------------------------------------
# Funcionalidades para banco de dados Mysql
# ----------------------------------------------------------------

def connect_DB_Open():
    
    # Configuração da Cloud
    con = mysql.connector.connect(host='xxx.xxx.xxx.xxx', database='xxxxxx', user='xxx', password='xxxxx')
   
    if con.is_connected():
        db_info = con.get_server_info()
        print("Conectado em Mysql - versão: ", db_info)
        cursor = con.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("--------------------------------------------")
        print("Conectado ao DB: " + str(linha))
    else:
        print("Erro na conexão com o BD!")
        
    return con

def connect_DB_Close(cursor, con):
    if con.is_connected():
        cursor.close()
        con.close()
        mensagem = "Conexão com DB encerrada!! \n"
    else:
        mensagem = "Não foi possível encerrar a conexão. Verificar se há conexão ativa!"
    
    return mensagem

def inserir_cadTestes(nome_teste, tipo_teste):
    # Definição da String SQL
    sql_insert_cad_testes = "INSERT INTO cad_testes (id_teste, nome_teste, tipo_teste)" + \
            " VALUES (null," + '\'' + nome_teste + '\',\'' +  tipo_teste + '\')'
     
    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_insert_cad_testes)
            con.commit()
            mensagem = cursor.rowcount, " registro(s) inserido(s) com sucesso em Cadastro de Testes!!"
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        mensagem= "Falha ao inserir dados em cad_testes: {}".format(erro)              
    
    return mensagem

def buscaID_cadTestes():
# Definição da String SQL
    sql_select_last_ID = 'SELECT MAX(id_teste) FROM cad_testes'

    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_select_last_ID)
            id = cursor.fetchone()
            print(connect_DB_Close(cursor,con))
                        
    except Error as erro:
        print("Falha na busca do ID do Cadastro de Testes: {}".format(erro))

    return id

def inserir_cadSementes(descricao_cor_semente, cor_RGB_semente, dados_sementes):
    # Definição da String SQL
    sql_insert_cad_sementes = "INSERT INTO cad_sementes (id_semente, descricao_cor_semente, cor_RGB_semente, dados_sementes) \
            VALUES (null," + '\'' + descricao_cor_semente + '\',\'' +  cor_RGB_semente + '\',\'' + dados_sementes  + '\')'
    
    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_insert_cad_sementes)
            con.commit()
            mensagem = cursor.rowcount, " registro(s) inserido(s) com sucesso em Cadastro de Sementes!!"
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        mensagem= "Falha ao inserir dados em cad_sementes: {}".format(erro)
        print(connect_DB_Close(cursor, con))

    return mensagem

def buscaID_cadSementes():
# Definição da String SQL
    sql_select_last_ID = 'SELECT MAX(id_semente) FROM cad_sementes'

    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_select_last_ID)
            id = cursor.fetchall()            
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        print("Falha na busca do ID do Cadastro de Sementes: {}".format(erro))

    return id

def inserir_cadSegmentacao(id_cadastro_teste, id_cadastro_semente, data_hora_teste, coordenadas_semente_central, coordenadas_calc_janela, total_pixels_janela, sementes_calculadas_janela, \
        total_sementes_calculadas, erro_estatistico_calculado, operacao_teste, desvio_padrao_teste, limiar_1_teste, limiar_2_teste, faixa_limiares, variancia_teste, img_janela,           \
        descricao_img_original, tipo_img_original, largura_img_original, altura_img_original, num_canais_img_original, total_pixels_img_original, img_original, img_filtro_mediana,        \
        img_canal_verde, img_limiarizada, img_processada_limiarizacao, relatorio_coleta_aut_semente, relatorio_dados_estatisticos, coord_janela_final_obj_interesse):

    # Definição da String SQL
    sql_insert_cad_segmentacao = sql_insert_cad_segmentacao = "INSERT INTO cad_segmentacao (id_cad_segmentacao, id_cadastro_teste, id_cadastro_semente, data_hora_teste, coordenadas_semente_central, coordenadas_calc_janela,    \
        total_pixels_janela, sementes_calculadas_janela, total_sementes_calculadas, erro_estatistico_calculado, operacao_teste, desvio_padrao_teste, limiar_1_teste, limiar_2_teste, faixa_limiares, \
        variancia_teste, img_janela, descricao_img_original, tipo_img_original, largura_img_original, altura_img_original, num_canais_img_original, total_pixels_img_original, img_original,         \
        img_filtro_mediana, img_canal_verde, img_limiarizada, img_processada_limiarizacao, relatorio_coleta_aut_semente, relatorio_dados_estatisticos, coord_janela_final_obj_interesse) VALUES (null," \
                +  str(id_cadastro_teste) + "," +  str(id_cadastro_semente) + ",'" + str(data_hora_teste) + "','" + str(coordenadas_semente_central) + "','" + str(coordenadas_calc_janela) + "'," +     \
                str(total_pixels_janela) + ",'" + str(sementes_calculadas_janela) + "'," + str(total_sementes_calculadas) + "," + str(erro_estatistico_calculado) + ",'" + str(operacao_teste) + "'," +  \
                str(desvio_padrao_teste) + "," + str(limiar_1_teste) + ","  + str(limiar_2_teste) + ",'" + str(faixa_limiares) + "'," + str(variancia_teste) + ",'" + str(img_janela) + "','" +          \
                str(descricao_img_original) + "','" + str(tipo_img_original) + "'," + str(largura_img_original) + "," + str(altura_img_original) + "," + str(num_canais_img_original) + "," +            \
                str(total_pixels_img_original) + ",'" + str(img_original) + "','" + str(img_filtro_mediana) + "','" + str(img_canal_verde) + "','" + str(img_limiarizada) + "','" +                        \
                str(img_processada_limiarizacao) + "','" + str(relatorio_coleta_aut_semente) + "','" + str(relatorio_dados_estatisticos) + "','" + str(coord_janela_final_obj_interesse) + "')"
            
    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_insert_cad_segmentacao)
            con.commit()
            mensagem = cursor.rowcount, "Registro(s) inserido(s) com sucesso em Cadastro de Segmentação!!"
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        mensagem= "Falha ao inserir dados em cad_segmentação: {}".format(erro)
        print(connect_DB_Close(cursor, con))      
    
    return mensagem

def buscaID_cadSegmentacao():
# Definição da String SQL
    sql_select_last_ID = 'SELECT MAX(id_cad_segmentacao) FROM cad_segmentacao'

    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_select_last_ID)
            id = cursor.fetchall()            
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        print("Falha na busca do ID do Cadastro de Segmentação: {}".format(erro))

    return id

def inserir_rotulosSegmentados(img_rotulo_segmentado, id_cad_segmentacao):
                 
    con = connect_DB_Open()
    
    try:
        if con.is_connected():
            cursor = con.cursor()

            for img in img_rotulo_segmentado:                            
                # Definição da String SQL
                sql_insert_rotulos_segmentados = "INSERT INTO rotulos_segmentados (id_rotulo_segmentado, img_rotulo_segmentado,\
                    id_cad_segmentacao) VALUES (null,'" + str(img) + "'," + str(id_cad_segmentacao)  + ")"
                cursor.execute(sql_insert_rotulos_segmentados)
                con.commit()
            
            mensagem = cursor.rowcount, " registro(s) inserido(s) com sucesso em Cadastro de Rótulos Segmentados!!"
            print(connect_DB_Close(cursor,con))
    except Error as erro:
        mensagem= "Falha ao inserir dados em Rotulos Segmentados: {}".format(erro)
        print(connect_DB_Close(cursor, con))
        
    return mensagem

def ler_imagem_DB():
    # Definição da String SQL
    sql_select_img = 'SELECT img_original FROM cad_segmentacao where id_cad_segmentacao = 1'

    con = connect_DB_Open()

    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_select_img)
            img = cursor.fetchall()
            print(img)                                   
        mensagem = connect_DB_Close(cursor,con)
    except Error as erro:
        mensagem = "Falha na busca da Imagem do Cadastro de Segmentação: {}".format(erro)

    return img

def update_imagens(path_imagem, tabela, id_tabela, coluna_tabela, valor_id_tabela):
    # Definição da String SQL
    sql_update = "UPDATE " + str(tabela) + " set " + str(coluna_tabela) + " = LOAD_FILE(" + "'" + str(path_imagem) + "'" + ") WHERE " +  str(id_tabela) + " = " + str(valor_id_tabela)
    
    mensagem = sql_update
    
    con = connect_DB_Open()
      
    try:
        if con.is_connected():
            cursor = con.cursor()
            cursor.execute(sql_update)
                                            
        mensagem = connect_DB_Close(cursor,con)
    except Error as erro:
        mensagem = "Falha na rotina de UPDATE: {}".format(erro)
    
    return mensagem

# ----------------------------------------------------------------
# Funcionalidades Oracle Cloud
# ----------------------------------------------------------------

# Definição das configurações
def configuration_Cloud():
    
    config = oci.config.from_file()
    
    # Initialize service client with default config file
    object_storage_client = oci.object_storage.ObjectStorageClient(config)

    return object_storage_client

def resource():
   
    # Configuração para uso na Cloud Oracle
    
    resource = boto3.resource('s3',
                                aws_access_key_id="ver conta na cloud",
                                aws_secret_access_key="ver conta na cloud",
                                region_name="ver conta na cloud",
                                endpoint_url="ver conta na cloud")
                               
    return resource

# Busca de objetos do bucket selecionado
def getObjectsToBucket(bucket, resource_value):
    objectsBucket = resource_value.Bucket(bucket)
    files = list(objectsBucket.objects.all())
    return files

# Chamda do Client com a definição endpoint
def client_s3(url):
    response = boto3.client('s3', endpoint_url=url)
    return response

# Função de download de arquivos do Bucket para o espaço de trabalho
def download_to_bucket(bucket,url,files,path):
    '''
    Files: O nome do conjunto de chaves (array) para baixar de
    Filename: O caminho para o arquivo a ser baixado
    ExtraArgs: Argumentos extras que podem ser passados para a operação do cliente
    Config: A configuração de transferência a ser usada ao realizar a transferência
    '''
    try:
        client =fun.client_s3(url)
        
        for file in files:             
            client.download_file(bucket,file.key, path + file.key.split('/')[-1])
            
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Função de upload de arquivos dos arquivos do espaço de trabalho para o Bucket selecionado
def upload_from_bucket(bucket, url, file_name, object_name=None, args=None):
    '''
    file_name: nome do arquivo local
    bucket: bucket_name
    object_name: nome do arquivo no bucket
    args: argumentos customizados
    '''
    try:
        client =client_s3(url)

        if object_name is None:
            object_name = file_name

        client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
        
    except ClientError as e:
        logging.error(e)
        return False
    return True
   
