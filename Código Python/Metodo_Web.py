#------------------------------------------------------------------------#
#------------------------------------------------------------------------#
# INTERFACE DE USUÁRIO WEB - VERSÃO 1.0                                  #
# DOUTORADO - PERÍODO: 2019 - 2024                                       #
# INSTITUIÇÕES: UNIVERSIDADE FEDERAL DE SÃO CARLOS - UFSCar              #
#               EMBRAPA INSTRUMENTAÇÃO - SÃO CARLOS                      #
#               INSTITUTO FEDERAL DE SÃO PAULO - IFSP                    #         
# DOUTORANDO: RICARDO ALEXANDRE NEVES                                    #
# ORIENTADOR: DR.PAULO ESTEVÃO CRUVINEL                                  #
# TECNOLOGIAS: PYTHON 3, STREAMLIT (FRAMEWORK WEB), ORACLE DATABASE      #
# AMBIENTE ORACLE CLOUD                                                  #
#------------------------------------------------------------------------#
#------------------------------------------------------------------------#

# Bibliotecas
import cx_Oracle
import os
import io
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import CirclePolygon
from datetime import datetime, timedelta
import numpy as np
from scipy import stats
import scipy.interpolate as interpolate
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import math
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from hmmlearn import hmm
import cv2
from statistics import median
import warnings
import base_regras_fuzzy as regras
import functions as fun
from datetime import date, timedelta
from docx import Document
from docx.shared import Inches
import streamlit as st
import streamlit.components.v1 as components
import base64
import streamlit_nested_layout
import timeit
import time
# Ignorar os avisos de Warnings
warnings.filterwarnings('ignore')

# Verificar a versão do Pandas (Pré-requisito 1.3.1)
#print("Versão do Pandas: %s" % pd.__version__)

#------------------------------------------------------------------------------------------------
# Configurações Globais:

# Definição de Casas Decimais
casas_decimais=1

# Variável global para acumular os Resultados das Abordagens para o Relatório Final
global text
text=""

# Variável para definição de Intervalo de Janela de Tempo
intervalo=9

# Definição da Variável de ambiente - Acesso Oracle Database - Aplicação em Cliente Oracle
#os.environ['TNS_ADMIN']='/lib/oracle/21/client64/lib'
# print(os.environ.get('TNS_ADMIN'))

# Definição de Path (Gravação de arquivos)
path_2='fusao_dados/'
# Criação de diretório
if not os.path.exists(path_2):
    os.makedirs(path_2)

# Definição de Path (Gravação de Relatórios)
path_3='fusao_dados/relatorios/'
# Criação de diretório
if not os.path.exists(path_3):
    os.makedirs(path_3)

# Definição de Path (Gravação de Códigos SQL)
path_4='fusao_dados/codigosSQL/'
# Criação de diretório
if not os.path.exists(path_4):
    os.makedirs(path_4)

# Definição dos Paths dos Relatórios do Data Warehouse (Cloud)
#relatorio_assunto_1='/home/opc/dashboard/Relatorios_WEB/Relatorio_Assunto_1.pdf'
#relatorio_assunto_2='/home/opc/dashboard/Relatorios_WEB/Relatorio_Assunto_2.pdf'
#relatorio_assunto_3='/home/opc/dashboard/Relatorios_WEB/Relatorio_Assunto_3.pdf'
#relatorio_qualidade_DW='/home/opc/dashboard/Relatorios_WEB/Relatorio_Qualidade_DW.pdf'

# Definição dos Paths dos Relatórios do Data Warehouse (Local)
relatorio_assunto_1='C:\\Users\\ratec\\OneDrive\\Documentos\\Códigos_Tese\\Relatorios_WEB\\Relatorio_Assunto_1.pdf'
relatorio_assunto_2='C:\\Users\\ratec\\OneDrive\\Documentos\\Códigos_Tese\\Relatorios_WEB\\Relatorio_Assunto_2.pdf'
relatorio_assunto_3='C:\\Users\\ratec\\OneDrive\\Documentos\\Códigos_Tese\\Relatorios_WEB\\Relatorio_Assunto_3.pdf'
relatorio_qualidade_DW='C:\\Users\\ratec\\OneDrive\\Documentos\\Códigos_Tese\\Relatorios_WEB\\Relatorio_Qualidade_DW.pdf'

#------------------------------------------------------------------------------------------------
# Configurações de Página Dashboard
st.set_page_config(layout="wide")

# Criação de Conteiners em "Abas"
tab4, tab5, tab3, tab6, tab2, tab1 = st.tabs(["Sobre o Projeto","🗃Processamento de Imagens","🗃Relatório Técnico",\
                                                    "🗃Qualidade de Dados","🗃Recomendações","🗃Dashboard"])

with tab1: # Aba "Dashboard"
    
    # Criar colunas - Exibição de Conteiner Relatórios Auxílio Tomada Decisão (DW)
    dash_col_0_1, dash_col_0_2, dash_col_0_3= st.columns([0.2,1.8,0.7], gap="medium")
        
    # Criar as duas primeiras colunas
    dash_col_1_1, dash_col_1_2, dash_col_1_3= st.columns([0.0001,2.5,0.7], gap="medium")

    # Criar outras duas colunas em seguida
    dash_col_2_1, dash_col_2_2, dash_col_2_3, dash_col_2_4 = st.columns([0.7,0.75,1.2,0.6], gap="medium")

with tab3: # Aba "Relatório Técnico"
    # Criar as duas primeiras colunas
    dash_3_col_1_1, dash_3_col_1_2= st.columns([4.7,0.5], gap="medium")

    # Criar outras quatro colunas em seguida
    dash_3_col_0_3, dash_3_col_1_3, dash_3_col_2_3, dash_3_col_3_3 = st.columns([0.9,1.5,1.5,1.4], gap="medium")

with tab6: # Aba "Qualidade de Dados"    
    # Criar as colunas iniciais
    dash_6_col_2_1, dash_6_col_2_2, dash_6_col_2_3 = st.columns([0.2,0.7,1.5], gap="medium")

    # Criar outras colunas em seguida
    dash_6_col_3_1, dash_6_col_3_2, dash_6_col_3_3 = st.columns([0.1,2,0.1], gap="medium")

with tab4: # Aba "Sobre o Projeto"
    # Logo da Aplicação WEB
    st.image('logo_V1.png', width=400)
    
    # Breve descrição do Projeto
    components.html(
        """
            <html>
                <hr size = 1>
                <p style="text-align: center;"><strong>Doutorado em Ci&ecirc;ncia da Computa&ccedil;&atilde;o</strong></p>
                <p style="text-align: center;"><strong>Programa de P&oacute;s-Gradua&ccedil;&atilde;o em Ci&ecirc;ncia da Computa&ccedil;&atilde;o (PPGCC)</strong></p>
                <p style="text-align: center;"><strong>&Aacute;rea de Concentra&ccedil;&atilde;o: Vis&atilde;o Computacional</strong></p>
                <p style="text-align: justify;"><strong><span style="text-align: justify; text-decoration-line: underline;">Pesquisa Intitulada</span><span style="text-align: justify;">: </span></strong>M&eacute;todo Avan&ccedil;ado para Integra&ccedil;&atilde;o de Conhecimentos Clim&aacute;ticos e de Imagens Digitais para o Monitoramento da Ferrugem Asi&aacute;tica na Cultura da Soja em Ambiente Cloud.</p>
                <div>
                    <ul>
                    <li style="text-align: justify;"><strong>Doutorando: Ricardo Alexandre Neves, Me.</strong></li>
                    <li style="text-align: justify;"><strong>Orientador: Paulo Estev&atilde;o Cruvinel, Professor Dr.</strong></li>
                    </ul>
                </div>
                <div>
                    <p style="text-align: justify;"><strong><u>Institui&ccedil;&otilde;es Envolvidas:</u> </strong></p>
                </div>
                <div>
                    <ul>
                    <li style="text-align: justify;">Universidade Federal de S&atilde;o Carlos (UFSCar) - S&atilde;o Carlos;</li>
                    <li style="text-align: justify;">Embrapa Instrumenta&ccedil;&atilde;o - S&atilde;o Carlos;</li>
                    <li style="text-align: justify;">Instituto Federal de S&atilde;o Paulo - <em>Campus</em> de S&atilde;o Jo&atilde;o da Boa Vista - SP.</li>
                    </ul>
                    <p style="text-align: justify;"><span style="color: #0000ff;">&Eacute; vi&aacute;vel o monitoramento durante o per&iacute;odo de cultivo (Ciclo de Cultura) com a utiliza&ccedil;&atilde;o das S&eacute;ries Temporais de Dados e uso de Janelamento para Amostragens Consecutivas em subper&iacute;odos de 10 dias. O primeiro per&iacute;odo de janelamento deve ser informado considerando a data inicial da ocorr&ecirc;ncia.</span></p>
                </div>
                <div>
                    <p>A Interface de Usu&aacute;rio est&aacute; organizada da seguinte forma:</p>
                </div>
                <div>
                    <ol>
                    <li style="text-align: justify;"><strong>Aba Processamento de Imagens</strong>: S&atilde;o exibidos os resultados (Imagens, C&aacute;lculos e Estat&iacute;sticas) do Processamento das Imagens nas Etapas 1 e 2 do Processo de Segmenta&ccedil;&atilde;o;&nbsp;</li>
                    <li style="text-align: justify;"><strong>Aba Relat&oacute;rio T&eacute;cnico:</strong>&nbsp;S&atilde;o exibidos&nbsp;os dados t&eacute;cnicos e gr&aacute;ficos referentes ao processamento&nbsp;&nbsp;realizado, de acordo com a janela de tempo definida;</li>
                    <li style="text-align: justify;"><strong>Aba Qualidade de Dados</strong>: S&atilde;o exibidos os dados de M&eacute;tricas <strong>MSE</strong>(<strong>Mean Squared Error</strong>), <strong>PSNR</strong>(<strong>Peak Signal-to-Noise Ratio</strong>), <strong>SSIM</strong>(<strong>Structural Similarity Index Measure</strong>);&nbsp;os <strong>Histogramas </strong>das Imagens, resultado da compara&ccedil;&atilde;o das Imagens Segmentadas na Etapa 1 e ap&oacute;s Processamento na Etapa 2; Os Gr&aacute;ficos Boxplot referentes aos dados dos "Pixels Sementes" antes e depois do Processamento com foco na Redu&ccedil;&atilde;o ou Elimina&ccedil;&atilde;o dos "Outliers";</li>
                    <li style="text-align: justify;"><strong>Aba Recomenda&ccedil;&otilde;es</strong>: Exibe o resultado do M&eacute;todo; Uma tabela de tratamentos para o controle da Ferrugem Asi&aacute;tica da Soja (F.A.S.), via Protocolos de Experimentos realizados pela EMBRAPA Soja e; Uma orienta&ccedil;&atilde;o para Boas Pr&aacute;ticas para Manejo da Soja;</li>
                    <li style="text-align: justify;"><strong>Aba Dashboard</strong>: Permite ao usu&aacute;rio realizar o processamento do M&eacute;todo para avalia&ccedil;&atilde;o da Favorabilidade da F.A.S. e visualizar os resultados no formato Dashboard; S&atilde;o exidos tamb&eacute;m os Relat&oacute;rios para Aux&iacute;lio &agrave; Tomada de Decis&atilde;o, de acordo com os Requisitos previstos no Projeto, frente a modelagem Multidimensional Elaborada, via Data Warehouse.</li>
                    </ol>
                </div>
            </html>
        """
        ,height=700)
#------------------------------------------------------------------------------------------------

# Função para Entrada de Data da Janela de Tempo
def dataJanelaTempo(intervalo, data, input_data):

    # Definição de Datas para uso na Janela de Tempo
    # Formato de data aceito: dd/mm/yyyy
    # Definição de Período da Janela de Tempo (em dias)
    periodo=timedelta(intervalo)

    # Verifica se o formato de data de entrada está correto
    #   Caso não esteja correto o formato "Digite novamente"
    while True:
        try:
            if data==0:
                #input_data = input('Entre com a Data Inicial da Janela de Tempo (dd/mm/yyyy): ')
                data_inicial = datetime.strptime(input_data, '%d/%m/%Y').date()
                break
            else:
                input_data = data
                data_inicial = datetime.strptime(input_data, '%d/%m/%Y').date()
                break
        except ValueError:
            print('Data em formato inválido, tente novamente!')

    # Atribuição da leitura da Data Final
    data_final=data_inicial + periodo

    # Formatar data para String (Entrada na Instrução SQL)
    DataInicial ="'" + data_inicial.strftime('%d/%m/%Y') + "'"
    DataFinal ="'" +data_final.strftime('%d/%m/%Y')+ "'"
    print("Datas Formatadas para uso em Consulta SQL (ORACLE)\n-------------------------------------------------")
    print("Data Inicial:", DataInicial, "e Data Final:", DataFinal)

    # Exibir as datas Inicial e Final na Dashboard
    st.sidebar.header("Janela Temporal:")
    st.sidebar.text("Data Inicial:"+ str(DataInicial).strip("'"))
    st.sidebar.text("Data Final:"+ str(DataFinal).strip("'"))

    return DataInicial, DataFinal

#------------------------------------------------------------------------------------------------

# Função para conexão com o Oracle Autonomous Database
def conexaoAutonomousDatabase(PYTHON_USERNAME,PYTHON_PASSWORD,PYTHON_CONNECTSTRING):
    # Objeto de Conexão
    connection=None
    try:
        connection = cx_Oracle.connect(user=PYTHON_USERNAME, password=PYTHON_PASSWORD, dsn=PYTHON_CONNECTSTRING, encoding="UTF-8") 
    
    except cx_Oracle.Error as error:
        print(error)
    
    return connection

#------------------------------------------------------------------------------------------------

# Função para Filtro das Regiões dos Dados Climáticos Cadastrados
def filtrarRegiao():
    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql="SELECT DISTINCT REGIAO_ESTACAO_CLIMATICA FROM DADOS_CLIMATICOS"
            
            # Carregar o resultado da consulta de Região no Dataframe
            listar_regioes=pd.DataFrame(cursor.execute(sql), columns=['regiao'])

    # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    return listar_regioes

#------------------------------------------------------------------------------------------------

# Função para Filtro das Localidades dos Dados Climáticos
def filtrarLocalidade(regiao_selecionada):
    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)
    
    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql="SELECT DISTINCT LOCAL_ESTACAO_CLIMATICA FROM DADOS_CLIMATICOS WHERE REGIAO_ESTACAO_CLIMATICA='" + regiao_selecionada + "'"
            
            # Carregar o resultado da consulta de Região no Dataframe
            listar_localidades=pd.DataFrame(cursor.execute(sql), columns=['local'])

    # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    return listar_localidades

#------------------------------------------------------------------------------------------------

# Função para fitrar as datas de acordo com o ciclo de cultura (Localidade e Ano cadastrados)
def filtrarAno(localidade_selecionada):

    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql="SELECT DISTINCT TO_CHAR(DATA_MEDICAO, 'YYYY') FROM DADOS_CLIMATICOS WHERE LOCAL_ESTACAO_CLIMATICA='" + localidade_selecionada + \
                 "' AND PERIODO_MEDICAO='safra'"
                     
            # Carregar o resultado da consulta no Dataframe
            listar_ano=pd.DataFrame(cursor.execute(sql), columns=['anoSelecionados']).sort_values(by='anoSelecionados', ascending=False)
                        
        # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    return listar_ano

#------------------------------------------------------------------------------------------------

