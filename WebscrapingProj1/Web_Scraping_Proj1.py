###############################################################################################
# Bibliotecas e comunicar com o site
import requests
import pyodbc
import pprint
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import re
import string
import numpy as np
import seaborn as sns
import networkx as nx
from bs4 import BeautifulSoup as bfs
import plotly.express as px
import plotly.graph_objects as go

###############################################################################################
# Selecionando o conteúdo da requisição da página Web
response = requests.get('https://g1.globo.com/')
#print(response.status_code) #aqui tenho o status da conecção
content = response.content
#pprint.pprint(content) # conteúde de resposta da nossa requisição Get

site = bfs(content, 'html.parser')
#print(type(site))
#print(site.prettify())

###############################################################################################
# Criando uma lista com as notícias
lista_news = []

# 3º Vamos usar uma função para visualizar todos os highlights da página
noticias = site.findAll('div', attrs= {'class': 'feed-post-body'})

for noticia in noticias:
    
    titulo    = noticia.find('span', attrs= {'class': 'feed-post-header-chapeu'})
    #print(titulo.text)
    conteudo  = noticia.find('a', attrs= {'class': 'feed-post-link'})
    #print(Conteudo.text)
    subtitulo = noticia.find('div', attrs= {'class': 'feed-post-body-resumo'})
    #print(subtitulo.text)
    link      = noticia.find('a', attrs= {'class': 'feed-post-link'})
    #print(link['href'])
         
    if (titulo) and (conteudo) and (subtitulo) and (link):
        lista_news.append([titulo.text, conteudo.text, subtitulo.text, link['href']])
        print(titulo.text); print(conteudo.text); print(subtitulo.text); print(link['href'])

    elif (titulo) and (conteudo) and (link):
        lista_news.append([titulo.text, conteudo.text, '', link['href']])
        print(titulo.text); print(conteudo.text); print(''); print(link['href'])

    elif (titulo) and (conteudo) and (subtitulo):
        lista_news.append([titulo.text, conteudo.text, subtitulo.text, ''])
        print(titulo.text); print(conteudo.text); print(subtitulo.text); print('')

    elif (titulo) and (subtitulo) and (link):
        lista_news.append([titulo.text, '', subtitulo.text, link['href']])
        print(titulo.text); print(''); print(subtitulo.text); print(link['href'])

    elif (titulo) and (conteudo):
        lista_news.append([titulo.text, conteudo.text, '', ''])
        print(titulo.text); print(conteudo.text); print(''); print('')

    elif (titulo) and (subtitulo):
        lista_news.append([titulo.text, '', subtitulo.text, ''])
        print(titulo.text); print(''); print(subtitulo.text); print('')

    elif (titulo) and (link):
        lista_news.append([titulo.text, '', '', link['href']])
        print(titulo.text); print(''); print(''); print(link['href'])

    elif (titulo):
        lista_news.append([titulo.text, '', '', ''])
        print(titulo.text); print(''); print(''); print('')

    elif (conteudo) and (subtitulo) and (link):
        lista_news.append(['', conteudo.text, subtitulo.text, link['href']])
        print(''); print(conteudo.text); print(subtitulo.text); print(link['href'])

    elif (conteudo) and (subtitulo):
        lista_news.append(['', conteudo.text, subtitulo.text , ''])
        print(''); print(conteudo.text); print(subtitulo.text); print('')

    elif (conteudo) and (link):
        lista_news.append(['', conteudo.text, '', link['href']])
        print(''); print(conteudo.text); print(''); print(link['href'])

    elif (conteudo):
        lista_news.append(['', conteudo.text, '', ''])
        print(''); print(conteudo.text); print(''); print('')

    elif (subtitulo) and (link):
        lista_news.append(['', '', subtitulo.text, link['href']])
        print(''); print(''); print(subtitulo.text); print(link['href'])

    elif (subtitulo):
        lista_news.append(['', '', subtitulo.text, ''])
        print(''); print(''); print(subtitulo.text); print('')

    elif (link):
        lista_news.append(['', '', '', link['href']])
        print(''); print(''); print(''); print(link['href'])

    else:
        lista_news.append(['', '', '', ''])
        print(''); print(''); print(''); print('')

