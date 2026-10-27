import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    # df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Interior']

    # delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()

    # Obtendo Total e o Percentual de roubos por municípios
    # Total
    total_roubos = df_roubo_veiculo['roubo_veiculo'].sum()

    # Percentual                            # O 2 faz parte do metodo round
    df_roubo_veiculo['percentual %'] = round(
        (df_roubo_veiculo['roubo_veiculo'] / total_roubos) * 100, 2
    )



    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )

    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')



try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ menos ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    # Exportando o dataframe
    df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')


# Medidas de Posição e Dispersão
try:
    print('\nCalculcando a Amplitude Total')
    # amplitude_total = maior valor - menor valor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto
    # Quanto mais próximo do maior valor, mais heterogêneos são os dados do conjunto
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo
    print(f'\nAmplitude total: {amplitude}')


except Exception as e:
    print(f'Erro ao calcular a amplitude {e}')


# Medidas de Dispersão
    
try:
    # Variância
    # É a média dos quadrados das diferenças entre cada valor e a média
    # OBS: O resultado da Variância está elevado ao Quadrado
    variancia = np.var(array_roubo_veiculo)

    # Distância entre variância e média
    # < 10% - Baixa Dispersão
    # Entre 10% e 25% - Tendência de Moderada Dispersão
    # > 25% Alta dispersão
    distancia_var_media = variancia / (media_roubo_veiculo ** 2) * 100

    # DESVIO PADRÃO
    # É a raiz quadrada da Variância. Observa-se em relação média.
    # É a normalização da variância
    # Quanto os dados se afastam da Média
    desvio_padrao = np.std(array_roubo_veiculo)


    # COEFICIENTE DE VARIAÇÃO
    # É a magnitude do desvio padrão em relação a média
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100



except Exception as e:
    print(f'Erro ao calcular medida de dispersão {e}')

# VERIFICANDO A ASSIMETRIA DA DISTRIBUIÇÃO
# Indica como os dados estão distribuídos. Para que lado tende a distribuição
try:
    # Assimetria > 1
    # Positiva Alta
    # Cauda longa à direita
    # Existem valores altos puxando a média para cima
    # A média tende a ser Maior que a Mediana

    # Assimetria entre 0.5 e 1.0
    # Assimetria Positiva Moderada
    # Cauda à direita existe porém menos acentuada
    # A média tende a ser Maior que a Mediana

    # Assimetria entre -0.5 e 0.5 (Tendência a Simetria)
    # Tendência a uma Simetria
    # Os dados tendem a estar equilibrados em torno do centro
    # A média e a mediana tendem a ter valores aproximados

    # Assimetria entre -1 e -0.5
    # Assimetria Negativa Moderada
    # Cauda existe, porém é menos acentuada
    # A mediana tende a ser Maior que a média

    # Assimetria < -1
    # Assimetria Negativa Alta
    # Cauda longa à esquerda
    # Existem valores baixos puxando a média para baixo
    # A média tende a ser menor que a Mediana

    assimetria = df_roubo_veiculo['roubo_veiculo'].skew()
    
    # CURTOSE
    # É uma medida que verifica o peso das caudas de uma distribuição
    # Indicando a importância dos valores extremos.
    # Quanto maior a curtose, maior tende a ser a influência dos extremos

    # Referência: Excesso de Curtose de Fisher

    # -0.5 a 0.5 (Aproximadamente Mesocúrtica)
    # Curtose próxima de uma distribuição normal.
    # Outliers não são comuns, mas podem ocorrer.

    # Curtose > 0.5 (LEPTOCÚRTICA)  
    # Caudas mais longas e pesadas e maior influência dos extremos
    # Poucos valores muito extremos elevando bastante a curtose
    # Outliers mais frequentes

    # Curtose < 0.5 (PLATICÚRTICA)
    # Caudas mais leves. Menor Influência dos extremos.
    # Tende a Distribuição mais achatada.
    # Outliers podem aparecer

    curtose = df_roubo_veiculo['roubo_veiculo'].kurtosis()
    
    
    print('\nAnalisando a Distribuição ')
    print(30*'-')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')


except Exception as e:
    print(f'Erro ao verificar a assimetria {e}')