# Função para fitrar as datas de acordo com o ciclo de cultura (Localidade e Ano cadastrados)
def filtrarDatas(ano_selecionado, regiao_selecionada, localidade_selecionada):

    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    ### Completar com as outras Regiões após o cadastro no Banco de Dados ###

    # Seleciona a Região para definição dos Meses Correspondentes
    #   às definições de Datas de Acordo com o Calendário da Região Centro-Oeste
    # Selecionar o Ciclo de Cultura  
    #   Calendário 3: Inicia em 01 de setembro + 120 dias (Ciclo-3:Set-Dez)
    #   Calendário 2: Inicia em ?? de ?? + 120 dias (Ciclo-2:Set-Dez)
    #   Calendário 1: Inicia em ?? de ?? + 120 dias (Ciclo-1:Set-Dez)
    if regiao_selecionada =='Região Centro-Oeste':
        data_inicial="'01/09/" + str(ano_selecionado) + "'"
        data_final="'31/12/" + str(ano_selecionado) + "'"    

    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql="SELECT DATA_MEDICAO FROM DADOS_CLIMATICOS WHERE DATA_MEDICAO BETWEEN TO_DATE("+data_inicial+ ",'DD/MM/YYYY') \
                AND TO_DATE("+data_final+ ",'DD/MM/YYYY') AND STATUS ='Ativo' AND LOCAL_ESTACAO_CLIMATICA='" + localidade_selecionada + "' ORDER BY DATA_MEDICAO"
                        
            # Carregar o resultado da consulta no Dataframe
            listar_datas=pd.DataFrame(cursor.execute(sql), columns=['datasSelecionadas'])
            # Formatar as datas de acordo com o padrão utilizado
            listar_datas['datasSelecionadas'] = listar_datas['datasSelecionadas'].dt.strftime('%d/%m/%Y')
            
        # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    return listar_datas

#------------------------------------------------------------------------------------------------

# Função para os componentes de filtro para entrada de dados - Dashboard
def definirFiltrosEntrada():
    # Definição do Ciclo de Cultura
    listar_ciclo_cultura=['Ciclo-2:Set-Dez','Ciclo-1:Jan-Abr']

    # Logo Resumido
    st.sidebar.image('logo_resumo_V1.png', width=170,)

    # Filtro por Região
    # Chamada de Função para Filtro das Regiões dos Dados Climáticos Cadastrados
    listar_regiao=filtrarRegiao()

    #********************************************************
    # Escolha da Opção de "Região" pelo usuário na Dashboard
    #********************************************************
    regiao_selecionada=st.sidebar.selectbox('Selecione a Região:', (listar_regiao))

    # Filtro por Localidade
    # Chamada de Função para Filtro das Localidades dos Dados Climáticos
    listar_localidade=filtrarLocalidade(regiao_selecionada)

    #************************************************************
    # Escolha da Opção de "Localidade" pelo usuário na Dashboard
    #************************************************************
    localidade_selecionada=st.sidebar.selectbox('Selecione a Localidade:', (listar_localidade))

    # Filtro por Ano
    # Chamada de Função para fitrar as datas de acordo com o ciclo de cultura (Localidade e Ano cadastrados)
    listar_ano=filtrarAno(localidade_selecionada)

    #*****************************************************
    # Escolha da Opção de "Ano" pelo usuário na Dashboard
    #*****************************************************
    ano_selecionado = st.sidebar.selectbox('Selecione o Ano:', (listar_ano))

    #*****************************************************
    # Escolha da Opção de "Ciclo de Cultura" pelo usuário na Dashboard
    #*****************************************************
    ciclo_cultura = st.sidebar.selectbox('Selecione o Ciclo de Cultura:', (listar_ciclo_cultura))

    # Escolha do Ciclo de Cultura restrita para os dados "Deste estudo de Caso"
    if ciclo_cultura =='Ciclo-1:Jan-Abr':
        ciclo_cultura='Ciclo-2:Set-Dez'
        st.sidebar.error('Não há dados cadastrados para Ciclo-1:Jan-Abr', icon="🚨")
        

    # Filtro por Data
    # Chamada de Função para fitrar as datas de acordo com o ciclo de cultura (Localidade e Ano cadastrados)
    listar_datas=filtrarDatas(ano_selecionado, regiao_selecionada, localidade_selecionada)
    
    #******************************************************
    # Escolha da Opção de "Data" pelo usuário na Dashboard
    #******************************************************
    data_selecionada=st.sidebar.selectbox('Selecione a Data:', (listar_datas))

    botao=st.sidebar.button("Processar Método")

    return data_selecionada, botao

#------------------------------------------------------------------------------------------------

# Função para consulta de Dados Climáticos (Janela de Tempo) no Banco ORACLE 
def consultarDadosClimaticos(connection, DataInicial, DataFinal):
    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql="SELECT * FROM dados_climaticos WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial + \
                ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')" + "ORDER BY DATA_MEDICAO"

                ### SQL do Banco Oracle
                    #SELECT * FROM "ADMIN"."dados_climaticos"
                    #WHERE DATA_MEDICAO BETWEEN TO_DATE('01/01/2000', 'DD/MM/YYYY')
                    #AND TO_DATE('11/02/2000', 'DD/MM/YYYY')

            # Carregar o resultado da consulta no DataFrame
            df_consulta_bd=pd.DataFrame(cursor.execute(sql), columns=['idDadosClimaticos','idProjetos',\
                'localEstacaoClimatica','periodoMedicao','dataMedicao','precipitacao', 'temperaturaMaxima',\
                'temperaturaMinima','umidadeRelativa','pontoOrvalho','temperaturaMedCompensada','regiaoEstacaoClimatica','status'])
            print(df_consulta_bd)

            # Contagem de linhas dataframe
            linhas_df_consulta_bd=df_consulta_bd.shape[0]

            # Verificação se o resultado da consulta ao Banco de Dados Oracle não retorna vazia
            if df_consulta_bd.empty:
                print("Consulta no período:", DataInicial, "e:", DataFinal, "não retornaram dados. Inserir outra data para processamento!!")
                raise SystemExit

            # Verificação se o resultado da consulta ao Banco de Dados Oracle retorna, no mínimo, 4 linhas (dias) de dadaos climáticos.
            #   => 4 dias são dados mínimos para o processamento dos dados na etapa de "Interpolação de Dados -> Cálculo da Spline Cúbica"
            if linhas_df_consulta_bd <4:
                print("Consulta no período:", DataInicial, "e:", DataFinal, "retornam somente " + str(linhas_df_consulta_bd) +\
                    " linhas. Dados insuficientes. \nInserir outra data para processamento!!")
                raise SystemExit

    # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            print(sql)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    return df_consulta_bd

#------------------------------------------------------------------------------------------------

# Função para gerar a lista de dados interpolados, de acordo com as Variáveis climáticas
def preparaDadosInterpolacao(df_consulta_bd):

    lista_interpolacao=[]
    # Eixo "Y" para Interpolação: Dados da coluna "Precipitação"
    # Coluna precipitacao com valores absolutos
    coluna_precipitacao=[abs(ele) for ele in df_consulta_bd['precipitacao']]
    lista_interpolacao.append(coluna_precipitacao)
    
    # Eixo "Y" para Interpolação: Dados da coluna "Temperatura Máxima"
    # Coluna temperaturaMaxima com valores absolutos
    coluna_temperatura_maxima=[abs(ele) for ele in df_consulta_bd['temperaturaMaxima']]
    lista_interpolacao.append(coluna_temperatura_maxima)

    # Eixo "Y" para Interpolação: Dados da coluna "Temperatura Mínima"
    # Coluna temperaturaMinima com valores absolutos
    coluna_temperatura_minima=[abs(ele) for ele in df_consulta_bd['temperaturaMinima']]
    lista_interpolacao.append(coluna_temperatura_minima)

    # Eixo "Y" para Interpolação: Dados da coluna "Umidade Relativa"
    # Coluna umidadeRelativa com valores absolutos
    coluna_umidade_relativa=[abs(ele) for ele in df_consulta_bd['umidadeRelativa']]
    lista_interpolacao.append(coluna_umidade_relativa)

    # Eixo "Y" para Interpolação: Dados da coluna "Ponto de Orvalho"
    # Coluna pontoOrvalho com valores absolutos
    coluna_ponto_orvalho=[abs(ele) for ele in df_consulta_bd['pontoOrvalho']]
    lista_interpolacao.append(coluna_ponto_orvalho)

    # Eixo "Y" para Interpolação: Dados da coluna "Temperatura Média Compensada"
    # Coluna temperaturaMedCompensada com valores absolutos
    coluna_temperatura_med_compensada=[abs(ele) for ele in df_consulta_bd['temperaturaMedCompensada']]
    lista_interpolacao.append(coluna_temperatura_med_compensada)

    # Eixo "X" para Interpolação
    # Pegar a quantidade de linhas da consulta do Dataframe para definir a quantidade igual aos dados de "Y"
    X=list(range(1,df_consulta_bd['precipitacao'].shape[0]+1))

    # Gerar os Labels para o Gráfico de Interpolação (Eixo X)
    labels=[]
    for i in range(1,len(X)+1):
        labels.append("Ponto " + str(i))  
   
    return X, lista_interpolacao, labels

# --------------------------------------------------------------------------------------

# Função para Calcular o Ajuste da Curva - Polinômios (FIT)
def calcularAjusteCurva(x,y,labels,descricao,tab, flag):
    # Dados de Entrada
    x = np.array(x)
    y = np.array(y)
    
    # Ajuste da curva a um polinômio
    p1 = np.polyfit(x,y,1)
    p2 = np.polyfit(x,y,2)
    p3 = np.polyfit(x,y,3)
    p4 = np.polyfit(x,y,4)
    p5 = np.polyfit(x,y,5)

    # Rotina para determinação do valor de R da equação da reta
    slope,intercept,r_value,p_value,std_err = stats.linregress(x,y)

    # Cálculo dos coeficientes de determinação dos polinômios de ordem 2 à 5

    # Cálculo do (R-Quadrado)
    #    Soma dos Quadrados dos Resíduos (SQresid): variação de Y que não é explicada pelo modelo elaborado. 
    #     => É o somatório das diferenças entre o valor predito e o valor real elevados ao quadrado.

    #    Soma dos Quadrados de Regressão (SQtotal): oferece a variação de Y considerando as variáveis X utilizadas no modelo.
    #     
    #    => Então, o R-quadrado é calculado dividindo (SQresid) pelo (SQtotal), sendo o resultado subtraído de 1.   
    #   --------------------------------------

    yfit2 = p2[0] * pow(x,2) + p2[1] * x + p2[2]
    yresid2 = y - yfit2
    SQresid = sum(pow(yresid2,2))
    SQtotal = len(y) * np.var(y)
    R2_2 = 0
    R2_2 = 1 - SQresid/SQtotal

    yfit3 = p3[0] * pow(x,3) + p3[1] * pow(x,2) + p3[2] * x + p3[3]
    yresid3 = y - yfit3
    SQresid = sum(pow(yresid3,2))
    SQtotal = len(y) * np.var(y)
    R2_3 = 0
    R2_3 = 1 - SQresid/SQtotal    

    yfit4 = p4[0] * pow(x,4) + p4[1] * pow(x,3) + p4[2] * pow(x,2) + p4[3] * x + p4[4]
    yresid4 = y - yfit4 
    SQresid = sum(pow(yresid4,2))
    SQtotal = len(y) * np.var(y) 
    R2_4 = 0
    R2_4 = 1 - SQresid/SQtotal
   
    yfit5 = p5[0] * pow(x,5) + p5[1] * pow(x,4) + p5[2] * pow(x,3) + p5[3] * pow(x,2) + p5[4] * x + p5[5]
    yresid5 = y - yfit5
    SQresid = sum(pow(yresid5,2))
    SQtotal = len(y) * np.var(y)
    R2_5 = 0
    R2_5 = 1 - SQresid/SQtotal       

    # Impressão dos Resultados
    status_descricao=""
    
    if flag==0:
        status_descricao = "Dados Sem Interpolação:"
    else:
        status_descricao = "Dados Com Interpolação:"

    print("\n" + status_descricao + "\n")
    print('Equação da reta: ' + str(descricao) )
    print('Coeficientes',p1,'R2 =',pow(r_value,2))
    print('Polinômio de ordem 2: ' + str(descricao))
    print('Coeficientes',p2,'R2 =',R2_2)
    print('Polinômio de ordem 3: ' + str(descricao))
    print('Coeficientes',p3,'R2 =',R2_3)
    print('Polinômio de ordem 4: ' + str(descricao))
    print('Coeficientes',p4,'R2 =',R2_4)
    print('Polinômio de ordem 5: ' + str(descricao))
    print('Coeficientes',p5,'R2 =',R2_5)

    # Interpolação
    new_length = 50
    new_x = np.linspace(x.min(), x.max(), new_length)
    temp= interpolate.splrep(x, y, k=3)
    new_y = interpolate.splev(new_x, temp, der=0)
    new_p2=interpolate.interp1d(x,np.polyval(p2,x), kind='linear')(new_x)
    new_p3=interpolate.interp1d(x,np.polyval(p3,x), kind='linear')(new_x)
    new_p4=interpolate.interp1d(x,np.polyval(p4,x), kind='linear')(new_x)
    new_p5=interpolate.interp1d(x,np.polyval(p5,x), kind='linear')(new_x)

    # Ajustar y para ter o mesmo comprimento que new_y
    y_adjusted = interpolate.interp1d(x, y, kind='linear')(new_x)

    # Calcular o R quadrado da Spline Cúbica

    SQresid = sum(pow(y_adjusted - new_y, 2))
    SQtotal = sum(pow(y_adjusted - np.mean(y_adjusted), 2))
    R2_Spline = 1 - SQresid/SQtotal

    if flag==1: # Não imprimir o valor se "Sem interpolação"
        print('R2 (B-Spline) ' + descricao + " =", R2_Spline)
    
    print('\n------------------------------------------\n')
    
    # Plotagem dos gráficos - Interpolação com Spline Cúbica
    
    fig_0=plt.figure(figsize=(10,10))
    plt.plot(x,y,'o')
    plt.style.use('default')

    # Plot polinômios de grau 1 até 5
    plt.subplot(2,2,1)
    plt.plot(x,y,'go')
    plt.plot(x,np.polyval(p1,x), 'g', label = 'Reta')
    plt.plot(x,np.polyval(p2,x), 'b-.', label = 'Grau 2')
    plt.plot(x,np.polyval(p3,x), label = 'Grau 3',color ='r')
    plt.plot(x,np.polyval(p4,x), label = 'Grau 4',color ='k')
    plt.plot(x,np.polyval(p5,x), 'c', label = 'Grau 5')
    plt.title("Gráfico de Dados Sem Interpolação")
    plt.xlabel("Dados Janela Temporal: " +str(descricao))
    plt.ylabel("Valores")
    plt.xticks(x, labels, rotation='vertical')
    plt.legend()

    fig_1=plt.figure(figsize=(10,10))

    # Plot com Interpolação e Spline Cúbica
    plt.subplot(2,2,2)
    plt.plot(x,y,'go')
    plt.plot(new_x,new_p2, 'b', label = 'Grau 2')
    plt.plot(new_x,new_p3, 'r', label = 'Grau 3')
    plt.plot(new_x,new_p4, 'k:.', label = 'Grau 4')
    plt.plot(new_x,new_p5, 'c', label = 'Grau 5')
    plt.plot(new_x, new_y,'m--', label = 'Spline Cúbica')
    plt.title("Gráfico Dados Interpolados")
    plt.xlabel("Dados Janela Temporal: " + str(descricao))
    plt.ylabel("Valores")
    plt.xticks(x, labels, rotation='vertical')
    plt.legend()
    plt.show()

    #*********************************************
    # Plotar Gráfico de Interpolação na Dashboard
    #*********************************************

    # Verificar se o Gráfico a ser plotado é:
    #   "Sem intepolação - fig_0" ou
    #   "Com intepolação - fig_1"
    with tab:
        if flag ==0:
            dash_3_col_1_3.pyplot(fig_0)
        
        if flag ==1:
            dash_3_col_2_3.pyplot(fig_1)

    return new_x, new_y

#------------------------------------------------------------------------------------------------