print(lista_news)

############################################################################################
# Criando um Data Frame com a lista das notícias para armazenar em dois tipos de bancos de dados

# Renomeando as colunas do Data Frame
dados = pd.DataFrame(lista_news, columns=['Titulo', 'Conteudo', 'Subtitulo', 'Link'])

news = pd.DataFrame(dados)
news

# Salvando o Data Frame em um arquivo .csv
news.to_csv('news_g1.csv', index=False)

# Convertendo o Data Frame em dicionário para ser gravado no Firebase
NewsFirebase = pd.DataFrame.to_dict(dados)
#############################################################################################
#Conectando com a API do Firebase

firelink = 'https://webscrappingproj1-default-rtdb.firebaseio.com/'

response2 = requests.post(f'{firelink}/NoticiasG1/.json', data= json.dumps(NewsFirebase))

pprint.pprint(response2.content)

response2.status_code

############################################################################################
# Conectando com um banco de dados SQL Server e salvando no banco

conn = pyodbc.connect(
    Driver='{SQL Server}',
    Server='Alexandre',
    Database='NoticiasG1',
    trusted_connection = 'yes'
    #uid = 'ALEXANDRE\alexa',
    #pwd = 'Windows Authentication'
)

print('Conexao bem sucedida!')

cursor = conn.cursor()

for index, linha in dados.iterrows():
    #print(index, linha)
    cursor.execute("insert into Noticias (Titulo, Conteudo, Subtitulo, Link) values(?,?,?,?)",
                   linha.Titulo, linha.Conteudo, linha.Subtitulo, linha.Link)

cursor.commit()

########################################################################################

texto = ' '.join(map(str, dados['Conteudo']))
texto
type(texto)

def contar_palavras(texto):
    # Inicializando um dicionário vazio para armazenar as contagens
    contagem_palavras = {}

    # Dividindo o texto em palavras separadas por espaços
    palavras = texto.split()

    # Iterando através de cada palavra no texto
    for palavra in palavras:
        # Removendo caracteres especiais como pontuação e converta para minúsculas
        palavra = palavra.strip(".,!?:;()[]{}'\"").lower()

        # Verificando se a palavra já está no dicionário de contagens
        if palavra in contagem_palavras:
            # Se sim, ele incrementa a contagem
            contagem_palavras[palavra] += 1
        else:
            # Se não, ele adiciona a palavra ao dicionário com uma contagem inicial de 1
            contagem_palavras[palavra] = 1

    # Retornando o dicionário de contagens
    return contagem_palavras

contagens = contar_palavras(texto)

# Exibindo as contagens
for palavra, contagem in contagens.items():
    print(f"{palavra}: {contagem}")

###########################################################################################

# Gerando um gráfico de barras com as palavras que mais se repetem
df = pd.DataFrame.from_dict(contagens, orient= 'index', columns=['contagem'])
df

df = df.sort_values(by = 'contagem', ascending=False)

sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))  # Defina o tamanho da figura (opcional)
sns.barplot(x=df.index, y=df['contagem'], palette="viridis")
plt.xticks(rotation=90)  # Rotacione os rótulos do eixo x para facilitar a leitura (opcional)
plt.xlabel("palavra")
plt.ylabel("contagem")
plt.title("Contagem de Palavras no Texto")
plt.tight_layout()

# Exiba o gráfico
plt.show()

##########################################################################################

# Criando uma lista de dicionários com a estrutura necessária para o gráfico hierárquico radial
hierarquia = []

for palavra, contagem in df.iterrows():
    hierarquia.append({'id': palavra, 'parent': '', 'value': contagem['contagem']})

# Crie o gráfico hierárquico radial com Plotly
fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=[node['id'] for node in hierarquia],
    labels=[node['id'] for node in hierarquia],
    parents=[node['parent'] for node in hierarquia],
    values=[node['value'] for node in hierarquia],
    domain=dict(column=1),
    maxdepth=2,
    insidetextorientation='radial',
    textfont_size=16
))

fig.update_layout(#grid= dict(columns=1, rows=1),
                  margin = dict(t=35, l=10, r=10, b=20), 
                  title="Gráfico Hierárquico Radial Interativo de Contagem de Palavras")
fig.show()