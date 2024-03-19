import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from datetime import datetime
import re



# Faz uma busca em todos os links referenciados de forma recursiva, através da url passada
# não inclui as urls repetidas
# retorna um conjunto de links
def obterLinks(url, links_encontrados=None):
    if links_encontrados is None:
        links_encontrados = set()

    try:
        # Fazendo a solicitação HTTP
        response = requests.get(url)
        # Verificando se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Analisando o HTML da página
            soup = BeautifulSoup(response.text, 'html.parser')
            # Obtendo o domínio base da URL
            base_url = response.url
            # Adicionando a URL passada como parâmetro ao conjunto
            links_encontrados.add(base_url)
            # Encontrando todos os links na página
            links = soup.find_all('a', href=True)
            # Iterando sobre os links encontrados
            for link in links:
                # Combinando links relativos com o domínio base
                link_absoluto = urljoin(base_url, link['href'])
                # Verificando se o link absoluto já foi encontrado anteriormente
                if link_absoluto not in links_encontrados:
                    # Chamada recursiva para obter os links da página encontrada
                    obterLinks(link_absoluto, links_encontrados)
            return links_encontrados
        else:
            print("Erro ao acessar a página:", response.status_code)
    except Exception as e:
        print("Ocorreu um erro:", e)
    # Se ocorrer um erro, retorna uma lista vazia
    return []



# conta a ocorrência da palavra pesquisada
# desconsiderando as que estão dentro de links <href>
def contarOcorrencia_palavra_geral (palavra, response):
    encontradas = contarOcorrencia_palavra_todoCodigo(palavra, response)
    dentroDeLink = contarOcorrencia_palavra_href(palavra, response)
    qtd = encontradas - dentroDeLink

    if qtd < 0:
        qtd = 0
    
    return int(qtd)


# Verifica a quantidade de vezes que a palavra aparece em todo o código HTML. Não apenas no texto visível
# Recebe uma palavra e um link e retorna um número
def contarOcorrencia_palavra_todoCodigo(palavra, response):
    # Contando as ocorrências da palavra no código HTML da página
    quantidade = response.text.lower().count(palavra.lower())
    
    return int(quantidade)



# Verifica a quantidade de vezes que a palavra aparece em links na página
# Recebe uma palavra e um link e retorna um número
def contarOcorrencia_palavra_href(palavra, response):
    # Parseia o HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontra todas as tags 'a' com o atributo 'href'
    href_tags = soup.find_all('a', href=True)
    
    # Inicializa a contagem
    count = 0
    
    # Itera sobre as tags 'a' encontradas
    for tag in href_tags:
        # Obtém o valor do atributo 'href' e verifica se a palavra está presente
        href = tag['href']
        if palavra in href:
            count += 1
    
    # Retorna o resultado da contagem
    return int(count)



# Conta a quantidade de referecias que aquela página recebeu
def contar_referencias(url_referenciada, lista_de_urls):
    count = 0
    for url in lista_de_urls:
        try:
            response = requests.get(url)
            baseUrl = response.url
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    link_absoluto = urljoin(baseUrl, link['href'])
                    if url_referenciada == link_absoluto:
                        count += 1
        except Exception as e:
            print("Erro ao acessar a página", url, ":", e)
    return int(count)


#Conta quantas vezes a página faz auto referência
#Recebe uma url e retorna um valor
def contar_autoReferencias(url, response):
    count = 0
    baseUrl = response.url
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        link_absoluto = urljoin(baseUrl, link['href'])
        if url == link_absoluto:
            count += 1
    
    return int(count)



#Recebe uma página e retorna o ano que foi criada
def obter_anoDaPagina(response):      
    
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a primeira tag <p>
    primeira_tag_p = soup.find('p')

    # Verificar se a tag <p> foi encontrada e se tem conteúdo
    if primeira_tag_p and primeira_tag_p.text.strip():
        # Extrair o conteúdo da primeira tag <p>
        texto = primeira_tag_p.text.strip()
        # Procurar uma correspondência para o ano no texto usando expressões regulares
        ano_match = re.search(r'\b\d{4}\b', texto)
        if ano_match:
            return int(ano_match.group())  # Retorna o ano encontrado
        else:
            return "Ano de publicação não encontrado."
    


#Calcula o frescor da página de acordo com o ano
#Recebe uma url e retorna um valor
def calcular_frescor(penalidade_porAno, response):
    anoAtual = datetime.now().year
    anoCriacao = obter_anoDaPagina(response)
    
    pontuacao = 30
    penalizacao = 0
    
    if anoCriacao < anoAtual:
        diferenca_anos = int(anoAtual - anoCriacao)
        penalizacao = (penalidade_porAno * diferenca_anos)
    
    return int(pontuacao + penalizacao)