# Função para Processamento de Interpolação
def processarInterpolacao(X,labels,lista_interpolacao,tab,flag):
    # Criar Dataframe para armazenar os resultados das interpolações
    df_interpolar=pd.DataFrame(columns=['Y'])
    
    # Descrição das Variáveis para uso nos gráficos
    descricao_variavel=['Precipitação','Temperatura Maxima','Temperatura Mínima','Umidade Relativa',\
        'Ponto Orvalho','Temperatura Med.Compensada']
    
    # Gerar lista chave/valor (valor de cada variável/descrição)
    lista_chave_valor=list(zip(descricao_variavel,lista_interpolacao))

    # Loop para processamento das interpolações e geração dos gráficos correspondentes por variável
    for chave,valor in lista_chave_valor:
        # Chamada de Função para Calcular o Ajuste da Curva - Polinômios (FIT)
        new_x, new_y = calcularAjusteCurva(X,valor,labels,chave,tab,flag)
        # Salvar dados de Interpolação calculado para cada variável
        df_interpolar=df_interpolar.append({'Y':new_y},ignore_index=True)
    
    df_interpolar=df_interpolar.round(casas_decimais)
    
    return df_interpolar, np.around(new_y,casas_decimais)

#------------------------------------------------------------------------------------------------

# Função para selecionar os dados interpolados para completar os dados faltantes "df_consulta_bd"
# -> DataFrame de dados Climáticos (De acordo com o intervalo definido)
def buscarValoresInterpolados(dados_interpolados, intervalo):
    dados_interpolados= list(dados_interpolados)
    vetor_dados=[]
    controle=0

    for pos in range(len(dados_interpolados)):
        if controle<pos:
            vetor_dados.append(dados_interpolados[controle])
            controle+=intervalo            
    return vetor_dados

#------------------------------------------------------------------------------------------------

# Função para processamento dos valores interpolados para completar (se necessário) o conjunto de dados com os dados faltantes
def processarCompletarDadosInterpolados(df_interpolar,df_consulta_bd,tab):

    consulta_bd_aux=[]

    #   -> Trocar o valor da coluna 'Status" para o valor "Original"
    #   -> "Original" significa que os valores NÃO são originados do "Processo de Interpolação"
    if not df_consulta_bd.empty:
        df_consulta_bd['status'] ='Original'

    # Chamada de Função para selecionar os dados interpolados para completar os dados faltantes "df_consulta_bd"
    # -> Alimentar o restante dos dados
    # -> Cada iteração alimenta uma variável ('precipitacao', 'temperaturaMaxima','temperaturaMinima','umidadeRelativa',
    #                                         'pontoOrvalho','temperaturaMedCompensada')  
    for contador in range(len(df_interpolar)):
        vetor_dados=buscarValoresInterpolados(np.hstack(df_interpolar.loc[contador].to_numpy()).round(casas_decimais), 5)
        # Loop no "vetor_dados" para atribuir "como absolutos" os valores interpolados (percorridos)
        consulta_bd_aux.append([abs (ele) for ele in vetor_dados])    
    # Montar o Dataframe Auxiliar com os dados interpolados
    df_consulta_bd_aux=pd.DataFrame(np.asarray(consulta_bd_aux).T, columns=['precipitacao', 'temperaturaMaxima','temperaturaMinima',\
            'umidadeRelativa','pontoOrvalho','temperaturaMedCompensada'])
    #print(df_consulta_bd_aux)
    
    # Contagem de linhas dataframe
    linhas_df_consulta_bd=df_consulta_bd.shape[0]

    # Contagem de linhas faltantes
    linhas_faltantes=(intervalo-linhas_df_consulta_bd)+1

    # Pegar a última linha do Dataframe auxiliar nas colunas de interesse
    lista_colunas=['idDadosClimaticos','idProjetos','localEstacaoClimatica','periodoMedicao','dataMedicao','regiaoEstacaoClimatica']
    ultima_linha_df= df_consulta_bd[0:linhas_df_consulta_bd].iloc[-1]
    vetor_linha_auxiliar=[]
    contador=0

    # Gerar o conjunto Auxiliar de dados Interpolados com as variáveis de interesse
    for colunas in lista_colunas:
        vetor_linha_auxiliar.append(ultima_linha_df[colunas])
        df_consulta_bd_aux.insert(contador,lista_colunas[contador],ultima_linha_df[colunas])
        contador+=1
               
    # Apagar as linhas "desnecessárias" do conjunto Auxiliar dados Interpolados com as variáveis de interesse
    df_consulta_bd_aux=df_consulta_bd_aux.drop(list(range(linhas_faltantes,len(df_consulta_bd_aux))))  
    print(df_consulta_bd_aux)

    # Completar o conjunto principal de dados com os dados faltantes (Interpolados)

    # Se o Conjunto Auxiliar for diferente de "vazio": 
    #   -> Significa que há dados interpolados à acrescentar no Conjunto Inicial, então:      
    #   -> Acrescentar a coluna 'Status" com o valor 'Interpolado'
    if not df_consulta_bd_aux.empty:
        df_consulta_bd_aux=df_consulta_bd_aux.assign(status ='Interpolado')    

    # Concatenar os Dataframes (inicial) e (dados auxiliares) para complementar os dados faltantes
    df_consulta_bd=pd.concat([df_consulta_bd,df_consulta_bd_aux],ignore_index=True)    
    print("Dados prontos para processamento:")
    print(df_consulta_bd)

    #=======================================================================
    # Chamada de Função para gerar a lista de dados interpolados, de acordo com as Variáveis climáticas
    X, lista_interpolacao, labels=preparaDadosInterpolacao(df_consulta_bd)

    #=======================================================================
    # Chamada de Função para Processamento de Interpolação
    df_interpolar,new_y=processarInterpolacao(X,labels,lista_interpolacao,tab3,1)
    #=======================================================================

    #****************************************************
    # Exibir o dataframe de dados completos no Dashboard
    #****************************************************
    with tab:
        dash_3_col_1_1.subheader("Dados Climáticos - Janela Temporal:")
        # Ajustar os nomes das colunas (Formatação para Visualização)
            # Copiar o Dataframe para outra variável para não alterar o Dataframe Original
            #   -> Continuar o restante do código com o "df_consulta_bd" original
            #   -> Usar "df_consulta_bd_view" somente para visualização na Interface
        df_consulta_bd_view=df_consulta_bd.copy()
        df_consulta_bd_view = df_consulta_bd_view.rename(columns={'idDadosClimaticos':'ID. Dados Clim.','idProjetos':'ID.Projeto',     \
            'localEstacaoClimatica':'Estação Climática','regiaoEstacaoClimatica':'Região','status':'Status',                           \
            'precipitacao': 'Precipitação','temperaturaMaxima':'Temp. Máxima','temperaturaMinima':'Temp. Mínima',                      \
            'umidadeRelativa':'Umidade Relativa','pontoOrvalho':'Ponto de Orvalho','temperaturaMedCompensada':'Temp. Média Compensada',\
            'dataMedicao':'Data Medição','periodoMedicao':'Período'})
                
        # Formatação para precisão da colunas "Float" e "Date"
        dash_3_col_1_1.dataframe(df_consulta_bd_view.style.format({'Precipitação':'{:.2f}',           \
            'Temp. Máxima':'{:.2f}','Temp. Mínima':'{:.2f}','Umidade Relativa':'{:.2f}',\
            'Ponto de Orvalho':'{:.2f}','Temp. Média Compensada':'{:.2f}',                         \
            'Data Medição':lambda t: t.strftime('%d/%m/%Y')}))        
        
    return df_consulta_bd

#------------------------------------------------------------------------------------------------

#Função Regra 01 -> (Período de Molhamento Foliar)
def regra01(df_consulta_bd,casas_decimais):
   # Se período de Molhamento Foliar (umidade relativa) maior ou igual a 90%
  regra_1= df_consulta_bd[(df_consulta_bd['umidadeRelativa']>=90)]
  if not regra_1.empty:
      flag_regra_1="Alta"
      medianaRegra_01=round(regra_1['umidadeRelativa'].median(),casas_decimais)
      # Mostrar o Resultado
      print("Mediana Regra 1:",medianaRegra_01)
      print("Período Molhamento Foliar(favorabilidade):", flag_regra_1)
      print(regra_1)

  # Se consulta (Regra Alta) retorna vazio - Verificar (Regra Média)
  if regra_1.empty:
      regra_1= df_consulta_bd[(df_consulta_bd['umidadeRelativa']>=80) & (df_consulta_bd['umidadeRelativa']<90)]
      if not regra_1.empty:
          flag_regra_1="Média"
          medianaRegra_01=round(regra_1['umidadeRelativa'].median(),casas_decimais)
          # Mostrar o Resultado
          print("Mediana Regra 1:",medianaRegra_01)
          print("Período Molhamento Foliar(favorabilidade):", flag_regra_1)
          print(regra_1)

      # Se consulta (Regra Média) retorna vazio - Verificar (Regra Baixa)
      if regra_1.empty:
          regra_1= df_consulta_bd[(df_consulta_bd['umidadeRelativa']<80) & (df_consulta_bd['umidadeRelativa']>0)]
          if not regra_1.empty:
            flag_regra_1="Baixa"
            medianaRegra_01=round(regra_1['umidadeRelativa'].median(),casas_decimais)
            # Mostrar o Resultado
            print("Mediana Regra 1:",medianaRegra_01)
            print("Período Molhamento Foliar (favorabilidade):", flag_regra_1)
            print(regra_1)

      ## Se consulta (Regra Baixa) retorna vazio      
      if regra_1.empty:
          medianaRegra_01=0
          flag_regra_1='Baixa'
          # Mostrar o Resultado
          print("Mediana Regra 1:", medianaRegra_01)
          print("Período Molhamento Foliar (favorabilidade):",flag_regra_1)
          print("Não há dados da REGRA_1 para serem visualizados!!")

  return medianaRegra_01, regra_1, flag_regra_1

#------------------------------------------------------------------------------------------------

#Função Regra 02 -> (Período Mínimo de Molhamento Foliar)
def regra02(df_consulta_bd,casas_decimais):
    #  Se precipitação for maior que 6h - equivale a 1/4 de 24h
    #              (Então: Se Precipitação maior ou igual a 25% - equivale a 1/4 de 100%)
    regra_2= df_consulta_bd[(df_consulta_bd['precipitacao']>=25)]
    if not regra_2.empty:
        medianaRegra_02=round(regra_2['precipitacao'].median(),casas_decimais)
        flag_regra_2="Alta"
        # Mostrar o Resultado
        print("Mediana Regra 2:", medianaRegra_02)
        print("Período Mínimo Molhamento Foliar:", flag_regra_2)
        print(regra_2)

    # Se consulta (Regra Alta) retorna vazio - Verificar (Regra Média)
    if regra_2.empty:
        regra_2= df_consulta_bd[(df_consulta_bd['precipitacao']<25) & (df_consulta_bd['precipitacao']>=20)]
        if not regra_2.empty:
            medianaRegra_02=round(regra_2['precipitacao'].median(),casas_decimais)
            flag_regra_2="Média"
            # Mostrar o Resultado
            print("Mediana Regra 2:", medianaRegra_02)
            print("Período Mínimo Molhamento Foliar:", flag_regra_2)
            print(regra_2)

    # Se consulta (Regra Média) retorna vazio - Verificar (Regra Baixa)
    if regra_2.empty:
        regra_2= df_consulta_bd[(df_consulta_bd['precipitacao']<20) & (df_consulta_bd['precipitacao']>0) ]
        if not regra_2.empty:
            medianaRegra_02=round(regra_2['precipitacao'].median(),casas_decimais)
            flag_regra_2="Baixa"
            # Mostrar o Resultado
            print("Mediana Regra 2:", medianaRegra_02)
            print("Período Mínimo Molhamento Foliar:", flag_regra_2)
            print(regra_2)

    # Se consulta (Regra Baixa) retorna vazio
    if regra_2.empty:
        medianaRegra_02=0
        flag_regra_2='Baixa'
        # Mostrar o Resultado
        print("Mediana Regra 2:", medianaRegra_02)
        print("Período Mínimo Molhamento Foliar:",flag_regra_2)
        print("Não há dados da REGRA_2 para serem visualizados!!")   

    return medianaRegra_02, regra_2, flag_regra_2

#------------------------------------------------------------------------------------------------

#Função Regra 03
def regra03(df_consulta_bd,casas_decimais):
    flag_df=1
    # Se a Faixa de Temperatura estiver entre 18 a 26.5°C
    regra_3= df_consulta_bd[(df_consulta_bd['temperaturaMinima']>=18) & (df_consulta_bd['temperaturaMaxima']<=26.5)]
    if not regra_3.empty:
        ## Tempertatura Inicial (Temperatura Mínima)
        medianaRegra_03_1=round(regra_3['temperaturaMinima'].median(),casas_decimais)
        ## Tempertatura Final (Temperatura Máxima)
        medianaRegra_03_2=round(regra_3['temperaturaMaxima'].median(),casas_decimais)
        flag_regra_3="Alta"
        # Mostrar o Resultado
        print("Mediana Regra 3 - Temperatura Inicial:",medianaRegra_03_1)
        print("Mediana Regra 3 - Temperatura Final:",medianaRegra_03_2)
        print("Faixa de Temperatura:", flag_regra_3)
        print(regra_3)
    
    # Se consulta (Regra Alta) retorna vazio - Verificar (Regra Média)
    if regra_3.empty:       
        regra_3= df_consulta_bd[(df_consulta_bd['temperaturaMinima']>=15.1) & (df_consulta_bd['temperaturaMaxima']<=17.9)]
        if not regra_3.empty:
            ## Tempertatura Inicial (Temperatura Mínima)
            medianaRegra_03_1=round(regra_3['temperaturaMinima'].median(),casas_decimais)
            ## Tempertatura Final (Temperatura Máxima)
            medianaRegra_03_2=round(regra_3['temperaturaMaxima'].median(),casas_decimais)
            flag_regra_3="Média"
            # Mostrar o Resultado
            print("Mediana Regra 3 - Temperatura Inicial:",medianaRegra_03_1)
            print("Mediana Regra 3 - Temperatura Final:",medianaRegra_03_2)
            print("Faixa de Temperatura:", flag_regra_3)
            print(regra_3)
    
    # Se consulta (Regra Média) retorna vazio - Verificar (Regra Baixa)
    if regra_3.empty:
        regra_3= df_consulta_bd[(df_consulta_bd['temperaturaMinima']>=0) & (df_consulta_bd['temperaturaMaxima']<=15)]   
        if not regra_3.empty:
            ## Tempertatura Inicial (Temperatura Mínima)
            medianaRegra_03_1=round(regra_3['temperaturaMinima'].median(),casas_decimais)
            ## Tempertatura Final (Temperatura Máxima)
            medianaRegra_03_2=round(regra_3['temperaturaMaxima'].median(),casas_decimais)
            flag_regra_3="Baixa"
            # Mostrar o Resultado
            print("Mediana Regra 3 - Temperatura Inicial:",medianaRegra_03_1)
            print("Mediana Regra 3 - Temperatura Final:",medianaRegra_03_2)
            print("Faixa de Temperatura:", flag_regra_3)
            print(regra_3)

    # Se consulta (Regra Baixa) retorna vazio
    if regra_3.empty:
        flag_df=0
        ## Temperatura Inicial (Temperatura Mínima)
        medianaRegra_03_1=0
        ## Temperatura Final (Temperatura Máxima)
        medianaRegra_03_2=0
        flag_regra_3="Baixa"
        regra_3=0
        # Mostrar o Resultado
        print("Mediana Regra 3 - Temperatura Inicial:",medianaRegra_03_1)
        print("Mediana Regra 3 - Temperatura Final:",medianaRegra_03_2)
        print("Faixa de Temperatura:",flag_regra_3)
        print("Não há dados da REGRA_3 para serem visualizados!!")        
        
    return medianaRegra_03_1, medianaRegra_03_2, regra_3, flag_regra_3, flag_df

#------------------------------------------------------------------------------------------------

