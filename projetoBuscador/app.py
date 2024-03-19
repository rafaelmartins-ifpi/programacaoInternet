from functions import *
from classes import *
import json


def main():

    #Lê o arquivo com as configurações e o peso para cada critério
    with open('settings.json','r') as f:
        settings = json.load(f)
    pesoAutoridade = settings['autoridade']
    pesoOcorrencia = settings['ocorrencia']
    pesoHead = int(settings['head'])
    pesoH1 = int(settings['h1'])
    pesoH2 = int(settings['h2'])
    pesoP = int(settings['p'])
    pesoA = int(settings['a'])
    penalidadeAutoreferencia = int(settings['autoReferencia'])
    penalidadePorAno = int(settings['penalidadePorAno'])
            
    # define a url inicial
    urlInicial = "https://kernel32dev.github.io/hosp-pi/matrix.html"
   
    # Verifica e agrupa o total das páginas encontradas
    listaUrls = obterLinks(urlInicial)


    # Loop para a tela principal do programa
    # Roda enquanto o usuário digita 's' ou 'sim'
    op = 's'
    while (op.lower() == 's') or (op.lower() == 'sim'):
        
        # instancia o buscadorInternet e inclui todas as páginas encontradas (5 ao total)
        buscador = BuscadorInternet()
        for url in listaUrls:
            response = requests.get(url)
            titulo = obterTitulo(response)
            pontosAutoridade = pesoAutoridade * (contar_referencias(url, listaUrls))
            pontosAutoreferencia = penalidadeAutoreferencia * (contar_autoReferencias(url, response))
            pontosFrescor = calcular_frescor(penalidadePorAno, response)

            pagina = PaginaInternet(titulo, url, response)
            pagina.set_pontosAutoridade(pontosAutoridade)
            pagina.set_pontosAutoreferencia(pontosAutoreferencia)
            pagina.set_pontosFrescor(pontosFrescor)
            
            buscador.adicionarPagina(pagina)
        
        clear()
        logo()
        print("Digite abaixo a palavra que deseja buscar")
        print("")
        print("")
        
        # rebece a palavra a ser buscada
        texto = (input('{} cade? {}  '.format(cores['fundociano'], cores['limpa'])).lower())
        palavras = texto.split()
        print("")
        print("")


        # loop para todas as páginas que estão no buscador
        for pagina in buscador.paginas:
            for palavra in palavras:
                
                # Atualiza a pontuação de cada página de acordo com a palavra inserida
                pontosFrequencia = pesoOcorrencia * contarOcorrencia_palavra_geral(palavra, pagina._response)
                pagina.incrementar_pontosFrequencia(pontosFrequencia)
                
                pontosHead = pesoHead * (contar_tagHead(palavra, pagina._response))
                pontosH1 = pesoH1 * (contar_tagH1(palavra, pagina._response))
                pontosH2 = pesoH2 * (contar_tagH2(palavra, pagina._response))
                pontosP = pesoP * (contar_tagP(palavra, pagina._response))
                pontosA = pesoA * (contar_tagA(palavra, pagina._response))

                pontosTags = pontosHead + pontosH1 + pontosH2 + pontosP + pontosA

                pagina.incrementar_pontosTags(pontosTags)
                
                pagina.verificarExibicao()
        
        
        # Exibe o resultado das Páginas Encontradas
        buscador.exibirResultadoOrdenado()
        
        #Trecho para exibir a Tabela de Pontuação
        exibitTabela = input ('Deseja Exibir Tabela de Pontuação [s/n] ? ')
                
        if (exibitTabela.lower() == 's') or (exibitTabela.lower() == 'sim'):
            print('')
            print('')
            print(' {} Tabela de Pontuação {} '.format(cores['fundociano'], cores['limpa']))
            print('')
            buscador.exibirTabelaPontuacao()
            print('')
            print('')

        
        # Deleta o buscado para não acumular a pontuação
        # caso o usuário queira refazer a pesquisa
        del buscador
        op = input('Refazer busca [s/n] ?: ')
    
    print('')
    print('{} Programa Encerrado {}  '.format(cores['fundociano'], cores['limpa']))
    print('')


main()