# Calcula a quantidade de ocorrências da palavra nas Tags <head>
# Recebe uma palavra e uma url e retorna um numero
def contar_tagHead(palavra, response):
    # Obtém o conteúdo HTML da URL
    html = response.text

    # Usa expressões regulares para encontrar o conteúdo dentro da tag <head>
    head_content = re.findall(r'<head>(.*?)</head>', html, re.DOTALL)

    # Converte a lista de strings em uma única string
    head_content = ''.join(head_content)

    # Conta o número de ocorrências da palavra
    count = head_content.lower().count(palavra.lower())

    return count



# Calcula a quantidade de ocorrências da palavra nas Tags <h1>
# Recebe uma palavra e uma url e retorna um numero
def contar_tagH1(palavra, response):
    # Obtém o conteúdo HTML da URL
    html = response.text

    # Analisa o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Obtém todas as tags <h1>
    h1_tags = soup.find_all('h1')

    # Inicializa contador
    count_h1 = 0

    # Conta o número de ocorrências da palavra nas tags <h1>
    for tag in h1_tags:
        count_h1 += tag.get_text().lower().count(palavra.lower())

    return int(count_h1)



# Calcula a quantidade de ocorrências da palavra nas Tags <h2>
# Recebe uma palavra e uma url e retorna um numero
def contar_tagH2(palavra, response):
    # Obtém o conteúdo HTML da URL
    html = response.text

    # Analisa o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Obtém todas as tags <h2>
    h2_tags = soup.find_all('h2')

    # Inicializa contador
    count_h2 = 0

    # Conta o número de ocorrências da palavra nas tags <h2>
    for tag in h2_tags:
        count_h2 += tag.get_text().lower().count(palavra.lower())

    return int(count_h2)



# Calcula a quantidade de ocorrências da palavra nas Tags <p>
# Recebe uma palavra e uma url e retorna um numero
def contar_tagP(palavra, response):
    # Obtém o conteúdo HTML da URL
    html = response.text

    # Analisa o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Obtém todas as tags <p>
    p_tags = soup.find_all('p')

    # Inicializa contador
    count_p = 0

    # Conta o número de ocorrências da palavra nas tags <p>
    for tag in p_tags:
        count_p += tag.get_text().lower().count(palavra.lower())

    return int(count_p)



# Calcula a quantidade de ocorrências da palavra nas Tags <a>
# Recebe uma palavra e uma url e retorna um numero
def contar_tagA(palavra, response):
    # Obtém o conteúdo HTML da URL
    html = response.text

    # Analisa o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Obtém todas as tags <a>
    a_tags = soup.find_all('a')

    # Inicializa contador
    count_a = 0

    # Conta o número de ocorrências da palavra nas tags <a>
    for tag in a_tags:
        count_a += tag.get_text().lower().count(palavra.lower())

    return int(count_a)



#Calcula o valor final de ocorrênciasem todas as tags
# Recebe uma palavrae uma url e retorna um valor
def contar_totalTags(palavra, url):
    # Chamando todas as funções anteriores
    ocorrencias_head = contar_tagHead(palavra, url)
    ocorrencias_h1 = contar_tagH1(palavra, url)
    ocorrencias_h2 = contar_tagH2(palavra, url)
    ocorrencias_p = contar_tagP(palavra, url)
    ocorrencias_a = contar_tagA(palavra, url)
    
    # Calculando a soma dos resultados
    total_ocorrencias = (ocorrencias_head +
                         ocorrencias_h1 +
                         ocorrencias_h2 +
                         ocorrencias_p +
                         ocorrencias_a)
    
    return total_ocorrencias



# Função que retorna o título de uma página passada por parâmetro
def obterTitulo(response):
    try:       
        # Analisando o HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        # Obtendo o título da página
        titulo = soup.title.string.strip() if soup.title else "Nenhum título encontrado"
        return titulo
    except Exception as e:
        print("Ocorreu um erro:", e)
    # Se ocorrer um erro, retorna uma string indicando que nenhum título foi encontrado
    return "Indefinido"



# imprime a logo na tela
def logo():
    print('{}                  _           ____'.format(cores['ciano']))  
    print('                 | |         (___ \ ')
    print('  ____  ____   _ | |  ____       ) )')
    print(' / ___)/ _  | / || | / _  )     /_/ ')
    print('( (___( ( | |( (_| |( (/ /      _   ')
    print(' \____)\_||_| \____| \____)    (_)  {}'.format(cores['limpa']))
    print("")
    print("")
    print("")



# limpa a tela do terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



cores = {
    'limpa':'\033[m',
    'branco':'\033[30m',
    'vermelho':'\033[31m',
    'verde':'\033[32m',
    'amarelo':'\033[33m',
    'azul':'\033[34m',
    'lilas':'\033[35m',
    'ciano':'\033[36m',
    'cinza':'\033[37m',
    'fundociano':'\033[1;46m',
    'cianoItalico':'\033[3;36m'
    }