#Função Regra 04
def regra04(df_consulta_bd,casas_decimais):
    # Maior Temperatura da Janela (Temperatura Máxima)
    regra_4_valor= df_consulta_bd['temperaturaMaxima'].max()
    # Flag para verificação da situação de Favorabilidade da variável "Temperatura Máxima"
    flag_regra_4=""

    # Compara se o valor da maior Temperatura Máxima dentro da faixa de favorabilidade (Baixa, Média ou Alta)
    if (regra_4_valor>=18) & (regra_4_valor<=26.5):
        flag_regra_4="Alta"
        regra_4=1

    elif ((regra_4_valor>=15.1) & (regra_4_valor<=17.9)) | ((regra_4_valor>26.5) & (regra_4_valor<=30)) :
        flag_regra_4="Média"
        regra_4=1
        
    elif ((regra_4_valor>0) & (regra_4_valor<=15)) | ((regra_4_valor>30) & (regra_4_valor<=42)):
        flag_regra_4="Baixa"
        regra_4=1

    # Temperatura de corte = 42 Graus (Erro de medição). 
    elif (regra_4_valor==0) | (regra_4_valor>42):
        flag_regra_4="Baixa"
        regra_4=0
                    
    # Mostrar o Resultado
    print("Temperatura Máxima da Janela (valor):",regra_4_valor)
    print("Valor de Favorabilidade (Regra 4):",flag_regra_4)
    print("Valor (Regra 4):",regra_4)

    return regra_4, regra_4_valor, flag_regra_4

#------------------------------------------------------------------------------------------------

#Função Regra 05
def regra05(df_consulta_bd,casas_decimais):
    # Menor Temperatura da Janela (Temperatura Mínima)
    regra_5_valor= df_consulta_bd['temperaturaMinima'].min()
    # Compara se o valor da maior Temperatura Mínima está dentro da faixa de favorabilidade
    if (regra_5_valor>=18) & (regra_5_valor<=26.5):
        flag_regra_5="Alta"
        regra_5=1

    elif ((regra_5_valor>=15.1) & (regra_5_valor<=17.9)) | ((regra_5_valor>26.5) & (regra_5_valor<=30)) :
        flag_regra_5="Média"
        regra_5=1
        
    elif ((regra_5_valor>=0) & (regra_5_valor<=15)) | (regra_5_valor>30):
        flag_regra_5="Baixa"
        regra_5=1
    
    elif (regra_5_valor<=-1):
        flag_regra_5="Baixa"
        regra_5=0
            
    # Mostrar o Resultado
    print("Temperatura Mínima da Janela (valor):",regra_5_valor)
    print("Valor de Favorabilidade (Regra 5):",flag_regra_5)
    print("Valor (Regra 5):",regra_5)

    return regra_5, regra_5_valor, flag_regra_5

#------------------------------------------------------------------------------------------------

# Função Regra 06
def regra06(df_consulta_bd,casas_decimais):
    # Calcular a diferença do Ponto de Orvalho e Temperatura Média Compensada 
    #   -> Se Temperatura Média Compensada for menor que (2 graus) que o Ponto de Orvalho
    regra_6=df_consulta_bd[(df_consulta_bd['temperaturaMedCompensada'] - (df_consulta_bd['pontoOrvalho'])) <=2]
    # Mostrar o Resultado
    if regra_6.empty:        
            ## Se o valor é vazio "NAN"
            # => quando o resultado da consulta (BD) retorna vazio
        medianaRegra_06=0
        flag_regra_6="Baixa"
        print("Mediana Regra 06:",medianaRegra_06)
        print("Valor de Favorabilidade (Regra 6):",flag_regra_6)
        print("Não há dados da REGRA_6 para serem visualizados!!")
    else:
        medianaRegra_06_PO=round(regra_6['pontoOrvalho'].median(),casas_decimais)
        medianaRegra_06_TEMP=round(regra_6['temperaturaMedCompensada'].median(),casas_decimais)
        # Diferença entre Temperatura e Ponto de Orvalho
        medianaRegra_06=abs(round(medianaRegra_06_PO - medianaRegra_06_TEMP, casas_decimais))
        flag_regra_6="Alta"
        print("Mediana Regra 06 - Ponto Orvalho:",medianaRegra_06_PO)
        print("Mediana Regra 06 - Temperatura Média Compensada:",medianaRegra_06_TEMP)
        print("Mediana Regra 06:",medianaRegra_06)
        print("Valor de Favorabilidade (Regra 6):",flag_regra_6)
        print(regra_6)

    return regra_6, medianaRegra_06, flag_regra_6

#------------------------------------------------------------------------------------------------

# Função Regra 07
def regra07(DataInicial,DataFinal):
    # Verificar se a imagem tem a doença (0-> Sem a doença e 1-> Com a presença da doença)
    # Dados do Cultivar /dados de classificação da imagem

    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql_1="SELECT RESULTADO                                        \
                 FROM CLASSIFICACOES                                       \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)    \
                                             FROM IMAGEM_CLIMA_FAVORAB     \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
                                    
            # Carregar o resultado da consulta no DataFrame
            resultado_classificacao=pd.DataFrame(cursor.execute(sql_1),columns=['Resultado'])

            # Consulta no Banco de Dados Oracle
            sql_2="SELECT ID_IMG_SEGMENTADAS                             \
                 FROM IMAGENS_SEGMENTADAS                                \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)  \
                                             FROM IMAGEM_CLIMA_FAVORAB   \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))\
                ORDER BY ID_IMG_SEGMENTADAS "
                                                       
            # Carregar o resultado da consulta no DataFrame
            df_consulta_img=pd.DataFrame(cursor.execute(sql_2), columns=['idDadosClimaticos'])

            #*********************************************
            # Consultas Classificação - Exibição Dashboard
            #*********************************************

            # Consulta Relatório Classificação (Banco de Dados Oracle)
            sql_3="SELECT RELATORIO_CLASSIFICACAO                         \
                 FROM CLASSIFICACOES                                      \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)   \
                                             FROM IMAGEM_CLIMA_FAVORAB    \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
            # Executar comando SQL
            cursor.execute(sql_3)
                                 
            # Recebe Dados tipo CLOB do Banco ORACLE
            for row in cursor:
                df_consulta_relat_classificacao=pd.DataFrame([[row[0].read()]], columns=['relatorioClassificacao'])

            # Consulta Matriz de Confusão (Banco de Dados Oracle)
            sql_4="SELECT MATRIZ_CONFUSAO                                 \
                 FROM CLASSIFICACOES                                      \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)   \
                                             FROM IMAGEM_CLIMA_FAVORAB    \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
            # Executar o código SQL
            cursor.execute(sql_4)

            # Recebe imagem BLOB do Banco ORACLE
            data_ref_1 = cursor.fetchall()
            image_ref_1 = data_ref_1[0][0].read()
                        
            # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
            image_ref_1 = np.asarray(Image.open(io.BytesIO(image_ref_1)))
            
            # Consulta Relatório Classificação (Banco de Dados Oracle)
            sql_5="SELECT CURVA_ROC                                       \
                 FROM CLASSIFICACOES                                      \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)   \
                                             FROM IMAGEM_CLIMA_FAVORAB    \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
            # Executar o código SQL
            cursor.execute(sql_5)

            # Recebe imagem BLOB do Banco ORACLE
            data_ref_2 = cursor.fetchall()
            image_ref_2 = data_ref_2[0][0].read()
                        
            # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
            image_ref_2 = np.asarray(Image.open(io.BytesIO(image_ref_2)))

            # Consulta no Banco de Dados Oracle (Instâncias duplicadas)
            sql_6="SELECT TUPLAS_BINARIAS_LIMPAS                           \
                 FROM CLASSIFICACOES                                       \
                 WHERE ID_BANCO_IMAGENS = (SELECT MIN(ID_BANCO_IMAGENS)    \
                                             FROM IMAGEM_CLIMA_FAVORAB     \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
            
            # Carregar o resultado da consulta no DataFrame
            df_instancias_duplicadas=pd.DataFrame(cursor.execute(sql_6),columns=['TUPLAS BINARIAS LIMPAS'])
            
            # Consulta no Banco de Dados Oracle (ID cadastro da relação imagem, dados climáticos e favorabilidade)
            #   => uso nas recomendações para indicar os dados de plantas_soja 
            sql_7="SELECT MIN(ID_DADOS_PLANTA_SOJA) FROM IMAGEM_CLIMA_FAVORAB WHERE ID_BANCO_IMAGENS =    \
                                            (SELECT MIN(ID_BANCO_IMAGENS) FROM IMAGEM_CLIMA_FAVORAB       \
                                             WHERE ID_DADOS_CLIMATICOS = (SELECT MIN(ID_DADOS_CLIMATICOS) \
                                                                          FROM DADOS_CLIMATICOS           \
                                                                          WHERE DATA_MEDICAO BETWEEN TO_DATE(" + DataInicial +          \
                                                                            ",'DD/MM/YYYY') and TO_DATE("+ DataFinal + ",'DD/MM/YYYY')))"
                                    
            # Carregar o resultado da consulta no DataFrame
            df_id_imagem_clima_favorab=pd.DataFrame(cursor.execute(sql_7),columns=['ID_IMAGEM_CLIMA_FAVORAB'])

    # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            print(sql_2)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    # Carregar a Imagem Segmentada de Referência no "subplot" (posição 1)
    fig_matriz_curva_classificacao = plt.figure(figsize = (25,25))
    plt.subplot(1, 5, 1)
    plt.axis('off')
    plt.imshow(image_ref_1)

    #------------------------------
    # Carregar a Imagem Canal Verde no "subplot" (posição 2)
    plt.subplot(1, 5, 2)
    plt.axis('off')
    plt.imshow(image_ref_2)

    if not resultado_classificacao.empty:
        regra_7=int(resultado_classificacao['Resultado'])

        if int(resultado_classificacao['Resultado'])==1:
            flag_regra_7="Alta"
        elif int(resultado_classificacao['Resultado'])==0:
            flag_regra_7="Baixa"
        
        # Mostrar o Resultado
        print("Valor de Favorabilidade (Regra 7):",int(resultado_classificacao['Resultado']))
        print("Valor de Favorabilidade (Flag):",flag_regra_7)

        print("\nImagens Segmentadas que participam da Classificação:")
        for ind in df_consulta_img.index:
            print("IMAGEM SEGMENTADA:",df_consulta_img['idDadosClimaticos'][ind])
        
        return regra_7, df_consulta_img, flag_regra_7, df_consulta_relat_classificacao, fig_matriz_curva_classificacao, df_instancias_duplicadas, df_id_imagem_clima_favorab

    else:
        print("Resultado da Classificação da Imagem retornou vazio. Verifique o Cadastro!!")
        return 0,0,0

#------------------------------------------------------------------------------------------------

# Função para Exibir Imagens Segmentadas participantes da Janela de Tempo
def exibirImagensParticipantes(df_consulta_img, tab):
    
    # Ordenar na sequência as imagens: em "Verde", "Amarela" e "Marrom"
    #   -> para a exibição no Matplotlib
    df_consulta_img= df_consulta_img.sort_values(['idDadosClimaticos'])
    lista_img_segment=[]
    lista_consulta_sementes=[]
    lista_consulta_estatistico=[]
    lista_consulta_qualidade=[]
    # Inicializar contagem subplot Figura Imagens Segmentadas: verde, amarela e marrom
    n=3

    # Inicialização de Dataframes
    #   =>Armazenamento de dados de características do Processamento "Imagens Segmentadas"
    df_consulta_caract= pd.DataFrame()
    df_consulta_sementes= pd.DataFrame()
    df_consulta_estatistico= pd.DataFrame()
    df_consulta_qualidade= pd.DataFrame()

    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    # A partir do objeto de conexão executar as consultas na base de dados ORACLE
    with connection.cursor() as cursor:        
        try:
            # Consulta no Banco de Dados Oracle
            sql_1="SELECT IMG_SEGMENT_REFERENCIA FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][0])
            cursor.execute(sql_1)

            # Recebe imagem BLOB do Banco ORACLE
            data_ref = cursor.fetchall()
            image_ref = data_ref[0][0].read()
                        
            # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
            image_ref = np.asarray(Image.open(io.BytesIO(image_ref)))

            #------------------------------
            # Consulta no Banco de Dados Oracle
            sql_2="SELECT IMG_CANAL_VERDE FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][0])
            cursor.execute(sql_2)

            # Recebe imagem BLOB do Banco ORACLE
            data_ref_2 = cursor.fetchall()
            image_ref_2 = data_ref_2[0][0].read()
                        
            # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
            image_ref_2 = np.asarray(Image.open(io.BytesIO(image_ref_2)))
            
        # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

        # Carregar a Imagem Segmentada de Referência no "subplot" (posição 1)
        fig1 = plt.figure(figsize = (25,25))
        plt.subplot(1, 5, 1)
        plt.imshow(image_ref)
        plt.title("Imagem Segmentada Referência", fontsize=10)

        #------------------------------
        # Carregar a Imagem Canal Verde no "subplot" (posição 2)
        plt.subplot(1, 5, 2)
        plt.imshow(image_ref_2)
        plt.title("Imagem Canal Verde", fontsize=10)
                
        # Loop para carregar as imagens segmentadas (Classes: Verde, Amarela e Marrom)
        for ind in df_consulta_img.index:                                
                try:
                    sql_3="SELECT IMG_ROTULO_ESCOLHIDO FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                    cursor.execute(sql_3)

                    # Recebe imagem BLOB do Banco ORACLE
                    data = cursor.fetchall()
                    image = data[0][0].read()
                                
                    # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
                    image = np.asarray(Image.open(io.BytesIO(image)))

                    # Consulta no Banco de Dados Oracle
                    sql_4="SELECT CLASSE_COR FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                    cor = cursor.execute(sql_4).fetchall()
                    
                    # Carregar as Imagens Segmentadas no "subplot" (posições 3,4 e 5)                         
                    plt.subplot(1, 5, n)
                    plt.imshow(image)
                    plt.title("Imagem Segmentada:" + str(df_consulta_img['idDadosClimaticos'][ind]) + \
                        " - (Cor):"+ str(cor).strip("[(',)]"), fontsize=10)
                    
                    #-----------------------------------
                    # Gerar dados de Características (1) da Imagem Segmentada para exibição em Dados no Dataframe 
                    #   =>passar como retorno - Exibir na Aba "Processamento de Imagens"

                    # Consulta no Banco de Dados Oracle
                    sql_5="SELECT COORDENADAS_SEMENTE_CENTRAL, COORDENADAS_CALC_JANELA, TOTAL_PIXELS_JANELA, LIMIAR_1_SEGMENTACAO,\
                        LIMIAR_2_SEGMENTACAO, FAIXA_LIMIARES FROM SEGMENTACAO WHERE ID_IMG_SEGMENTADAS =" +  \
                        str(df_consulta_img['idDadosClimaticos'][ind])

                    # Carregar dados "SQL_5" e índices das Imagens Segmentadas correspondentes
                    df_consulta_caract=df_consulta_caract.append(cursor.execute(sql_5).fetchall())
                    lista_img_segment.append(str("Imagem Segment.:"+ str(df_consulta_img['idDadosClimaticos'][ind])))

                    #-----------------------------------
                    # Gerar dados de Características (2) da Imagem Segmentada para exibição em Dados no Dataframe 
                    #   =>passar como retorno - Exibir na Aba "Processamento de Imagens"

                    # Consulta no Banco de Dados Oracle
                    sql_6="SELECT A.DESCRICAO_COR_SEMENTE, A.COR_RGB_SEMENTE, A.DADOS_SEMENTES,\
                          B.TOTAL_SEMENTES_CALCULADAS FROM SEMENTES A, SEGMENTACAO B WHERE A.ID_SEMENTES = B.ID_SEMENTES AND ID_IMG_SEGMENTADAS =" +\
                          str(df_consulta_img['idDadosClimaticos'][ind])
                        
                    # Carregar dados "SQL_6" e índices das Imagens Segmentadas correspondentes
                    df_consulta_sementes=df_consulta_sementes.append(cursor.execute(sql_6).fetchall())
                    lista_consulta_sementes.append(str("Imagem Segment.:"+ str(df_consulta_img['idDadosClimaticos'][ind])))

                    #-----------------------------------
                    # Gerar dados de Características (3) da Imagem Segmentada para exibição em Dados no Dataframe 
                    #   =>passar como retorno - Exibir na Aba "Processamento de Imagens"

                    # Consulta no Banco de Dados Oracle
                    sql_7="SELECT ERRO_ESTATISTICO_CALCULADO, OPERACAO_PROJETO, DESVIO_PADRAO_PROJETO, VARIANCIA_SEGMENTACAO\
                          FROM SEGMENTACAO\
                          WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                        
                    # Carregar dados "SQL_7" e índices das Imagens Segmentadas correspondentes
                    df_consulta_estatistico=df_consulta_estatistico.append(cursor.execute(sql_7).fetchall())    
                    lista_consulta_estatistico.append(str("Imagem Segment.:"+ str(df_consulta_img['idDadosClimaticos'][ind])))

                    #-----------------------------------
                    # Gerar dados de Qualidade (1) da Imagem Segmentada para exibição em Dados no Dataframe 
                    #   =>passar como retorno - Exibir na Aba "Qualidade de Dados"

                    # Consulta no Banco de Dados Oracle
                    sql_8="SELECT MSE, PSNR, SSIM, OUTLIERS_BOXPLOT_SEMENTES, OUTLIERS_BOXPLOT_SEMENTES_CALCULO FROM IMAGENS_SEGMENTADAS\
                          WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                        
                    # Carregar dados "SQL_8" e índices das Imagens Segmentadas correspondentes
                    df_consulta_qualidade=df_consulta_qualidade.append(cursor.execute(sql_8).fetchall())     
                    lista_consulta_qualidade.append(str("Imagem Segment.:"+ str(df_consulta_img['idDadosClimaticos'][ind])))

                    # Incrementar posição de carga de Imagens Segmentadas para montar o "subplot"
                    n+=1
                                        
                # Exceção
                except cx_Oracle.Error as e:
                    error, = e.args
                    print(error.message)                    
                    if (error.offset):
                        print('^'.rjust(error.offset+1, ' '))

        # Carga de Imagens Segmentadas para montar o "subplot" Figura Boxplot
        n=1

        # Figura Boxplot - Configurações do Plot
        fig_boxplot= plt.figure(figsize = (25,25))
    
        try:
            # Loop para carregar os gráficos BoxPlot (Classes: Verde, Amarela e Marrom)
            for ind in df_consulta_img.index:
                # Consulta no Banco de Dados Oracle
                sql_10="SELECT CLASSE_COR FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                cor = cursor.execute(sql_10).fetchall()

                # Consulta no Banco de Dados Oracle
                sql_11="SELECT BOXPLOT_SEMENTES FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                cursor.execute(sql_11)

                # Recebe imagem BLOB do Banco ORACLE
                data = cursor.fetchall()
                image1 = data[0][0].read()
                            
                # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
                image1 = np.asarray(Image.open(io.BytesIO(image1)))
                
                # Carregar as Imagens Segmentadas no "subplot" (posições dinâmicas)                         
                plt.subplot(3, 2, n)
                plt.axis('off')
                plt.imshow(image1)
                plt.title("Sementes Sem Processamento - Cor: "+ str(cor).strip("[(',)]") + \
                            ' (Img.Segmentada:'+ str(df_consulta_img['idDadosClimaticos'][ind]) + ')', fontsize=13)
                
                # Incrementar posição de carga de Imagens Segmentadas para montar o "subplot" Figura Boxplot
                n+=1

                # Consulta no Banco de Dados Oracle
                sql_12="SELECT BOXPLOT_SEMENTES_CALCULO FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                cursor.execute(sql_12)

                # Recebe imagem BLOB do Banco ORACLE
                data = cursor.fetchall()
                image2 = data[0][0].read()
                            
                # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
                image2 = np.asarray(Image.open(io.BytesIO(image2)))

                # Carregar as Imagens Segmentadas no "subplot" (posições dinâmicas)                         
                plt.subplot(3, 2, n)
                plt.axis('off')
                plt.imshow(image2)
                plt.title("Sementes Com Processamento - Cor: "+ str(cor).strip("[(',)]") + \
                            ' (Img.Segmentada:'+ str(df_consulta_img['idDadosClimaticos'][ind]) + ')', fontsize=13)

                # Incrementar posição de carga de Imagens Segmentadas para montar o "subplot"
                n+=1
                                    
        # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))
                
        #**********************************************
        # Exibição das Imagens Segmentadas em Dashboard
        #**********************************************
        with tab: # Aba "Dashboard"
            dash_col_1_2.latex(r'''
            \textcolor{blue}{\textbf{Imagens Segmentadas:}}
            ''')                    
            dash_col_1_2.pyplot(fig1)

    connection.close()

    return df_consulta_caract, fig1, lista_img_segment, df_consulta_sementes, lista_consulta_sementes,\
        df_consulta_estatistico, lista_consulta_estatistico, df_consulta_qualidade, lista_consulta_qualidade, fig_boxplot
    
