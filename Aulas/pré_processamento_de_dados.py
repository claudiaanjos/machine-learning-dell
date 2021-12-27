# -*- coding: utf-8 -*-
"""Pré-processamento de dados.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J9TOZv2XKGs37Vl-QLllCcQYDFYLpqHG

#Processamento de dados
"""

import pandas as pd

data = pd.read_table('/content/fruit_data_with_colors_miss.txt')

data

data

"""Nosso conjunto de dados tem alguns dados faltantes:
- Linha 3: um ponto de interrogação
- Linha 7: um ponto final
- Linha 8: um ponto final

### Imputando valores faltantes

Vamos ler os dados novamente, mas agora passando o parâmetro na_values, para indicar quais os dados faltantes no conjunto de dados: interrogação e ponto final como string.
Esses valores serão substituidos por NaN (Not a number).
"""

data = pd.read_table('/content/fruit_data_with_colors_miss.txt', na_values=['.','?'])

data

"""Agora vamos substituir os valores NaN por zero."""

data.fillna(0)

"""Não temos garantia que esse valor imputado (zero) está de acordo com a distribuição dos dados.

Temos variações entre as massas, ou seja, o valor de zero está distante do valor padrão das frutas.

Uma técnica é aplicar a média dos dados selecionados.
"""

data.describe()

data.fillna(data.mean())

"""Temos que na coluna do subtipo da fruta não foi utilizada a média, pois é uma string.

Uma possibilidade é usar o valor que mais se repete.
"""

data['fruit_subtype'].value_counts()

data['fruit_subtype'].value_counts().argmax()

"""Para inserir no conjunto de dados:"""

data = data.fillna(data.mean())

data.head(5)

data['fruit_subtype'] = data['fruit_subtype'].fillna(data['fruit_subtype'].value_counts().argmax())

data.head(10)

"""### Eliminação de colunas

Supondo que metades dos dados de um certa coluna, não podemos confiar na média. A média pode não representar o padrão dos dados, então podemos utilizar a abordagem de eliminar a coluna.
"""

data = pd.read_table('/content/fruit_data_with_colors_miss.txt', na_values=['.','?'])

"""Calcular o total de dados:"""

data.shape[0] #número de linhas

"""Nome das colunas e quantidade de dados faltantes:"""

data.isnull().sum()

"""Se a quantidade de dados faltantes for superior a 25%, devemos eliminar a coluna. Se for infeirior a 25% podemos manter a coluna e utilizar algumas técnica de imputação de dados.

Vamos verificar a porcentagem de dados faltantes:

"""

data.isnull().sum()/data.shape[0]*100

"""Para eliminar a coluna é só solicitar as colunas que não gostariamos eliminar. Por exemplo, queremos eliminar a coluna massa:"""

data = data[['fruit_label','fruit_name','fruit_subtype','width','height','color_score']]

data.head(3)

"""### Transformando a escala dos dados

Técnica de pré-processamento para alterar a escala dos dados, o intervalo no qual os dados está abrangendo.

A ordem de grandenza das colunas é diferente.

Vamos selecionar apenas as colunas numéricas:
"""

data = pd.read_table('fruit_data_with_colors_miss.txt',na_values=['.','?'])
data = data.fillna(data.mean())
data = data[['mass','width','height','color_score']]

data

"""Percebe-se que as escalas são diferentes:"""

data.describe()

"""Para cada coluna iremos capturar o valor que queremos transformar e subtrair do valor mínimo da coluna dividido pelo valor máximo subraído do mínimo.

(valor - min) / (max - mix)

Para aplicar essa técnica iremos utilizar o sklearn: MinMaxScaler.
"""

from sklearn.preprocessing import MinMaxScaler

mm = MinMaxScaler()

"""A função fit é muito utilizada no aprendizado de máquinas.
Essa função irá construir para cada coluna do conjuntos de dados o máximo e minímo e armazenar no mm.
"""

mm.fit(data)

"""Agora vamos retornar os dados transformados."""

data_escala = mm.transform(data)

"""Nosso conjunto de dados entre zero e um:"""

data_escala

"""### Encontrando outliers

Outliers: elemento que possui entre suas características estar fora do padrão, não são o que acontece normalmente. 
Iremos eliminar esses elementos, pois queremos que o modelo aprenda padrões.
"""

data = pd.read_table('fruit_data_with_colors_miss.txt',na_values=['.','?'])
data = data.fillna(data.mean())

macas = data[data['fruit_name'] == 'apple']

macas.describe()

"""Vamos encontrar outliers pelo desvio padrão."""

est = macas['mass'].describe()

"""Iremos utilizar a seguinte técnica para verificar outliers:
Queremos as maçãs as quais a massa é maior que a média da coluna de massa das maçãs + duas vezes o desvio padrão.


"""

macas[(macas['mass'] > est['mean'] + (est['std']) * 2)] #acima da média

macas[(macas['mass'] < est['mean'] - (est['std']) * 2)] #abaixo da média

est['mean']

est['std'] #em média as massas das frutas se afastam 11 unidades da média