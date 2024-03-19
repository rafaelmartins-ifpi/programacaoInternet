from tabulate import tabulate
from functions import *


class PaginaInternet:
    def __init__(self, titulo, url, response):
        self._titulo = titulo
        self._url = url
        self._response = response
        self._pontosAutoridade = 0
        self._pontosFrequencia = 0
        self._pontosTags = 0
        self._pontosAutoreferencia = 0
        self._pontosFrescor = 0
        self._pontosTotal = 0
        self._exibir = False
    
    def incrementar_pontosFrequencia(self, pontos):
        self._pontosFrequencia += pontos
        self.incrementar_pontosTotal(pontos)
    
    def incrementar_pontosTags(self, pontos):
        self._pontosTags += pontos
        self.incrementar_pontosTotal(pontos)
    
    def set_pontosAutoridade(self, pontos):
        self._pontosAutoridade = pontos
        self.incrementar_pontosTotal(pontos)
    
    def set_pontosAutoreferencia(self, pontos):
        self._pontosAutoreferencia = pontos
        self.incrementar_pontosTotal(pontos)
    
    def set_pontosFrescor(self, pontos):
        self._pontosFrescor = pontos
        self.incrementar_pontosTotal(pontos)

    def incrementar_pontosTotal(self, pontos):
        self._pontosTotal += pontos
    
    def verificarExibicao(self):
        if self._pontosFrequencia > 0:
            self._exibir = True
    
    

class BuscadorInternet:
    def __init__(self):
        self.paginas = []

    def adicionarPagina(self, pagina):
        self.paginas.append(pagina)

    def exibirResultadoOrdenado(self):
        resultadoOrdenado = sorted(self.paginas,key=lambda x: (x._pontosTotal, x._pontosFrequencia, x._pontosFrescor, x._pontosAutoridade), reverse=True)
        print('')
        print('------------------ {} Resultados Encontrados {} -----------------'.format(cores['fundociano'], cores['limpa']))
        print('')
        print('')

        for pagina in resultadoOrdenado:
            if pagina._exibir == True:
                print('{}{}{}'.format(cores['amarelo'], pagina._titulo, cores['limpa']))
                print('{}{}{}'.format(cores['cianoItalico'], pagina._url, cores['limpa']))
                print("")
        
        print('')
        print('-' * 60)
        print('')
        print('')

    def exibirTabelaPontuacao(self):
        paginasOrdenadas = sorted(self.paginas,key=lambda x: (x._pontosTotal, x._pontosFrequencia, x._pontosFrescor, x._pontosAutoridade), reverse=True)
        headers = ["Título", "Autoridade", "Frequência do Termo", "Uso em Tags", "Autoreferência", "Frescor do Contúdo", "Total", "Exibir"]
        rows = []
        
        for pagina in paginasOrdenadas:
            rows.append([pagina._titulo, pagina._pontosAutoridade, pagina._pontosFrequencia, pagina._pontosTags, pagina._pontosAutoreferencia, pagina._pontosFrescor, pagina._pontosTotal, pagina._exibir])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        