#------------------------------------------------------------------------------------------------

#Função para Exibir Histogramas
def exibirHistogramas(df_consulta_img):
    # Inicializar contador para subplot
    n=1
    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)
    
    # Configurações do Plot
    fig_histograma = plt.figure(figsize = (25,25))
    
    with connection.cursor() as cursor: 
        for ind in df_consulta_img.index:
            try:

                # Consulta no Banco de Dados Oracle
                sql_1="SELECT CLASSE_COR FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                cor = cursor.execute(sql_1).fetchall()

                #-----------------------------------
                # Gerar dados de Qualidade (2) Histograma de Comparação das Imagens 
                #   =>passar como retorno - Exibir na Aba "Qualidade de Dados"

                # Consulta no Banco de Dados Oracle
                sql_2="SELECT HISTOGRAMA FROM IMAGENS_SEGMENTADAS WHERE ID_IMG_SEGMENTADAS =" + str(df_consulta_img['idDadosClimaticos'][ind])
                cursor.execute(sql_2)

                # Recebe imagem BLOB do Banco ORACLE
                data = cursor.fetchall()
                image_histograma = data[0][0].read()
                            
                # Converte BLOB em bytes e array para plotar a imagem (Matplotlib)
                image_histograma = np.asarray(Image.open(io.BytesIO(image_histograma)))

                # Carregar as Imagens Segmentadas no "subplot"                       
                plt.subplot(1, 3, n)
                plt.imshow(image_histograma)
                plt.axis('off')
                plt.title("Imagem Segmentada:" + str(df_consulta_img['idDadosClimaticos'][ind]) + \
                    " - (Cor):"+ str(cor).strip("[(',)]"), fontsize=10)
                
                # Incremento do contador subplot
                n+=1

            # Exceção
            except cx_Oracle.Error as e:
                error, = e.args
                print(error.message) 
                if (error.offset):
                    print('^'.rjust(error.offset+1, ' '))
             
    connection.close()
    return fig_histograma

#------------------------------------------------------------------------------------------------

# Função para Contagem de Ocorrências por Regras
def contagemOcorrencias(df_consulta_bd,regra_1,regra_2,regra_3,regra_4,regra_5,regra_6,regra_7, \
      medianaRegra_01,medianaRegra_02,regra_4_valor,regra_5_valor,medianaRegra_06, casas_decimais,\
      flag_df,medianaRegra_03_1, medianaRegra_03_2):

   totalJanela=len(df_consulta_bd.index)
   print("Total de Dados (leituras diárias) da Janela-> "+ str(totalJanela))
   ocorrenciasRegra_1= len(regra_1.index)
   print("Ocorrências Regra 1-> "+ str(ocorrenciasRegra_1))
   ocorrenciasRegra_2= len(regra_2.index)
   print("Ocorrências Regra 2-> "+ str(ocorrenciasRegra_2))
   
   # Se Regra 3 retornar "0" ler o valor normalmente
   #  -> Se Diferente de "0" ler a quantidade de linhas do Dataframe Pandas
   if flag_df==0:
      ocorrenciasRegra_3=regra_3
   else:
      ocorrenciasRegra_3= len(regra_3.index)
   
   print("Ocorrências Regra 3-> "+ str(ocorrenciasRegra_3))
   ocorrenciasRegra_4= regra_4
   print("Ocorrências Regra 4-> "+ str(ocorrenciasRegra_4))
   ocorrenciasRegra_5= regra_5
   print("Ocorrências Regra 5-> "+ str(ocorrenciasRegra_5))
   ocorrenciasRegra_6= len(regra_6.index)
   print("Ocorrências Regra 6-> "+ str(ocorrenciasRegra_6))
   ocorrenciasRegra_7= regra_7
   print("Ocorrências Regra 7-> "+ str(ocorrenciasRegra_7))

   # Vetor de Valores das Regras (Valores de Referência)      
   dados_regras=np.array([medianaRegra_01,medianaRegra_02,medianaRegra_03_1, medianaRegra_03_2,regra_4_valor,regra_5_valor,medianaRegra_06, regra_7])

   return dados_regras, totalJanela, ocorrenciasRegra_1, ocorrenciasRegra_2, ocorrenciasRegra_3, ocorrenciasRegra_4,\
      ocorrenciasRegra_5, ocorrenciasRegra_6, ocorrenciasRegra_7

#------------------------------------------------------------------------------------------------

# Função para Plotar gráfico de ocorrências
def plotarOcorrencias(ocorrenciasRegra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,ocorrenciasRegra_4,ocorrenciasRegra_5,\
   ocorrenciasRegra_6,ocorrenciasRegra_7, tab):
   x=[1,2,3,4,5,6,7]
   y=[ocorrenciasRegra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,ocorrenciasRegra_4,ocorrenciasRegra_5,ocorrenciasRegra_6,
      ocorrenciasRegra_7]
   labels = ['Per.Molham.Foliar','Per.Min.Molham.Foliar','Faixa Temperatura','Temperatura Máxima','Temperatura Mínima',\
    'Ponto de Orvalho','Dados de Imagem']
   fig = plt.figure(figsize = (5,5))
   plt.plot(x,y,'k--')
   plt.plot(x,y,'go')
   plt.grid(True)
   plt.title("Ocorrências x Variáveis 'R'")
   #plt.xlabel("Variáveis da Base de Regras de Favorabilidade da FAS")
   plt.ylabel("Ocorrências")
   plt.xticks(x, labels, rotation='vertical')
   plt.show()
  
   #***********************************************
   # Exibir o gráfico de Ocorrências no Dashboard
   #***********************************************
   with tab:
    dash_col_2_1.latex(r'''
        \textcolor{blue}{\textbf{Gráfico de Variáveis - F.A.S.:}}
    ''')
    dash_col_2_1.pyplot(fig)

   return x,y

#------------------------------------------------------------------------------------------------

# Função para Calcular os erros: Abordagens: Figura Mérito e Lógica Fuzzy
def calcularErro(resultado):   
   vetor_resultado_erro=[]
   descricao=["Calculado:","+5% Erro:","-5% Erro:"]

   # Valor Calculado
   vetor_resultado_erro.append(round(resultado, casas_decimais))
   # Considerar +5% de erro
   vetor_resultado_erro.append(round(resultado + ((5*resultado)/100),casas_decimais))
   # Considerar -5% de erro
   vetor_resultado_erro.append(round(resultado - ((5*resultado)/100),casas_decimais))
   
   # Associa o resultado ao erro
   lista_resultado=list(zip(descricao,vetor_resultado_erro))

   return lista_resultado

#------------------------------------------------------------------------------------------------

# Função para Carregar a Tabela Verdade (Abordagem Markov)
def carregarTabelaVerdade():
    # Leitura dos dados da Tabela Verdade - Arquivo .CSV
    # Carga dos dados em um Dataframe Pandas
    path="Tabelas_Verdade_Probabilidades_7_VAR.csv"
    df_tab_verdade=pd.DataFrame()
    df_tab_verdade=pd.read_csv(path, sep=';')
    
    return df_tab_verdade

#------------------------------------------------------------------------------------------------

# Função para encontrar a Combinação da Tabela - Descobrir o Estado correspondente
# Dado o vetor de Ocorrências de Favorabilidade da FAS
def encontraCombinacao(ocorrenciasRegra_1,flag_regra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,ocorrenciasRegra_4,ocorrenciasRegra_5,ocorrenciasRegra_6,
                    ocorrenciasRegra_7,df_tab_verdade,tab):
    vetor_compara=[]
    vetor_ocorrencias=[ocorrenciasRegra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,ocorrenciasRegra_4,ocorrenciasRegra_5,ocorrenciasRegra_6,
                    ocorrenciasRegra_7]
    text=""
    text+="\nEntradas para o Modelo Cadeias Ocultas de Markov"
    text+="\nVetor de Ocorrências:" + str(vetor_ocorrencias)

    #**********************************************
    # Exibição do Vetor de Ocorrências - Dashboard
    #**********************************************
    with tab:
        dash_col_2_3.latex(r'''
        \textcolor{blue}{\textbf{Resultados do Processamento:}}
        ''')              
        dash_col_2_3.write("\nVetor de Ocorrências:" + str(vetor_ocorrencias))      

    for ocorrencia in vetor_ocorrencias:
        if ocorrencia>0:
            vetor_compara.append(1)        
        else:
            vetor_compara.append(0)

    # # Compara a flag de favorabilidade da variável V1 com o resultado
    # #   das ocorrências, apenas quando a flag for para "Baixa".
    # if flag_regra_1 =='Baixa':
    #     vetor_compara[0]=0

    text+="\nVetor de Comparação:" + str(vetor_compara)

    #*********************************************
    # Exibição do Vetor de Comparação - Dashboard
    #*********************************************
    #with tab:
        #dash_col_2_3.write("\nVetor de Comparação:" + str(vetor_compara))

    # Recupera na Tabela Verdade os dados iguais ao Vetor de Comparação
    vetor_resultado=df_tab_verdade[(df_tab_verdade['V1']==vetor_compara[0]) & (df_tab_verdade['V2']==vetor_compara[1]) &              \
        (df_tab_verdade['V3']==vetor_compara[2]) & (df_tab_verdade['V4']==vetor_compara[3]) &                                         \
        (df_tab_verdade['V5']==vetor_compara[4]) & (df_tab_verdade['V6']==vetor_compara[5]) & (df_tab_verdade['V7']==vetor_compara[6])]
    print(vetor_resultado)

    #*****************************************************
    # Exibir o Vetor Resultado em duas linhas - Dashboard
    #*****************************************************
    df_vetor_resultado_linhas=pd.DataFrame([
                                            [int(vetor_resultado.iloc[0,0]),vetor_resultado.iloc[0,1],vetor_resultado.iloc[0,2],vetor_resultado.iloc[0,3], \
                                                vetor_resultado.iloc[0,4],vetor_resultado.iloc[0,5],vetor_resultado.iloc[0,6]],                            \
                                            [vetor_resultado.iloc[0,8],vetor_resultado.iloc[0,9],vetor_resultado.iloc[0,10],vetor_resultado.iloc[0,11],    \
                                                vetor_resultado.iloc[0,12],vetor_resultado.iloc[0,13],vetor_resultado.iloc[0,14]]],
                                                columns=["R1", "R2", "R3", "R4", "R5", "R6", "R7"], index=['Combinação:','Porcentagem:'])
            
    #*********************************************
    # Exibição do Vetor de Resultados - Dashboard
    #*********************************************
    with tab:
        # Exibir Texto do Vetor de Resultados - Dashboard
        dash_col_2_3.text("Vetor de Resultado - Cadeias Ocultas Markov:")
        
        # Formatar os campos em duas casas decimais
        dash_col_2_3.dataframe(df_vetor_resultado_linhas.style.format({'R1':'{:.2f}','R2':'{:.2f}','R3':'{:.2f}','R4':'{:.2f}','R5':'{:.2f}',\
                                                             'R6':'{:.2f}','R7':'{:.2f}'}))              
                                 
    return vetor_resultado, vetor_compara, vetor_ocorrencias, text

#------------------------------------------------------------------------------------------------