# Achando os outliers
try:
    # Intervalo Interquartil
    # É a amplitude dos dados mais centrais
    # Ignora o maior e menor valor
    # Não sofre interferência dos extremos
    # Quanto mais próximo do 0, mais homogêneos são os dados centrais
    # Quanto mais próximo do q3, mais heterogêneos são os dados dos 50% mais centrais
    iqr = q3 - q1
    print(f'\nIntervalo Interquartil: {iqr}')

    # calculando os limites
    # Superior
    limite_superior = q3 + (1.5 * iqr)

    # Inferior
    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    # Filtrando os outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    # Printando os outliers menores
    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)
    

    # Filtrando os outliers maiores
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )
    
    # Printando os outliers maiores
    print('\nMunicípios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')


# SAÍDA DE DADOS
try:
    print('\n Mostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Maximo: {maximo}')
    print(f'Total de Roubos: {total_roubos}')

    print(f'\nMédia: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia:.2f}%')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')
    print(f'Variância: {variancia:.2f}')
    print(f'Distância entre Variância e Média: {distancia_var_media:.2f}%')
    print(f'Desvio Padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de Variação: {coef_variacao:.2f}%')






except Exception as e:
    print(f'\nErro ao mostrar as medidas {e}')



# Plotando Gráfico

# try:
    # print('Plotando BoxPlot')                       # biblioteca matplotlib
    # # pip install matplotlib
    # # import matplotlib.pyplot as plt
    
    # # BoxPlot
    # # Retirar os outliers - showfliers=False
    # # Mostrar a média - showmeans=True
    # plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation= 'horizontal', showmeans=True)
    # plt.show()



# except Exception as e:
#     print(f'Erro ao plotar o gráfico {e}')



try:
   # BoxPLot serve para visualizar a distribuição das medidas
   print('\nInformações de Roubos de Veículos')
   plt.figure(figsize=(18, 12))

   # Posição 01 - Boxplot
   plt.subplot(2, 2, 1)
    
   plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation= 'horizontal', showmeans=True, showfliers=True)
   plt.title('Distribuição dos dados')
   plt.xlabel('Roubo de Veículos')
#    plt.ylabel('Municípios')

    # Posição 02
   plt.subplot(2, 2, 2)
   plt.text(0.1, 0.95, f'Limite Inferior: {limite_inferior}',fontsize=12)
   plt.text(0.1, 0.90, f'Menor Valor: {minimo}',fontsize=12)
   plt.text(0.1, 0.85, f'Q1: {q1}',fontsize=12)
   plt.text(0.1, 0.80, f'Q2: {q2}',fontsize=12)
   plt.text(0.1, 0.75, f'Q3: {q3}',fontsize=12)
   plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}',fontsize=12)
   plt.text(0.1, 0.65, f'Maior Valor: {maximo}',fontsize=12)
   
   plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}',fontsize=12)
   plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}',fontsize=12)
   plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}',fontsize=12)
   plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}',fontsize=12)
   plt.text(0.1, 0.35, f'Distância {distancia}',fontsize=12)
   plt.axis('off')


   # Histograma
   plt.subplot(2, 2, 3)
   plt.hist(array_roubo_veiculo, bins=100, edgecolor='black')
   plt.axvline(media_roubo_veiculo, color='green', linewidth=1)
   plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=1)

   contagens, limites = np.histogram(array_roubo_veiculo, bins=100)

   
   print('\nFaixas de Roubos do Histograma')
   for i in range(len(contagens)):
       if contagens[i] > 0:
        print(
           f'Faixa {i+1}: '
           f'{limites[i]:.0f} até {limites[i+1]:.0f} roubos '
           f'=> {contagens[i]} Municípios'
       )
   

   

   
   # Barras | 10 - maiores valores      Posição 04
   plt.subplot(2, 2, 4)
   df_roubo_veiculo_10maiores = (
       df_roubo_veiculo_maiores
       .head(10)
       .sort_values(by='roubo_veiculo', ascending=True)
   )

   plt.bar(df_roubo_veiculo_10maiores['munic'], df_roubo_veiculo_10maiores['roubo_veiculo'], edgecolor='black')
   plt.xlabel('Municípios')
   plt.ylabel('Roubo de Veículos')
   plt.xticks(rotation= 45, ha='right')     # Rotaciona o texto
   plt.title('Top 10 - Municípios com mais roubos')


  
   plt.suptitle('Informações sobre Roubo de veículos - 2003 a 2026')
   plt.show()



except Exception as e:
    print(f'Erro ao plotar o gráfico {e}')