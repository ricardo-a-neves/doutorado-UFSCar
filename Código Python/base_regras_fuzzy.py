from skfuzzy import control as ctrl
from itertools import combinations

def regras(periodoMinMolhamentoFoliar,periodoMolhamentoFoliar,dadosCultivarImagem,pontoOrvalho,faixaTemperaturaInicial,faixaTemperaturaFinal,temperaturaMinima,temperaturaMaxima, favorabilidade):

    ####################################
    ## Favorabilidade Baixa (1 opção) ##
    ####################################

    rule1_1 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura abaixo do limiar'] | 
    (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar'] | temperaturaMaxima['temperatura maxima abaixo do limiar'],
        favorabilidade['baixa'])

        # ---------------------------------------------------------------------------------------------------------------
        #SE favorabilidade for TRUE para até duas variáveis ENTÃO favorabilidade baixa
        #(1 opção: variável 1 ou variável 2 ou variável 3 ou variável 4 ou variável 5 ou variável 6 ou variável 7        
        #----------------------------------------------------------------------------------------------------------------

    #####################################
    ## Favorabilidade Baixa (2 opções) ##
    #####################################

        # ---------------------------------------------------------------------------------------------------------------
        #SE favorabilidade for TRUE para até duas variáveis ENTÃO favorabilidade baixa        
        #(2 opções: variável 1 ou grupo(variável 2 ou variável 3 ou variável 4 ou variável 5 ou variável 6 ou variável 7)
        #----------------------------------------------------------------------------------------------------------------         
         
    rule1_2 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo abaixo do limiar'] & (periodoMolhamentoFoliar['umidade abaixo do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura abaixo do limiar'] |
    (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar'] | 
    temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_3 = ctrl.Rule(periodoMolhamentoFoliar['umidade abaixo do limiar'] & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura abaixo do limiar'] |
    (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar'] | temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_4 = ctrl.Rule(dadosCultivarImagem['não favorável'] & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] | pontoOrvalho['temperatura abaixo do limiar'] |
    (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar'] | temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_5 = ctrl.Rule(pontoOrvalho['temperatura abaixo do limiar'] & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] | dadosCultivarImagem['não favorável'] |
    (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar'] | temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_6 = ctrl.Rule((faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] |
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura abaixo do limiar'] | temperaturaMinima['temperatura minima abaixo do limiar'] | temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_7 = ctrl.Rule(temperaturaMinima['temperatura minima abaixo do limiar'] & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] | dadosCultivarImagem['não favorável'] |
    pontoOrvalho['temperatura abaixo do limiar'] | (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMaxima['temperatura maxima abaixo do limiar']),
        favorabilidade['baixa'])

    rule1_8 = ctrl.Rule(temperaturaMaxima['temperatura maxima abaixo do limiar'] & (periodoMinMolhamentoFoliar['tempo abaixo do limiar'] | periodoMolhamentoFoliar['umidade abaixo do limiar'] | dadosCultivarImagem['não favorável'] |
    pontoOrvalho['temperatura abaixo do limiar'] | (faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']) | temperaturaMinima['temperatura minima abaixo do limiar']),
        favorabilidade['baixa'])

    #####################################
    ## Favorabilidade Média (3 opções) ##
    #####################################

    #------------------------------------------------------------------------------------------------------------------
    #SE favorabilidade for TRUE para até quatro variáveis ENTÃO favorabilidade média
        #(3 opções: variável 1 E variável 2 E grupo(variável 3 ou variável 4 ou variável 5 ou variável 6 ou variável 7)       
    # -----------------------------------------------------------------------------------------------------------------

    rule2_1 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & (dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_2 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & dadosCultivarImagem['não favorável'] & (periodoMolhamentoFoliar['umidade acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_3 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) |temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_4 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & (periodoMolhamentoFoliar['umidade acima do limiar'] | 
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_5 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] |
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_6 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] | 
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule2_7 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_8 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_9 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | 
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_10 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] |
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_11 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] | 
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),  
        favorabilidade['média'])

    rule2_12 = ctrl.Rule(dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_13 = ctrl.Rule(dadosCultivarImagem['não favorável'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | 
    periodoMolhamentoFoliar['umidade acima do limiar'] |pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_14 = ctrl.Rule(dadosCultivarImagem['não favorável'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | 
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_15 = ctrl.Rule(dadosCultivarImagem['não favorável'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | 
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) |temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule2_16 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | 
    periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] |  temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_17 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_18 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) |temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule2_19 = ctrl.Rule((faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | 
    periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule2_20 = ctrl.Rule((faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    periodoMolhamentoFoliar['umidade acima do limiar'] |dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule2_21 = ctrl.Rule(temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar'])),
        favorabilidade['média'])

    #####################################
    ## Favorabilidade Média (4 opções) ##
    #####################################

        #------------------------------------------------------------------------------------------------------------
        #SE favorabilidade for TRUE para até quatro variáveis ENTÃO favorabilidade média
        #(4 opções: variável 1 E variável 2 E variável 3 E grupo(variável 4 ou variável 5 ou variável 6 ou variável 7)
        #------------------------------------------------------------------------------------------------------------

    rule3_1 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] &  
    (pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_2 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & (dadosCultivarImagem['não favorável'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
    favorabilidade['média'])

    rule3_3 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_4 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] &
    (dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_5 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & periodoMolhamentoFoliar['umidade acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_6 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] &
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_7 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & dadosCultivarImagem['não favorável'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (periodoMolhamentoFoliar['umidade acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_8 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & dadosCultivarImagem['não favorável'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_9 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & dadosCultivarImagem['não favorável'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] | 
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])
        
    rule3_10 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_11 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_12 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_13 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] &
    (periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_14 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_15 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMolhamentoFoliar['umidade acima do limiar'] |
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] |(faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar'])),
        favorabilidade['média'])

    rule3_16 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_17 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_18 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_19 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & dadosCultivarImagem['não favorável'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_20 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_21 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_22 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] | 
    dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_23 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_24 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMaxima['temperatura maxima acima do limiar'] & 
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_25 = ctrl.Rule(periodoMolhamentoFoliar['umidade acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar'])),
        favorabilidade['média'])

    rule3_26 = ctrl.Rule(dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_27 = ctrl.Rule(dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    periodoMolhamentoFoliar['umidade acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_28 = ctrl.Rule(dadosCultivarImagem['não favorável'] & pontoOrvalho['temperatura acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    periodoMolhamentoFoliar['umidade acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_29 = ctrl.Rule(dadosCultivarImagem['não favorável'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_30 = ctrl.Rule(dadosCultivarImagem['não favorável'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_31 = ctrl.Rule(dadosCultivarImagem['não favorável'] & temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] & (periodoMinMolhamentoFoliar['tempo acima do limiar'] |
    periodoMolhamentoFoliar['umidade acima do limiar'] | pontoOrvalho['temperatura acima do limiar'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar'])),
        favorabilidade['média'])

    rule3_32 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | temperaturaMaxima['temperatura maxima acima do limiar']),
        favorabilidade['média'])

    rule3_33 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | temperaturaMinima['temperatura minima acima do limiar']),
        favorabilidade['média'])

    rule3_34 = ctrl.Rule(pontoOrvalho['temperatura acima do limiar'] & temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | (faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar'])),
        favorabilidade['média'])

    rule3_35 = ctrl.Rule((faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']) & temperaturaMinima['temperatura minima acima do limiar'] & temperaturaMaxima['temperatura maxima acima do limiar'] &
    (periodoMinMolhamentoFoliar['tempo acima do limiar'] | periodoMolhamentoFoliar['umidade acima do limiar'] | dadosCultivarImagem['não favorável'] | pontoOrvalho['temperatura acima do limiar']),
        favorabilidade['média'])

    ####################################
    ## Favorabilidade Alta (5 opções) ##
    ####################################
     
        #------------------------------------------------------------------------------------------------------------
        #SE favorabilidade for TRUE para acima de quatro variáveis ENTÃO favorabilidade alta
        #(5 opções: variável 1 E variável 2 E variável 3 E variável 4 E grupo(variável 5 ou variável 6 ou variável 7)        
        #------------------------------------------------------------------------------------------------------------

    rule4_1 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] &
    ((faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_2 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar']) & (pontoOrvalho['temperatura no limiar'] | temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_3 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & temperaturaMinima['temperatura minima no limiar'] &
    (pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_4 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & temperaturaMaxima['temperatura maxima no limiar'] &
    (pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_5 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar']) & (dadosCultivarImagem['favorável'] | temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_6 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] &
    (dadosCultivarImagem['favorável'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_7 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] &
    (dadosCultivarImagem['favorável'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_8 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] | (dadosCultivarImagem['favorável'] | pontoOrvalho['temperatura no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
    favorabilidade['alta'])

    rule4_9 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMaxima['temperatura maxima no limiar'] & (dadosCultivarImagem['favorável'] | pontoOrvalho['temperatura no limiar'] | temperaturaMinima['temperatura minima no limiar']),
    favorabilidade['alta'])

    rule4_10 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (dadosCultivarImagem['favorável'] | pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_11 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & (periodoMolhamentoFoliar['umidade no limiar'] | temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_12 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] &
    (periodoMolhamentoFoliar['umidade no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_13 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] &
    (periodoMolhamentoFoliar['umidade no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_14 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | pontoOrvalho['temperatura no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_15 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | pontoOrvalho['temperatura no limiar'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_16 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_17 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_18 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_19 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável'] | (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_20 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & 
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável'] |
    pontoOrvalho['temperatura no limiar']),
        favorabilidade['alta'])

    rule4_21 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar']) & (periodoMinMolhamentoFoliar['tempo no limiar'] | temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_22 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] &
    (periodoMinMolhamentoFoliar['tempo no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_23 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] &
    (periodoMinMolhamentoFoliar['tempo no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_24 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & 
    temperaturaMinima['temperatura minima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | pontoOrvalho['temperatura no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_25 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | pontoOrvalho['temperatura no limiar'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_26 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & temperaturaMinima['temperatura minima no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_27 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | dadosCultivarImagem['favorável'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_28 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | dadosCultivarImagem['favorável'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_29 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | dadosCultivarImagem['favorável'] | (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_30 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & 
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | dadosCultivarImagem['favorável'] | 
    pontoOrvalho['temperatura no limiar']),
        favorabilidade['alta'])

    rule4_31 = ctrl.Rule(dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & 
    temperaturaMinima['temperatura minima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule4_32 = ctrl.Rule(dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & 
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar'] |temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule4_33 = ctrl.Rule(dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] &
    (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule4_34 = ctrl.Rule(dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & temperaturaMinima['temperatura minima no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar'] | pontoOrvalho['temperatura no limiar']),
        favorabilidade['alta'])

    rule4_35 = ctrl.Rule(pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & temperaturaMinima['temperatura minima no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável']),
        favorabilidade['alta'])

    ####################################
    ## Favorabilidade Alta (6 opções) ##
    ####################################

        #------------------------------------------------------------------------------------------------------------
        #SE favorabilidade for TRUE para acima de quatro variáveis ENTÃO favorabilidade alta
        #(6 opções: variável 1 E variável 2 E variável 3 E variável 4 E variável 5 E grupo(variável 6 ou variável 7)
        #------------------------------------------------------------------------------------------------------------
        
    rule5_1 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & 
    (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) & (temperaturaMinima['temperatura minima no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_2 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & 
    temperaturaMinima['temperatura minima no limiar'] & ((faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_3 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & ((faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule5_4 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMinima['temperatura minima no limiar'] & (pontoOrvalho['temperatura no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_5 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMaxima['temperatura maxima no limiar'] & (pontoOrvalho['temperatura no limiar'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule5_6 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (pontoOrvalho['temperatura no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule5_7 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & (temperaturaMinima['temperatura minima no limiar'] | dadosCultivarImagem['favorável'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_8 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMaxima['temperatura maxima no limiar'] & (dadosCultivarImagem['favorável'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule5_9 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & (dadosCultivarImagem['favorável'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule5_10 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & periodoMolhamentoFoliar['umidade no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (dadosCultivarImagem['favorável'] | pontoOrvalho['temperatura no limiar']),
        favorabilidade['alta'])

    rule5_11 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMinima['temperatura minima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_12 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & 
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule5_13 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] &
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    rule5_14 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] | (periodoMolhamentoFoliar['umidade no limiar'] | pontoOrvalho['temperatura no limiar']),
        favorabilidade['alta'])

    rule5_15 = ctrl.Rule(periodoMinMolhamentoFoliar['tempo no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMolhamentoFoliar['umidade no limiar'] | dadosCultivarImagem['favorável']),
        favorabilidade['alta'])

    rule5_16 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMinima['temperatura minima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | temperaturaMaxima['temperatura maxima no limiar']),
        favorabilidade['alta'])

    rule5_17 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] &
    faixaTemperaturaFinal['faixa no limiar']) & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | temperaturaMinima['temperatura minima no limiar']),
        favorabilidade['alta'])

    rule5_18 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & temperaturaMinima['temperatura minima no limiar'] & 
    temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])),
        favorabilidade['alta'])

    # rule5_19 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & dadosCultivarImagem['favorável'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    # temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] | (periodoMinMolhamentoFoliar['tempo no limiar'] | pontoOrvalho['temperatura no limiar']),
    #     favorabilidade['alta']) ## Regra retirada (Modelo: descalibração do modelo)

    rule5_20 = ctrl.Rule(periodoMolhamentoFoliar['umidade no limiar'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | dadosCultivarImagem['favorável']),
        favorabilidade['alta'])

    rule5_21 = ctrl.Rule(dadosCultivarImagem['favorável'] & pontoOrvalho['temperatura no limiar'] & (faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar']) &
    temperaturaMinima['temperatura minima no limiar'] & temperaturaMaxima['temperatura maxima no limiar'] & (periodoMinMolhamentoFoliar['tempo no limiar'] | periodoMolhamentoFoliar['umidade no limiar']),
        favorabilidade['alta'])

    return rule1_1, rule1_2, rule1_3, rule1_4, rule1_5, rule1_6, rule1_7, rule1_8,\
        rule2_1, rule2_2, rule2_3, rule2_4, rule2_5, rule2_6, rule2_7, rule2_8, rule2_9, rule2_10,rule2_11, \
        rule2_12, rule2_13, rule2_14, rule2_15, rule2_16, rule2_17, rule2_18, rule2_19, rule2_20, rule2_21, \
        rule3_1,rule3_2,rule3_3,rule3_4,rule3_5,rule3_6,rule3_7,rule3_8,rule3_9,rule3_10,rule3_11,rule3_12, \
        rule3_13,rule3_14,rule3_15,rule3_16, rule3_17,rule3_18,rule3_19,rule3_20,rule3_21,rule3_22,rule3_23,\
        rule3_24,rule3_25,rule3_26,rule3_27,rule3_28,rule3_29,rule3_30,rule3_31, rule3_32,rule3_33,rule3_34,rule3_35, \
        rule4_1,rule4_2,rule4_3,rule4_4,rule4_5,rule4_6,rule4_7,rule4_8,rule4_9,rule4_10,rule4_11,rule4_12,rule4_13,  \
        rule4_14,rule4_15,rule4_16,rule4_17,rule4_18,rule4_19,rule4_20,rule4_21,rule4_22,rule4_23,rule4_24,rule4_25,  \
        rule4_26,rule4_27,rule4_28,rule4_29,rule4_30,rule4_31,rule4_32,rule4_33,rule4_34,rule4_35,\
        rule5_1, rule5_2, rule5_3, rule5_4, rule5_5,rule5_6, rule5_7, rule5_8, rule5_9, rule5_10,rule5_11, rule5_12,  \
        rule5_13, rule5_14, rule5_15,rule5_16, rule5_17, rule5_18, rule5_20,rule5_21

#-----------------------------------------------------------------------------
## Procedimento para gerar as combinações de Regras Fuzzy
#-----------------------------------------------------------------------------

def gerarCombinacoes():
    # Geração das combinações para Favorabilidade Alta
        # SE favorabilidade for TRUE para cinco ou mais variáveis ENTÃO favorabilidade alta

    # SE favorabilidade for TRUE para até duas variáveis ENTÃO favorabilidade baixa

    A=["periodoMolhamentoFoliar['umidade abaixo do limiar']",
     "periodoMinMolhamentoFoliar['tempo abaixo do limiar']",
     "dadosCultivarImagem['não favorável']",
     "pontoOrvalho['temperatura abaixo do limiar']",
     "faixaTemperaturaInicial['faixa abaixo do limiar'] & faixaTemperaturaFinal['faixa abaixo do limiar']",
     "temperaturaMinima['temperatura minima abaixo do limiar']",
     "temperaturaMaxima['temperatura maxima abaixo do limiar']"]

    # SE favorabilidade for TRUE para quatro variáveis ENTÃO favorabilidade média

    B=["periodoMolhamentoFoliar['umidade acima do limiar']",
     "periodoMinMolhamentoFoliar['tempo acima do limiar']",
     "dadosCultivarImagem['não favorável']",               
     "pontoOrvalho['temperatura acima do limiar']",
     "faixaTemperaturaInicial['faixa acima do limiar'] & faixaTemperaturaFinal['faixa acima do limiar']",
     "temperaturaMinima['temperatura minima acima do limiar']",
     "temperaturaMaxima['temperatura maxima acima do limiar']"]

    # SE favorabilidade for TRUE para quatro variáveis ENTÃO favorabilidade alta

    C=["periodoMinMolhamentoFoliar['tempo no limiar']",
       "periodoMolhamentoFoliar['umidade no limiar']",
       "dadosCultivarImagem['favorável']",
       "pontoOrvalho['temperatura no limiar']",
       "(faixaTemperaturaInicial['faixa no limiar'] & faixaTemperaturaFinal['faixa no limiar'])",
       "temperaturaMinima['temperatura minima no limiar']",
       "temperaturaMaxima['temperatura maxima no limiar']"]

    temp = combinations(C, 4)
    for i in list(temp):
    	print (i)