# Função para capturar o índice do resultado do "vetor_resultado"
def capturarIndiceFavorab(vetor_resultado, text, df_consulta_bd):
        #  Origem da Tabela Verdade de Favorabilidade (Abordagem Markov)
    ID_TAB_VERD_FAVORAB=0
    ID_TAB_VERD_FAVORAB=vetor_resultado.index.values
    ID_TAB_VERD_FAVORAB[0]+=1
    text+="\n\nResultados Abordagem Cadeias Ocultas de Markov"
    text+="\n-------------------------------------------------"
    text+="\nÍndice Resultado Tabela Verdade:\n" + str(ID_TAB_VERD_FAVORAB[0])

    # Cria o Dataframe e organizar os dados para a tabela "IMAGEM_CLIMA_FAVORAB"
    df_img_cli_favorab = pd.DataFrame()
    df_img_cli_favorab.insert(0,"ID_DADOS_CLIMATICOS", df_consulta_bd["idDadosClimaticos"])
    df_img_cli_favorab.insert(1,"ID_TAB_VERD_FAVORAB", ID_TAB_VERD_FAVORAB[0])
    df_img_cli_favorab.insert(2,"ID_BANCO_IMAGENS", 1)
    print(df_img_cli_favorab)

    return df_img_cli_favorab,text

#------------------------------------------------------------------------------------------------

# Função para Normalização dos valores de probabilidades iniciais
def normalizaProbabilidadesIniciais():
    # Probabilidade baixa (0 - 33,3)
    # Probabilidade média (33,4 - 66,6)
    # Probabilidade alta (66,7 - 100)
    scala_Regras=MinMaxScaler(feature_range=(0,1))
    pbi=scala_Regras.fit_transform(np.array([0, 34.4, 66.7]).reshape(-1, 1))
    print(pbi)

    return pbi

#------------------------------------------------------------------------------------------------

# Função para identificar a probabilidade do Estado Atual
def probabilidadeEstadoAtual(text,vetor_resultado):
    # Inserir informações do Modelo 
    # Matriz de Probabilidade Inicial
    ##probab_inicial= [[0.1], [0.2], [0.7]]
    probab_inicial= [[0.33], [0.33], [0.33]]

    # Matriz de Transição de Estados
    matriz_transicao= [[0.4, 0.3, 1],
                      [0.6, 0.7, 0],
                      [0  , 0  , 0]]

    # Tratamento das Probabilidades - Combinações das Variáveis
    probab_estado=vetor_resultado[['P_V1','P_V2','P_V3','P_V4','P_V5','P_V6','P_V7']]
    text+=str(probab_estado)

    # Soma dos valores das Probabilidades (Soma = "1")
    probab_previsao=np.sum(probab_estado)

    return probab_estado, probab_previsao, matriz_transicao, probab_inicial, text

#------------------------------------------------------------------------------------------------

# Função para identificar o Estado do Atual da Favorabilidade FAS
def identificaEstadoAtual(vetor_resultado, probab_previsao, text, tab):
    # Atribui o valor da Matriz de Previsão
    # -> uso após o primeiro cálculo de previsão
    # -> monta a matriz de previsão com a soma dos valores
    #    das probabilidades origidas da combinação escolhida
    # Imprimir o resultado

    if np.array(vetor_resultado['S'])==1:
        resultado_markov= "Favorabilidade Baixa"
        text+="\nAbordagem Cadeias Ocultas de Markov - Estado Atual:" + str(resultado_markov) + "\n\n"

        #************************************
        # Exibição de Resultado no Dashboard
        #************************************
        with tab:
            st.subheader("Recomendações para Tomada de Decisão para Prognóstico")
            #st.caption("Legenda de Resultados: Favorabilidade Baixa - Cor Verde; Favorabilidade Média - Cor Azul; Favorabilidade Alta - Cor Vermelha")
            components.html(
                """
                <html>
                    <table style="font-size:20px" border="0">
                        <tr align="center" bgcolor="green">
                            <td>Favorabilidade Baixa</td>
                        </tr>                        
                    </table> 
                </html>
                """
                ,height=40)

        previsao_prox=[[probab_previsao.sum()], [0], [0]]
    elif np.array(vetor_resultado['S'])==2:
        resultado_markov= "Favorabilidade Média"
        text+="\nAbordagem Cadeias Ocultas de Markov - Estado Atual:" + str(resultado_markov) + "\n\n"

        #************************************
        # Exibição de Resultado no Dashboard
        #************************************
        with tab:
            st.subheader("Recomendações para Tomada de Decisão para Prognóstico:")
            #st.caption("Legenda de Resultados: Favorabilidade Média - Cor Verde; Favorabilidade Média - Cor Azul; Favorabilidade Alta - Cor Vermelha")
            components.html(
                  """
                <html>
                    <table style="font-size:20px" border="0">
                        <tr align="center" bgcolor="blue">
                            <td><span style="color:#FFFFFF">Favorabilidade Média</span></td>
                        </tr>                        
                    </table>
                </html>
                """
                ,height=40)

        previsao_prox=[ [0], [probab_previsao.sum()], [0]]
    elif np.array(vetor_resultado['S'])==3:
        resultado_markov= "Favorabilidade Alta"
        text+="\nAbordagem Cadeias Ocultas de Markov - Estado Atual:" + str(resultado_markov) + "\n\n"

        #************************************
        # Exibição de Resultado no Dashboard
        #************************************
        with tab:
            st.subheader("Recomendações para Tomada de Decisão para Prognóstico:")
            #st.caption("Legenda de Resultados: Favorabilidade Alta - Cor Verde; Favorabilidade Média - Cor Azul; Favorabilidade Alta - Cor Vermelha")
            components.html(
                """
                <html>
                    <table style="font-size:20px" border="0">
                        <tr align="center" bgcolor="red">
                            <td><span style="color:#FFFFFF">Favorabilidade Alta</span></td>
                        </tr>
                    </table>
                </html>
                """
                ,height=40)

        previsao_prox=[[0], [0], [probab_previsao.sum()]]

    return previsao_prox, resultado_markov, text

#------------------------------------------------------------------------------------------------

# Abordagem Modelo de Cadeias Ocultas de Markov
# Função para Exibição do Modelo Gráfico
def exibir_img_modelo(resultado_markov, tab):
    if resultado_markov == "Favorabilidade Baixa":
        img =cv2.cvtColor(cv2.imread('Automato_3_baixa.png'), cv2.COLOR_BGR2RGB)
        plt.figure(figsize=[10, 10])
        plt.imshow(img)
    if resultado_markov == "Favorabilidade Média":
        img =cv2.cvtColor(cv2.imread('Automato_3_media.png'), cv2.COLOR_BGR2RGB)
        plt.figure(figsize=[10, 10])
        plt.imshow(img)
    if resultado_markov == "Favorabilidade Alta":
        img =cv2.cvtColor(cv2.imread('Automato_3_alta.png'), cv2.COLOR_BGR2RGB)
        plt.figure(figsize=[10, 10])
        plt.imshow(img)

    #****************************************
    # Exibir a figura do Modelo no Dashboard
    #****************************************
    with tab:
        dash_col_2_2.latex(r'''
        \textcolor{blue}{\textbf{Resultado Cadeias Ocultas Markov:}}
        ''')
    dash_col_2_2.image(img)

#------------------------------------------------------------------------------------------------

# Função para calcular Próxima Previsão das Probabilidades 
# Uso da Probabilidade Inicial
def calcularPrevisoes(matriz_transicao, probab_inicial,previsao_prox):
    previsao_1=np.matmul(matriz_transicao, probab_inicial)
    print("Previsão 1:",previsao_1)

    # Previsão das Probabilidades - Uso da Probabilidade
    # -> Combinação da Tabela Verdade selecionada
    previsao_2=np.matmul(matriz_transicao, previsao_prox)
    print("Previsão 2:",previsao_2)
    finalizado=True

    return previsao_1, previsao_2, finalizado

#------------------------------------------------------------------------------------------------

# Script SQL para inserir dados na tabela "FAVORABILIDADES_FAS" no Banco Oracle (Cloud)
def gerarScriptSQLFavorabilidades_FAS(ID_BANCO_IMAGENS,RESULTADO_FAVORABILIDADE,VETOR_FAVORABILIDADE,JANELA_TEMPO_INICIAL,JANELA_TEMPO_FINAL,ABORDAGEM_FUSAO_DADOS):
    # Inserir dados de inserção da tabela "FAVORABILIDADE_FAS"

    # Consulta no Banco de Dados Oracle
    sql="insert into FAVORABILIDADES_FAS (ID_FAVORABILIDADE,ID_BANCO_IMAGENS,RESULTADO_FAVORABILIDADE,VETOR_FAVORABILIDADE,JANELA_TEMPO_INICIAL,JANELA_TEMPO_FINAL,ABORDAGEM_FUSAO_DADOS)"
    
    # Inserir dados de valores da tupla
    sql_values="values (ID_FAVORABILIDADE_FAS_SEQ.nextval," + str(ID_BANCO_IMAGENS) + ",'" + str(RESULTADO_FAVORABILIDADE) + "','" + str(VETOR_FAVORABILIDADE) + "',TO_DATE(" + str(JANELA_TEMPO_INICIAL) +\
    "),TO_DATE(" + str(JANELA_TEMPO_FINAL) + "),'" + str(ABORDAGEM_FUSAO_DADOS) + "');\n"
    #incrementar uma linha do script
    text=''
    text+=sql + sql_values
    
    return text

#------------------------------------------------------------------------------------------------

# Script SQL para inserir dados na tabela "IMAGEM_CLIMA_FAVORAB" no Banco Oracle (Cloud)
def gerarScriptSQLImagemClima_Favorab(dataframe_dados):
    text=''
    for idx, dados in dataframe_dados.iterrows():
        # Inserir dados de inserção da tabela "FAVORABILIDADE_FAS"

        # Consulta no Banco de Dados Oracle
        sql="insert into IMAGEM_CLIMA_FAVORAB (ID_IMAGEM_CLIMA_FAVORAB,ID_BANCO_IMAGENS,ID_TAB_VERD_FAVORAB,ID_DADOS_CLIMATICOS)"

        # Inserir dados de valores da tupla
        sql_values="values (ID_IMAGEM_CLIMA_FAVORAB_SEQ.nextval," + str(dados.ID_BANCO_IMAGENS) + ",'" + str(dados.ID_TAB_VERD_FAVORAB) + "','" + str(dados.ID_DADOS_CLIMATICOS) + "');\n"
        #Incrementar uma linha do script
        text+=sql + sql_values
       
    return text

#------------------------------------------------------------------------------------------------

# Salvar script SQL em disco
def salvarScriptSQL(text,path_2,nome):
    data_hora = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(path_2 + nome + str(data_hora) + '.sql', 'w') as f:
        f.write(text)

#------------------------------------------------------------------------------------------------

# Função para Exibir as Recomendações na Aba da Aplicação WEB
def ExibirRecomendacoes(tab, resultado_markov, df_id_imagem_clima_favorab):
    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    print("ID_imagem_clima_favorab:",int(df_id_imagem_clima_favorab['ID_IMAGEM_CLIMA_FAVORAB']))

    id_imagem_clima_favorab = int(df_id_imagem_clima_favorab['ID_IMAGEM_CLIMA_FAVORAB'])

    # A partir do objeto de conexão executar a consulta na base de dados
    with connection.cursor() as cursor:
        try:
            # Consulta no Banco de Dados Oracle
            sql_1="SELECT ID_FUNGICIDA,TRATAMENTO,DOSAGEM_1,DOSAGEM_2,SEVERIDADE,PORCENTAGEM_CONTROLE,PRODUTIVIDADE FROM FUNGICIDAS"
                                                       
            # Carregar o resultado da consulta no DataFrame
            df_recomendacoes=pd.DataFrame(cursor.execute(sql_1), columns=['ID','TRATAMENTO','DOSAGEM 1',\
                'DOSAGEM 2','SEVERIDADE','% CONTROLE','PRODUTIVIDADE'])
            
            # Definir o "ID" como índice do Dataframe "df_recomendacoes"
            df_recomendacoes.set_index('ID', inplace=True)                      

            # Consulta do Texto correspondente à recomendação de acordo com o resultado do Modelo de Markov
            # Se resultado de Favorabilidade for "Baixa"
            if resultado_markov == "Favorabilidade Baixa":
                sql_2="SELECT RECOMENDACAO_FAVORAB_BAIXA FROM RECOMENDACOES"
                
            # Se resultado de Favorabilidade for "Média"
            if resultado_markov == "Favorabilidade Média":
                sql_2="SELECT RECOMENDACAO_FAVORAB_MEDIA FROM RECOMENDACOES"
                
            # Se resultado de Favorabilidade for "Alta"
            if resultado_markov == "Favorabilidade Alta":
                sql_2="SELECT RECOMENDACAO_FAVORAB_ALTA FROM RECOMENDACOES"                

            # Executar comando SQL selecionado
            cursor.execute(sql_2)

            # Recebe Dados tipo CLOB do Banco ORACLE
            for row in cursor:
                df_recomendacoes_texto=pd.DataFrame([[row[0].read()]], columns=['RECOMENDAÇÃO'])
            
            # Consulta no Banco de Dados ORACLE para trazer o tipo de cultura associada à imagem original que deu origem à segmentação
            #    => que foi processada via imagens segmentadas de resultado do processamento
            sql_3="SELECT ID_DADOS_PLANTA_SOJA, VARIEDADE_CULTURA, DISTANCIA_LINHA_CULTURA, ALTURA_PLANTA_CULTURA, DISTANCIA_PLANTA_CULTURA FROM \
                              DADOS_PLANTA_SOJA WHERE ID_DADOS_PLANTA_SOJA =" + str(id_imagem_clima_favorab)

            # Carregar o resultado da consulta no DataFrame
            df_dados_planta_soja=pd.DataFrame(cursor.execute(sql_3), columns=['ID','VARIEDADE DA CULTURA', 'DISTÂNCIA ENTRE LINHAS (Metros)',\
                                                                               'ALTURA DA PLANTA (Metros)', 'DISTÂNCIA ENTRE PLANTAS (Metros)'])
            
            # Definir o "ID" como índice do Dataframe "df_dados_planta_soja"
            df_dados_planta_soja.set_index('ID', inplace=True) 
    
    # Exceção
        except cx_Oracle.Error as e:
            error, = e.args
            print(error.message)
            print(sql_1)
            if (error.offset):
                print('^'.rjust(error.offset+1, ' '))

    # Fechar a Conexão
    connection.close()

    print(df_recomendacoes_texto)

    #****************************************************
    # Exibir os Dataframes (Tabela e Texto) no Dashboard
    #****************************************************
    with tab:
        # Adiconar a Tabela de Fungicidas
            # Formatação para precisão das colunas "Float"
        tab.subheader("Opções e Seleção de Fungicidas:")

        tab.markdown("""
            <p>***Sujeito a atualização, conforme <a href="https://www.gov.br/agricultura/pt-br/assuntos/insumos-agropecuarios/insumos-agricolas/agrotoxicos/agrofit" target="_blank">Agrofit</a></p>
        """, unsafe_allow_html=True)

        tab.dataframe(df_recomendacoes.style.format({'SEVERIDADE':'{:.2f}', '% CONTROLE':'{:.2f}'}))

        tab.dataframe(df_dados_planta_soja.style.format({'DISTÂNCIA ENTRE LINHAS (Metros)':'{:.0f}','ALTURA DA PLANTA (Metros)':'{:.2f}',\
                                                          'DISTÂNCIA ENTRE PLANTAS (Metros)':'{:.2f}'}))
        
        # Adicionar o Texto de Recomendação
        tab.subheader("Boas Práticas de Manejo da Soja (Visão Agronômica):")
        tab.write(df_recomendacoes_texto.iloc[0]['RECOMENDAÇÃO'])

    return df_recomendacoes, df_recomendacoes_texto

#------------------------------------------------------------------------------------------------

def exibirDadosProcessamentoImagens(df_consulta_caract, tab, img_segmentadas, lista_img_segment, df_consulta_sementes,\
         lista_consulta_sementes, df_consulta_estatistico, lista_consulta_estatistico):

    #*********************************************************************
    # Exibir o Dataframes e Demais dados na Aba "Processamento de Imagens"
    #*********************************************************************
    with tab:
        # Configurações de Tabela "Configurações Gerais - Imagens Segmentadas":

        # Inserir nova coluna à pesquisa do banco de dados com os dados de índice das Imagens Segmentadas
        df_consulta_caract.insert(6, "nova_coluna", lista_img_segment, True)
        # Nomear as colunas do Dataframe
        df_consulta_caract.columns=['COORD. SEMENTE','COORD. VIZINHANÇA SEMENTE', 'TOTAL PIXELS JANELA','LIMIAR 1',\
                            'LIMIAR 2','FAIXA LIMIARES','IMG_SEGMENTADA']
        # Configurar os índices do Dataframe com os valores de índices das imagens segmentadas
        df_consulta_caract= df_consulta_caract.set_index('IMG_SEGMENTADA')

        #-------------------------

        # Inserir nova coluna à pesquisa do banco de dados com os dados de índice das Imagens Segmentadas
        df_consulta_sementes.insert(4, "nova_coluna", lista_consulta_sementes, True)
        # Nomear as colunas do Dataframe
        df_consulta_sementes.columns=['DESCRIÇÃO COR SEMENTE','COR RGB SEMENTE','DADOS SEMENTES',\
                             'TOTAL SEMENTES CALCULADAS','IMG_SEGMENTADA']
        # Configurar os índices do Dataframe com os valores de índices das imagens segmentadas
        df_consulta_sementes= df_consulta_sementes.set_index('IMG_SEGMENTADA')

         #-------------------------

        # Inserir nova coluna à pesquisa do banco de dados com os dados de índice das Imagens Segmentadas
        df_consulta_estatistico.insert(4, "nova_coluna", lista_consulta_estatistico, True)
        # Nomear as colunas do Dataframe
        df_consulta_estatistico.columns=['ERRO ESTATÍSTICO CALCULADO','OPERAÇÃO','DESVIO PADRÃO',\
                                'VARIÂNCIA SEGMENTACAO','IMG_SEGMENTADA']
        # Configurar os índices do Dataframe com os valores de índices das imagens segmentadas
        df_consulta_estatistico= df_consulta_estatistico.set_index('IMG_SEGMENTADA')

        #-------------------------

        # Adicionar a Tabela dos Dados das Imagens Processadas
            # Formatação de Títulos; e precisão das colunas "Float"
            # Formatação da precisão des colunas "Float"
        
        tab.latex(r'''
        \textcolor{black}{\textbf{Imagens Segmentadas:}}
        ''')                    
        tab.pyplot(img_segmentadas)

        tab.latex(r'''
        \textcolor{black}{\textbf{Etapa 2: Coordenadas e Limiares - Pixel Semente:}} \\
        \textcolor{black}{\textit{(Cálculo da Vizinhança do Pixel Semente)}}
        ''') 
        tab.dataframe(df_consulta_caract)

        tab.latex(r'''
        \textcolor{black}{\textbf{Etapa 2: Sementes - Imagens Segmentadas:}}
        ''') 
        tab.dataframe(df_consulta_sementes)

        tab.latex(r'''
        \textcolor{black}{\textbf{Etapa 2: Estatísticas Cálculos - Imagens Segmentadas:}}
        ''')
        # Formatação de Precisão - Cálculos Estatísticos
        tab.dataframe(df_consulta_estatistico.style.format({'ERRO ESTATÍSTICO CALCULADO':'{:.2f}',\
             'DESVIO PADRÃO':'{:.2f}','VARIÂNCIA SEGMENTACAO':'{:.2f}'}))

#------------------------------------------------------------------------------------------------

def exibir_dados_qualidade_dados(tab, df_consulta_qualidade, lista_consulta_qualidade, fig_histograma, fig_boxplot, df_consulta_relat_classificacao,\
                                  fig_matriz_curva_classificacao, df_instancias_duplicadas, arquivo_4, fig_qualidade_fusao):

    # Definição de Colunas (fora dos Conteiners)
    dash_6_col_0_1, dash_6_col_0_2, dash_6_col_0_3= tab.columns([0.1,2.0,1.5], gap="medium")
    
    #************************************************************************
    # Exibir tabela com os Indicadores de Qualidade para as Fases do Processo
    #************************************************************************

    # Dados dos Indicadores de Qualidade Segmentação
    dados_ind_segmentacao=[['Histograma, SSIM, PSNR, MSE','% Outliers']]
    
    # Inicializar Dataframe para exibição de Indicadores de Qualidade Etapa Segmentação
    df_indicadores=pd.DataFrame(dados_ind_segmentacao, columns=['Filtro de Mediana','Outliers'], index=["Indicadores:"])

    # Exibição de Título e Indicadores da Etapa de Segmentação
    dash_6_col_0_2.latex(r'''
            \textcolor{black}{\textbf{Indicadores de Qualidade - Fase Segmentação:}}\\
            \textcolor{blue}{\textbf{\footnotesize{Dimensões: Validade, Confiabilidade, Janela Temporal de Coleta}}}            
            ''')
    
    dash_6_col_0_2.dataframe(df_indicadores)

    #---------------------------------------

    # Dados dos Indicadores de Qualidade Fase de Extração Características/Reconhecimento de Padrões
    dados_ind_caract_padroes=[['% Valores Ausentes','% Redução de Dimensionalidade']]
    
    # Inicializar Dataframe para exibição de Indicadores de Qualidade Fase de Extração de Características/Reconhecimento de Padrões
    df_dados_ind_caract_padroes=pd.DataFrame(dados_ind_caract_padroes, columns=['Imputação','Alta Dimensionalidade'], index=["Indicadores:"])

    # Exibição de Título e Indicadores da Fase de Extração de Características/Reconhecimento de Padrões
    dash_6_col_0_2.latex(r'''
            \textcolor{black}{\textbf{Indicadores de Qualidade - Fase Extração de Características e Reconhecimento de Padrões:}}\\
            \textcolor{blue}{\textbf{\footnotesize{Dimensões: Validade, Exatidão}}}
            ''')
    dash_6_col_0_2.dataframe(df_dados_ind_caract_padroes)

     #---------------------------------------
    
    # Dados dos Indicadores de Qualidade Fase Aprendizado de Máquinas (Classificação)
    dados_ind_aprend_maquinas=[['% Instâncias Duplicadas Eliminadas','% Precisão, Acurácia, F1 Score, Revocação','VP, VN, FP, FN, Área sob a Curva']]
    
    # Inicializar Dataframe para exibição de Indicadores Fase Fase Aprendizado de Máquinas (Classificação)
    df_dados_dados_ind_aprend_maquinas=pd.DataFrame(dados_ind_aprend_maquinas, columns=['Instâncias Duplicadas','Relatório Classificador',\
                                                                                        'Matriz confusão e Curva ROC'], index=["Indicadores:"])

    # Exibição de Título e Indicadores Fase Aprendizado de Máquinas (Classificação)
    dash_6_col_0_2.latex(r'''
            \textcolor{black}{\textbf{Indicadores de Qualidade - Fase Aprendizado de Máquinas:}}\\
            \textcolor{blue}{\textbf{\footnotesize{Dimensão: Exatidão}}}
            ''')
    dash_6_col_0_2.dataframe(df_dados_dados_ind_aprend_maquinas)

    #---------------------------------------

    # Dados dos Indicadores de Qualidade Fase Fusão de Dados
    dados_ind_fusao_dados=[['Histograma','MSE']]
    
    # Inicializar Dataframe para exibição de Indicadores Fase de Fusão de Dados
    df_dados_ind_dados_ind_fusao_dados=pd.DataFrame(dados_ind_fusao_dados, columns=['Precisão','Acurácia'], index=["Indicadores:"])

    # Exibição de Título e Indicadores da Fase de Fusão de Dados
    dash_6_col_0_2.latex(r'''
            \textcolor{black}{\textbf{Indicadores de Qualidade - Fase Fusão de Dados:}}\\
            \textcolor{blue}{\textbf{\footnotesize{Dimensões: Exatidão, Janela Temporal de Coleta}}}
            ''')
    dash_6_col_0_2.dataframe(df_dados_ind_dados_ind_fusao_dados)

         
    #****************************************************************
    # Exibir o Dataframes e Demais dados na Aba "Qualidade de Dados"
    #****************************************************************
    with tab:
        # Configurações Gerais - "Qualidade de Dados":
            # -> Criação dos Conteiners
        qualidade_segmentacao = tab.expander("Qualidade de Dados - Segmentação")
        qualidade_extracao_caracteristicas = tab.expander("Qualidade de Dados - Extração de Características")
        qualidade_aprendizado_maquinas = tab.expander("Qualidade de Dados - Aprendizado de Máquinas")
        qualidade_fusao_dados = tab.expander("Qualidade de Dados - Fusão de Dados")
        qualidade_dados_DW=tab.expander("Qualidade de Dados - Base de Dados (Data Warehouse)")                 
                
        #----------------------------------------------------------------------------
        # Qualidade na Etapa de Segmentação
        #----------------------------------------------------------------------------

        # Inserir nova coluna com os dados de índice das Imagens Segmentadas
        df_consulta_qualidade.insert(5, "nova_coluna", lista_consulta_qualidade, True)
        # Nomear as colunas do Dataframe
        df_consulta_qualidade.columns=['Métrica MSE','Métrica PSNR','Métrica SSIM','Outliers Sementes','Outliers Sementes - Cálculo','IMG_SEGMENTADA']
        # Configurar os índices do Dataframe com os valores de índices das imagens segmentadas
        df_consulta_qualidade= df_consulta_qualidade.set_index('IMG_SEGMENTADA')

        # Conteiner de Expansão
        with qualidade_segmentacao:

            # Exibição de Título e Figura do Histograma da Imagem Segmentada
            qualidade_segmentacao.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Histograma:}}
            ''')
            qualidade_segmentacao.pyplot(fig_histograma)

            # Definição de Colunas para o Conteiner
            dash_6_col_1_1, dash_6_col_1_2, dash_6_col_1_3= st.columns([0.8,1.8,0.8], gap="medium")

            # Exibição de Título e Métricas em formato de "Tabela" (Dataframe)
            dash_6_col_1_2.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Imagens Segmentadas}} \\
            \textcolor{black}{\textit{(Métricas: Filtro Mediana e Similaridade; Outliers Cálculo Estatístico)}}
            ''')
                #->  Formatação de Precisão - Cálculos Estatísticos
            dash_6_col_1_2.dataframe(df_consulta_qualidade.style.format({'Métrica MSE':'{:.3f}',\
                'Métrica PSNR':'{:.3f}','Métrica SSIM':'{:.3f}'}))   
        
        # Exibição fora do Conteiner
            #-> Título e exibição dos Gráficos de Boxplot
        qualidade_segmentacao.latex(r'''
        \textcolor{black}{\textbf{Qualidade de Dados - Sementes "Sem Processamento" e "Com Processamento" (Outliers):}}
        ''')
        qualidade_segmentacao.pyplot(fig_boxplot) 

        #----------------------------------------------------------------------------
        # Qualidade na Etapa de Extração de Características
        #----------------------------------------------------------------------------

        # Conteiner de Expansão
        with qualidade_extracao_caracteristicas:
            # Definição de Colunas para o Conteiner
            dash_6_col_2_1, dash_6_col_2_2, dash_6_col_2_3= st.columns([0.2,0.9,1.5], gap="medium")

            # Dados para Dimensionalidade
            dados_dim=[['130','19']]
            
            # Inicializar Dataframe para exibição de Dados Estáticos (Dimensionalidade)
            #   => Estes dados são fixos para o trabalho e por esta razão não foram armazenados no Banco Oracle
            df_dimensionalidade=pd.DataFrame(dados_dim, columns=['Original','Reduzida'], index=["Dimensão:"])            

            # Exibir o Título e os Dados de Redução de Dimensionalidade
                # -> Dados de entrada no Classificador originados da Extração de Características
            dash_6_col_2_2.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Redução de Dimensionalidade:}}
            ''')
            dash_6_col_2_2.dataframe(df_dimensionalidade)

        #----------------------------------------------------------------------------
        # Qualidade na Etapa de Aprendizado de Máquinas
        #----------------------------------------------------------------------------
        
        # Inserir nova coluna com os dados de índice de Instâncias Duplicadas
        df_instancias_duplicadas.insert(1, "nova_coluna", 'Utilização: 100%', True)
        # Nomear as colunas do Dataframe
        df_instancias_duplicadas.columns=['Tuplas Binárias Limpas','% Utilização:']
        # Configurar os índices do Dataframe com os valores de índices de Instâncias Duplicadas
        df_instancias_duplicadas= df_instancias_duplicadas.set_index('% Utilização:')

        # Conteiner
        with qualidade_aprendizado_maquinas:
            dash_6_col_3_1, dash_6_col_3_2, dash_6_col_3_3= st.columns([0.1,1.0,1.5], gap="medium")
           
            # Exibir o Título e os Dados de Instâncias Duplicadas
                # -> Dados de entrada no Classificador originados da Extração de Características
            dash_6_col_3_2.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Instâncias Duplicadas:}}
            ''')
            dash_6_col_3_2.dataframe(df_instancias_duplicadas)

            # Exibir o Título e os Dados do Relatório de Classificação
            dash_6_col_3_2.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Relatório de Classificação:}}
            ''')
            dash_6_col_3_2.text(df_consulta_relat_classificacao.iloc[0]['relatorioClassificacao'])

            # Exibir o Título e a Figuras: (1) Matriz de Confusão e (2) Curva ROC
            qualidade_aprendizado_maquinas.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Matriz de Confusão e Curva ROC:}}
            ''')
            qualidade_aprendizado_maquinas.pyplot(fig_matriz_curva_classificacao)

        #----------------------------------------------------------------------------
        # Qualidade na Etapa de Fusão de Dados
        #----------------------------------------------------------------------------
        
        # Cointeiner
        with qualidade_fusao_dados:
            # Definição de Colunas para o Conteiner
            dash_6_col_4_1, dash_6_col_4_2, dash_6_col_4_3= st.columns([0.2,0.9,2.0], gap="medium")

            # Exibir o Título do Relatório de Qualidade de Dados - Fusão de Dados 
            dash_6_col_4_2.latex(r'''
            \textcolor{black}{\textbf{Análise da Qualidade de Dados - Etapa Fusão de Dados:}}
            ''')
            dash_6_col_4_2.pyplot(fig_qualidade_fusao)
        
        #----------------------------------------------------------------------------
        # Qualidade na Etapa de Base de Dados: Data Warehouse (Oracle Cloud)
        #----------------------------------------------------------------------------

        # Cointeiner
        with qualidade_dados_DW:
            # Exibir o Título do Relatório de Qualidade de Dados do Data Warehouse 
            qualidade_dados_DW.latex(r'''
            \textcolor{black}{\textbf{Qualidade de Dados - Base de Dados: Data Warehouse (Oracle Cloud):}}
            ''')

            # Abertura de Arquivo PDF dos Relatórios Qualidade de Dados 
            with open(arquivo_4,"rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="800" type="application/pdf"></iframe>'
            qualidade_dados_DW.markdown(pdf_display, unsafe_allow_html=True)
        

#------------------------------------------------------------------------------------------------
# Chamada de Função para Exibir Relatórios Originados do Data Warehouse
def exibirRelatorios_DW(tab, arquivo_1, arquivo_2, arquivo_3):
    
    relatorios_conteiner= dash_col_0_2.expander("Exibir Relatórios - Auxílio a Tomada de Decisão:")
    
    #****************************************************************************************************************
    # Exibir o Conteiner de Expansão - Requisitos 1 "Aba Dashboard": Exibir Relatórios - Auxílio a Tomada de Decisão:
    #****************************************************************************************************************
    requisitos_1 = relatorios_conteiner.expander("Requisitos de Projeto: 1")
    requisitos_1.markdown("""
        <table border="2" cellpadding="0" cellspacing="0" style="width:900px">
            <tbody>
                <tr>
                    <td style="text-align:center"><strong>Assunto 1: Influ&ecirc;ncia das Vari&aacute;veis Clim&aacute;ticas na Favorabilidade da Ferrugem Asi&aacute;tica da Soja:&nbsp;</strong></td>
                </tr>
                <tr>
                    <td><u><strong>Descri&ccedil;&atilde;o:</strong></u></td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do ano que a Temperatura (m&iacute;nima, m&aacute;xima) pode favorecer o aparecimento da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do ano que a Temperatura (Faixa de Temperatura) pode favorecer o aparecimento da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura que a Umidade Relativa contribuiu para o aparecimento da doen&ccedil;a da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura que o Ponto de Orvalho contribuiu para o aparecimento da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura que a Precipita&ccedil;&atilde;o contribui para o aparecimento da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura que a Per&iacute;odo M&iacute;nimo de Molhamento Foliar contribui para o aparecimento da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura que a Per&iacute;odo de Molhamento Foliar contribui para o aparecimento da FAS?</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    # Abertura de Arquivo PDF dos Relatórios Assunto 1 - Data Warehouse
    with open(arquivo_1,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="460" type="application/pdf"></iframe>'    
    requisitos_1.markdown(pdf_display, unsafe_allow_html=True)

    #****************************************************************************************************************
    # Exibir o Conteiner de Expansão - Requisitos 2 "Aba Dashboard": Exibir Relatórios - Auxílio a Tomada de Decisão:
    #****************************************************************************************************************

    requisitos_2 = relatorios_conteiner.expander("Requisitos de Projeto: 2")
    requisitos_2.markdown("""
        <table border="2" cellpadding="0" cellspacing="0" style="width:900px">
            <tbody>
                <tr>
                    <td style="text-align:center"><strong>Assunto 2: Contabiliza&ccedil;&atilde;o da Favorabilidade Baixa, M&eacute;dia e Alta por Ano:</strong></td>
                </tr>
                <tr>
                    <td><strong><u>Descri&ccedil;&atilde;o:</u></strong></td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura, que compreende a etapa de plantio e colheita por Regi&atilde;o, mostra a favorabilidade Baixa da FAS?</td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura, que compreende a etapa de plantio e colheita por Regi&atilde;o, mostra a favorabilidade M&eacute;dia da FAS?</td>
                </tr>
                <tr>
                    <td>
                    <p><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do Ciclo de Cultura, que compreende a etapa de plantio e colheita por Regi&atilde;o, mostra a favorabilidade Alta da FAS?</p>
                    </td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    # Abertura de Arquivo PDF dos Relatórios Assunto 2 - Data Warehouse
    with open(arquivo_2,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="600" type="application/pdf"></iframe>'
    requisitos_2.markdown(pdf_display, unsafe_allow_html=True)
    
    #****************************************************************************************************************
    # Exibir o Conteiner de Expansão - Requisitos 3 "Aba Dashboard": Exibir Relatórios - Auxílio a Tomada de Decisão:
    #****************************************************************************************************************
    requisitos_3 = relatorios_conteiner.expander("Requisitos de Projeto: 3")
    requisitos_3.markdown("""
        <table border="2" cellpadding="0" cellspacing="0" style="width:900px">
            <tbody>
                <tr>
                    <td style="text-align:center"><strong>Assunto 3: Influ&ecirc;ncia da Imagem da Folha de Soja na Favorabilidade da Ferrugem Asi&aacute;tica da Soja:</strong></td>
                </tr>
                <tr>
                    <td><strong><u>Descri&ccedil;&atilde;o:</u></strong></td>
                </tr>
                <tr>
                    <td><span style="font-size:14px">&nbsp;Qual o per&iacute;odo do ano, que compreende a etapa de plantio e colheita (R5 e R6) por Regi&atilde;o, que a informa&ccedil;&atilde;o da Imagem da Folha de Soja contribuiu para o aparecimento da doen&ccedil;a da FAS?</span></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    
    # Abertura de Arquivo PDF dos Relatórios Assunto 3 - Data Warehouse
    with open(arquivo_3,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="900" height="600" type="application/pdf"></iframe>'
    requisitos_3.markdown(pdf_display, unsafe_allow_html=True)
                  
#==========================================================================

# Função para contabizar contagem de tempo funções Cadeia Oculta de Markov

def contabilizarTempo(t0,t):
    # Cálculo de c(t) - Tempo de Processamento
    ct=t/t0
    
    # Imprimir os resultados do Cálculo do Tempo de Processamento
    print("\nContagem de Tempo - Abordagem de Markov:")
    print("Tempo Inicial(t0): " + str(t0) +  "\nTempo Final(t): " + str(t) + "\nC(t): " + str(ct))

    return ct

#==========================================================================

# Função para Calcular Qualidade de Dados - Fusão de Dados

def calcularQualidadeFusao(ct, dadosMarkov):    

    vetor_resultado_linhas=pd.DataFrame([[int(dadosMarkov.iloc[0,0]),dadosMarkov.iloc[0,1],dadosMarkov.iloc[0,2],dadosMarkov.iloc[0,3], \
                                                dadosMarkov.iloc[0,4],dadosMarkov.iloc[0,5],dadosMarkov.iloc[0,6]]]).to_numpy()
    
    print("Entrada gráfico qualidade fusão: ", vetor_resultado_linhas)

    # Somatório 
    somatorio=1+2*((1-(1/7))+(1-(2/7))+(1-(3/7))+(1-(4/7))+(1-(5/7))+(1-(6/7)))

    # Variância do Observável (Caso especial de Autocorrelação)
    #   -> Entrada dados de entrada Cadeia de Markov
    var_observavel=np.var(vetor_resultado_linhas)/7 * (somatorio * ct)    
    
    return var_observavel

#==========================================================================

# Função Gráfico Qualidade de Dados - Fusão de Dados

def graficoQualidadeFusaoDados(dadosCalculo):
    # Eixo "x"
    #   -> Pontos de entrada (Dados Calculados)
    x = []
    x.append(dadosCalculo)
    # Eixo "y"
    y = np.arange(len(x))

    # Cálculo do desvio padrão por ponto no cálculo
    std = []
    # Percorre os dados de entrada e calcula o desvio padrão "por ponto"
    for i in range(len(x)):    
        std.append(np.sqrt(x[i]))       

    # Plotar o gráfico
    fig_qualidade_fusao = plt.figure(figsize = (8,5))
    plt.errorbar(y, x, yerr=std, fmt='o', color='blue', 
                 mew=0.5, ms=4, ecolor='black', capsize=4, elinewidth=0.4)
    plt.ylim(-0.4, 1.4)
    plt.xlabel('Entrada dados Markov')
    plt.ylabel('Estado das Variáveis')    
    plt.title('Gráfico Autoconsistência vs Erro Razoável (Desvio Padrão)')
    
    return fig_qualidade_fusao

    #==========================================================================

# Função para Chamadas das Funções - Interação com a Interface de Usuário
def processar(input_data_teste):

    #------------------------------------------------------------------------------------------------
    #                                       CHAMADAS DE FUNÇÕES
    #------------------------------------------------------------------------------------------------
  
    #Chamada de Função para Entrada de Data da Janela de Tempo
    #Informar a Janela de Tempo como "Intervalo"
    DataInicial, DataFinal = dataJanelaTempo(intervalo,0,input_data_teste)

    #=======================================================================

    # Chamada de função para conexão com o Oracle Autonomous Database
    connection=conexaoAutonomousDatabase(fun.PYTHON_USERNAME,fun.PYTHON_PASSWORD,fun.PYTHON_CONNECTSTRING)

    #=======================================================================

    # Chamada de Função para consulta de Dados Climáticos (Janela de Tempo) no Banco ORACLE
    df_consulta_bd=consultarDadosClimaticos(connection,DataInicial,DataFinal)

    #=======================================================================

    # Chamada de Função para gerar a lista de dados interpolados, de acordo com as Variáveis climáticas
    X, lista_interpolacao, labels=preparaDadosInterpolacao(df_consulta_bd)

    #=======================================================================

    # Chamada de Função para Processamento de Interpolação
    df_interpolar,new_y=processarInterpolacao(X,labels,lista_interpolacao,tab3,0)

    #=======================================================================

    # Chamada de Função para processamento dos valores interpolados para completar (se necessário) o conjunto de dados com os dados faltantes
    df_consulta_bd=processarCompletarDadosInterpolados(df_interpolar,df_consulta_bd,tab3)

    #=======================================================================

    # Chamada de Função Regra 01 -> (Período de Molhamento Foliar)
    medianaRegra_01, regra_1, flag_regra_1=regra01(df_consulta_bd,casas_decimais)

    #=======================================================================

    # Chamada de Função Regra 02 -> (Período Mínimo de Molhamento Foliar)
    medianaRegra_02, regra_2, flag_regra_2=regra02(df_consulta_bd,casas_decimais)

    #=======================================================================

    #Chamada de Função Regra 03 
    medianaRegra_03_1, medianaRegra_03_2, regra_3, flag_regra_3, flag_df=regra03(df_consulta_bd,casas_decimais)

    #=======================================================================

    # Chamada Função Regra 04
    regra_4, regra_4_valor, flag_regra_4=regra04(df_consulta_bd,casas_decimais)

    #=======================================================================

    # Chamada de Função Regra 05
    regra_5, regra_5_valor, flag_regra_5=regra05(df_consulta_bd,casas_decimais)

    #=======================================================================

    # Chamada de Função Regra 06
    regra_6, medianaRegra_06, flag_regra_6=regra06(df_consulta_bd,casas_decimais)

    #=======================================================================

    # Chamada de Função Regra 07
    regra_7, df_consulta_img, flag_regra_7, df_consulta_relat_classificacao, \
        fig_matriz_curva_classificacao,df_instancias_duplicadas,df_id_imagem_clima_favorab=regra07(DataInicial,DataFinal)
    
    #=======================================================================

    # Chamada de Função para Exibir Relatórios Originados do Data Warehouse
    exibirRelatorios_DW(tab1, relatorio_assunto_1, relatorio_assunto_2, relatorio_assunto_3)

    #=======================================================================

    #Chamada de Função para Exibir Imagens Segmentadas participantes da Janela de Tempo
    df_consulta_caract, fig1, lista_img_segment, df_consulta_sementes, lista_consulta_sementes,\
        df_consulta_estatistico, lista_consulta_estatistico, df_consulta_qualidade, \
        lista_consulta_qualidade, fig_boxplot=exibirImagensParticipantes(df_consulta_img, tab1)

    #=======================================================================
    
    #Chamada de Função para Exibir Histogramas
    fig_histograma=exibirHistogramas(df_consulta_img)

    #=======================================================================

    # Função para Contagem de Ocorrências por Regras
    dados_regras, totalJanela, ocorrenciasRegra_1, ocorrenciasRegra_2, ocorrenciasRegra_3, ocorrenciasRegra_4, \
    ocorrenciasRegra_5, ocorrenciasRegra_6, ocorrenciasRegra_7=contagemOcorrencias(df_consulta_bd,             \
        regra_1,regra_2,regra_3,regra_4,regra_5,regra_6,regra_7,medianaRegra_01,medianaRegra_02,regra_4_valor, \
        regra_5_valor,medianaRegra_06, casas_decimais, flag_df, medianaRegra_03_1, medianaRegra_03_2)

    #=======================================================================

    # Chamada de Função para Plotar gráfico de ocorrências
    x,y=plotarOcorrencias(ocorrenciasRegra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,ocorrenciasRegra_4,ocorrenciasRegra_5,\
    ocorrenciasRegra_6,ocorrenciasRegra_7, tab1)

    #=======================================================================

    # Início da Contagem de Tempo para Medição de tempo Abordagem de Markov (Tempo Inicial t0)
        # => Tempo em Milisegundos
    t0=timeit.default_timer()
    # Chamada de Função para Carregar a Tabela Verdade (Abordagem Markov)
    df_tab_verdade=carregarTabelaVerdade()

    #=======================================================================

    # Chamada de Função para encontrar a Combinação da Tabela - Descobrir o Estado correspondente    
    vetor_resultado, vetor_compara, vetor_ocorrencias, text=encontraCombinacao(ocorrenciasRegra_1,flag_regra_1,ocorrenciasRegra_2,ocorrenciasRegra_3,\
        ocorrenciasRegra_4,ocorrenciasRegra_5,ocorrenciasRegra_6,ocorrenciasRegra_7,df_tab_verdade, tab1)    

    #=======================================================================

    # Chamada de Função para capturar o índice do resultado do "vetor_resultado"    
    df_img_cli_favorab,text=capturarIndiceFavorab(vetor_resultado,text,df_consulta_bd)    

    #=======================================================================

    # Chamada de Função para identificar a probabilidade do Estado Atual    
    probab_estado, probab_previsao, matriz_transicao, probab_inicial, text=probabilidadeEstadoAtual(text,vetor_resultado)    

    #=======================================================================

    # Chamada de Função para identificar o Estado do Atual da Favorabilidade FAS
    previsao_prox, resultado_markov, text=identificaEstadoAtual(vetor_resultado,\
        probab_previsao, text, tab2)    

    #=======================================================================
    
    # Chamada de Função para Exibição do Modelo Gráfico
    exibir_img_modelo(resultado_markov, tab1)
    # Finalizar contagem de tempo para Medição de tempo Abordagem de Markov (Tempo Inicial t)
        # => Tempo em Milisegundos
    t=timeit.default_timer()          

    #====================================================================================

    # Chamada de Função para contabizar contagem de tempo funções Cadeia Oculta de Markov
    ct= contabilizarTempo(t0,t)
    
    #====================================================================================

    # Chamada de Função para Calcular Qualidade de Dados - Fusão de Dados

    var_observavel= calcularQualidadeFusao(ct, vetor_resultado)

    #====================================================================================

    # Chamada de Função Gráfico Qualidade de Dados - Fusão de Dados

    fig_qualidade_fusao= graficoQualidadeFusaoDados(var_observavel)

    #====================================================================================
   
    # Chamada de Função para Exibir Recomendações na Aba Aplicação WEB
    df_recomendacoes=ExibirRecomendacoes(tab2, resultado_markov, df_id_imagem_clima_favorab)

    #=======================================================================
    
    # Chamada de Função para Exibir Características das Imagens Segmentadas
    #   Aba "Processamento de Imagens"
    exibirDadosProcessamentoImagens(df_consulta_caract, tab5, fig1, lista_img_segment, df_consulta_sementes,\
         lista_consulta_sementes, df_consulta_estatistico, lista_consulta_estatistico)

    #=======================================================================
   
    # Chamada de Função para Exibir os Dados de Qualidade das Imagens Segmentadas
    #   Aba "Qualidade de Dados"
    exibir_dados_qualidade_dados(tab6, df_consulta_qualidade, lista_consulta_qualidade, fig_histograma, fig_boxplot,\
                                 df_consulta_relat_classificacao, fig_matriz_curva_classificacao, df_instancias_duplicadas, relatorio_qualidade_DW, fig_qualidade_fusao)
    
    #=======================================================================
    
    # Chamada de Função para calcular Próximas Previsão das Probabilidades
    previsao_1, previsao_2, finalizado=calcularPrevisoes(matriz_transicao, probab_inicial,previsao_prox)

    #=======================================================================
    
    # Mensagem de Finalização do Ciclo de Processamento
    #   -> Exibir a mensagem no canto esquerdo inferior da Barra Lateral (sidebar)
    if finalizado == True:
        with tab1:
            st.sidebar.success('Processamento do Método Finalizado com Sucesso!', icon="✅")

#========================================================================================================

# Chamada de Função para os componentes de filtro para entrada de dados - Dashboard
data_selecionada, botao=definirFiltrosEntrada()
input_data_teste=data_selecionada

if botao:
    processar(input_data_teste)

#========================================== FIM =========================================================