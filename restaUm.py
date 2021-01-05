# Alunos: Gabriel Medina Braga - 2016.1905.023-4
#		  Diego Garcia Segovia - 2016.1905.018-8 
# 		  Vitor Santa Barbara Lira - 2016.1905.035-4 

import time
import math
import copy
import random

# ALGORITMO: Para resolver o jogo resta um foi utilizada uma lista de objetos No. Essa lista abstrai a arvore de possibilidades
# de jogadas para um dado estado do tabuleiro. Assim, cada elemento da lista vai conter um tabuleiro, suas jogadas com suas respectivas
# estimativas de custo (que coincidem com a funcao de avaliacao dado que a funcao de custo eh a mesma para todas jogadas) e uma lista 
# de jogadas que levaram ate aquele elemento. Assim, eh executado uma laco que verifica as jogadas do tabuleiro atual, o insere na lista
# para que seja comparado com os outros elementos da lista; o laco termina quando o numero de pontos do tabuleiro atual chegar a 1.
# --------------------------------------------------------------------------------------------------------------------------------------

# Um no eh definido pelo tabuleiro, suas jogadas, as estimativas de custo de cada jogada e as jogadas que trouxeram ateh ele
class No:
	# Metodo construtor inicializa tabuleiro do no e suas jogadas
	def __init__(self, tabuleiro, jogadas):
		self.tabuleiroNo = copy.deepcopy(tabuleiro)
		self.jogadasDoTabuleiro = copy.deepcopy(jogadas)
		self.jogadasAteAqui = [] 

	# Adiciona lista de fa de cada jogada
	def adicionaFa(self, fa):
		self.fa = copy.deepcopy(fa)

	# Adiciona lista de jogadas que trouxe ateh esse estado
	def addListaJogadas(self, jogadasParaAdicionar):
		self.jogadasAteAqui = copy.deepcopy(jogadasParaAdicionar)

def resolucao():
	# Condicao inicial do tabuleiro
	tabuleiro = [[0,0,1,1,1,0,0], 
				 [0,0,1,1,1,0,0], 
				 [1,1,1,1,1,1,1], 
				 [1,1,1,0,1,1,1], 
				 [1,1,1,1,1,1,1], 
				 [0,0,1,1,1,0,0], 
				 [0,0,1,1,1,0,0]] 
		
	nPts = 32 # Tabuleiro comeca com 32 pecas
	jogadasDoTabuleiro = [] # Lista de jogadas do estado atual do tabuleiro (lista de triplas de tuplas)
	listaNos = [] # Lista de objetos No
	#jogadasParaAdicionar = [] # Jogadas a serem adicionadas a lista de jogadas que leva a um estado

	tempo = 0
	c = 0
	nEstados = 0
	# Comecando a contar o tempo da resolucao
	inicio = time.time()
	
	# Roda ateh achar uma solucao (dentro de 30 minutos)
	while nPts > 1 and tempo <= 30:
		# Calculando jogadas para estado atual do tabuleiro
		jogadasDoTabuleiro = copy.deepcopy(calculaJogadas(tabuleiro))

		# So vai criar novo No se houver jogadas para o tabuleiro daquele No
		if len(jogadasDoTabuleiro) > 0:
			noAtual = No(tabuleiro, jogadasDoTabuleiro)
			listaNos.append(noAtual)
			
			# Exceto para o primeiro No, vamos adicionar as jogadas que levaram aquele No
			if nPts < 32:
				noAtual.addListaJogadas(j)

			nEstados += 1
								

		# A escolha da proxima jogada nos leva a um novo tabuleiro e tambem retorna as jogadas que trouxeram ate ele 
		tabuleiro,j = escolheJogada(listaNos)
		
		# Limpando jogadas atuais (para as definir as jogadas do proximo estado)
		clear(jogadasDoTabuleiro) 

		# Calculando numero de pontos do tabuleiro atual
		nPts = calculaNPts(tabuleiro)
		
		# Calculando tempo de execucao do laco (em minutos)
		fim = time.time()
		tempo = (fim - inicio) / 60

		# Devido a heuristica aplicada nao ser tao adequada ao problema, varias possibilidades tem o mesmo valor, mesmo sendo
		# piores ou melhores, fazendo com que o algoritmo dependa da sorte de escolher um caminho bom ou ruim. 
		# Assim, se o tempo passar de um 1 minuto, entao tenta de novo desde o inicio
		
		if tempo >= 1+c: # Se tempo passar de 1 minuto, entao tenta de novo desde o comeco
			c = tempo
			tabuleiro = [[0,0,1,1,1,0,0], 
				 		 [0,0,1,1,1,0,0], 
				 		 [1,1,1,1,1,1,1], 
				 		 [1,1,1,0,1,1,1], 
				 		 [1,1,1,1,1,1,1], 
				 		 [0,0,1,1,1,0,0], 
				 		 [0,0,1,1,1,0,0]] 
		
			nPts = 32 
			jogadasDoTabuleiro = [] 
			listaNos = [] 
	# fim while
	
	# Ultimo No que contem a resposta eh tratado fora do laco
	ultimoNo = No(tabuleiro, [])
	ultimoNo.addListaJogadas(j)
	
	#print "TEMPO ", tempo, " minutos"
	escreveSaida(ultimoNo)

# Para definir uma jogada, precisamos de: posicao inicial (X,Y), posicao final (X_,Y_) e peca comida (Xc,Yc)
def calculaJogadas(tabuleiro):
	jogadas = []
	vazios = [] # Lista de posicoes vazias (lista de tuplas)
	# De cada posicao em vazios, eh possivel atribuir ate 4 jogadas, assim, enquanto houver posicoes vazias vou definir jogadas
	calculaVazios(vazios, tabuleiro)

	# Laco que inicializa jogadas
	while len(vazios) > 0: # Enquanto houver posicoes vazias
		# Cada variavel serve para dizer quais jogadas sao possiveis
		posValida1 = posValida2 = posValida3 = posValida4 = True 

		X_, Y_ = vazios[0] # Pegando coordenadas da posicao vazia
		
		vazios.pop(0) # ATENCAO: pop MUDA DINAMICAMENTE OS INDICES, POR ISSO vazios.pop(0) E vazios[0] ALI EM CIMA
		

		# Para uma jogada ser possivel, eh necessario que a posicao inicial esteja dentro do tabuleiro e que a peca a ser comida exista
		# k anda nas linhas do tabuleiro
		for k in range(7):
			# Se k estiver em uma dessas linhas, verifico as colunas que estao fora do tabuleiro
			if k == 0 or k == 1 or k == 5 or k == 6:
				# j anda nas colunas do tabuleiro
				for j in range(7):

					if j == 0 or j == 1 or j == 5 or j == 6:
				 		
				 		# Entao verifica se a posicao inicial esta dentro do tabuleiro e se a peca ser comida existe

						if (X_ + 2, Y_) == (k,j) or X_ + 2 not in range(7) or tabuleiro[X_ + 2][Y_] == 0 or tabuleiro[X_+1][Y_] == 0:
							posValida1 = False

						if (X_ - 2, Y_) == (k,j) or X_ - 2 not in range(7) or tabuleiro[X_ - 2][Y_] == 0 or tabuleiro[X_-1][Y_] == 0:
							posValida2 = False

						if (X_, Y_ + 2) == (k,j) or Y_ + 2 not in range(7) or tabuleiro[X_][Y_ + 2] == 0 or tabuleiro[X_][Y_+1] == 0:
							posValida3 = False

						if (X_, Y_ - 2) == (k,j) or Y_ - 2 not in range(7) or tabuleiro[X_][Y_ - 2] == 0 or tabuleiro[X_][Y_-1] == 0:
							posValida4 = False
		
		# Se a posicao inicial de uma jogada existir, entao podemos criar uma nova jogada
		if posValida1 == True:
			jogadas.append( ( (X_ + 2,Y_), (X_,Y_), (X_+1,Y_) ) ) # (X,Y) - (X',Y') => remover ( (X+X') / 2 , (Y+Y') / 2 )  
			
		if posValida2 == True:
			jogadas.append( ( (X_ - 2,Y_), (X_,Y_), (X_-1,Y_) ) )
			
		if posValida3 == True:
			jogadas.append( ( (X_,Y_ + 2), (X_,Y_), (X_,Y_+1) ) )
			
		if posValida4 == True:
			jogadas.append( ( (X_,Y_ - 2), (X_,Y_), (X_,Y_-1) ) )

	return jogadas

# Escolhe jogada de acordo com heuristica, a executa e retorna tabuleiro modificado
def escolheJogada(listaNos):
	no = listaNos[len(listaNos) - 1]
	
	# Aplicando heuristica para no mais recente da lista	
	aplicaHeuristica(no)

	# Procurando menor fa de todos
	# Percorrendo todos nos
	for i in range(len(listaNos)): 
		noAtual = listaNos[i]

		# Define fa minimo como o fa minimo do primeiro no
		if i == 0: 
			minFa = (min(noAtual.fa), i) # Guardo em minimoFA: o minimo fa do no e o indice do no
		# Nas proximas iteracoes, comparo fa minimo do no atual com o fa minimo ate entao
		else:
			minimoAteAgora, index = minFa
			# Se o minimo atual for menor que o minimo ate agora, entao redefino minimoFa
			if min(noAtual.fa) < minimoAteAgora :
				minFa = (min(noAtual.fa), i)	

	# Apos definir menor FA, defino jogada com essa FA
	minimoFa, indexNo = minFa

	noEscolhido = listaNos[indexNo] 
	
	listaFa = copy.deepcopy(noEscolhido.fa)

	# Posicao da lista onde ocorre minimo FA (se houver mais de uma, deve ser aleatorio)	
	pos = random.choice(indicesDeMinimos(listaFa, minimoFa)) 	
	jogadaEscolhida = copy.deepcopy(noEscolhido.jogadasDoTabuleiro[pos])

	# Tabuleiro onde vai ser aplicada a jogada escolhida
	tabuleiro = copy.deepcopy(noEscolhido.tabuleiroNo)
	
	executaJogada(jogadaEscolhida, tabuleiro)

	# Removendo o que foi usado
	noEscolhido.jogadasDoTabuleiro.pop(pos)
	noEscolhido.fa.pop(pos)
	
	# Se esgotar um lista de FA's, entao retiro no de listaNos
	if len(noEscolhido.fa) == 0:
		listaNos.pop(indexNo)

	# Aux vai receber adicionar a jogada escolhida as jogadas que trouxeram ate o No que ela pertence
	aux = copy.deepcopy(noEscolhido.jogadasAteAqui)
	aux.append(jogadaEscolhida)
	
	return (tabuleiro,aux)

# Aplica heuristica que calcula funcao de avaliacao
def aplicaHeuristica(no):
	# A estimativa de custo eh igual a funcao de avaliacao de um No, e vai ser avaliada da seguinte maneira:
		# Quanto MENOS extremidades ocupadas devido aquela jogada, MELHOR
		# Quanto MENOR a distancia de Manhattan das posicoes ocupadas para o centro MELHOR

	fa = [] # Lista de funcoes de avaliacao
	tabuleiro = copy.deepcopy(no.tabuleiroNo)
	nPts = calculaNPts(tabuleiro)
	
	# Definindo heuristica para cada jogada do tabuleiro
	for i in range( len(no.jogadasDoTabuleiro) ):
		tabuleiroAux = copy.deepcopy(tabuleiro)

		jogada = copy.deepcopy(no.jogadasDoTabuleiro[i])
		inicio, destino, comida = jogada
		X,Y = inicio
		X_,Y_ = destino
		Xc,Yc = comida

		tabuleiroAux[X][Y] = 0
		tabuleiroAux[Xc][Yc] = 0
		tabuleiroAux[X_][Y_] = 1

		# Calculando numero de extremidades ocupadas do tabuleiro
		e = analisaExtremidades(tabuleiroAux) 

		# Calculando distancias das posicoes ocupadas para o centro
		d = []
		for i in range(7):
			for j in range(7):
				if tabuleiroAux[i][j] == 1:
					d.append(abs(i-3) + abs(j - 3))
				
		# Adicionando valor a lista fa (obs.: so funciona se usar aquela exponencial)
		fa.append(pow(2,max(d)) + e)
	
	# Apos inicializar toda lista fa, adiciona ela ao No
	no.adicionaFa(fa)

# Executa jogada escolhida
def executaJogada(jogadaEscolhida, tabuleiro):
	# Agora podemos executar a jogada escolhida
	inicio, destino, comida = jogadaEscolhida
	X,Y = inicio
	X_,Y_ = destino
	Xc, Yc = comida

	tabuleiro[X][Y] = 0
	tabuleiro[Xc][Yc] = 0
	tabuleiro[X_][Y_] = 1

# --------------------------------------------------------------------------------------------------------------------------------------
# Funcoes auxiliares
# Calcula posicoes vazias do estado atual do tabuleiro
def calculaVazios(vazios,tabuleiro):
	# Laco for que busca novas posicoes vazias
	for i in range(7):
			if i == 0 or i == 1 or i == 5 or i == 6:
				for j in range(2,5): # COLUNAS 2, 3 e 4
					if tabuleiro[i][j] == 0:
						vazios.append((i,j))
			else:
				for j in range(7): # COLUNAS DE 0 A 6
					
					if tabuleiro[i][j] == 0:
						vazios.append((i,j))
	# fim do laco for
# Cria arquivo de saida
def escreveSaida(ultimoNo):
	# Criando arquivo de saida
	arquivo = open("saida-resta-um.txt", "w")
	
	solucao = copy.deepcopy(ultimoNo.jogadasAteAqui)

	arquivo.write("==SOLUCAO\n")
	
	for i in range(len(solucao)-1):
		inicio, destino, comida = solucao[i]
		X,Y = inicio
		X_,Y_ = destino
		arquivo.write("(%d,%d) - (%d,%d)\n" % (X,Y,X_,Y_))

	arquivo.write("==FINAL ")
	inicio,destino,comida = solucao[i+1]
	X,Y = inicio
	X_,Y_ = destino
	arquivo.write("(%d,%d) - (%d,%d)\n" % (X,Y,X_,Y_))
	arquivo.write('\n')

	# fim do laco
	
	arquivo.close()

# Calcula quantidade de pontos na extremidades
def analisaExtremidades(tabuleiro):
	e = 0
	# Percorrendo as extremidades do tabuleiro
	
	for i in range(7):
		# Se estivermos na primeira ou ultima linha do tabuleiro
		if i == 0 or i == 6:
			for j in range(2,5):
				# Se a essa extremidade estiver ocupada, somo mais um
				if tabuleiro[i][j] == 1:
					e += 1

		# Se estivermos nestas linhas, entao vericamos a primeira e ultima coluna
		if i == 2 or i== 3 or i == 4:
			if tabuleiro[i][0] == 1:
				e += 1
			if tabuleiro[i][6] == 1:
				e += 1

	return e

# Funcoes personalizada para imprimir tabuleiro
def printTabuleiro(tabuleiro):
	print "   0  1  2  3 4   5  6"
	for i in range(7):
		if i == 0 or i == 1 or i == 5 or i == 6:
			print i,"       ",tabuleiro[i][2], tabuleiro[i][3], tabuleiro[i][4]
		else:
			print i, tabuleiro[i]

# Limpa lista passada como argumento
def clear(lista):
	while len(lista) > 0:
		lista.pop()

# Calcula numero de pontos do tabuleiro passado como argumento
def calculaNPts(tabuleiro):
	nPts = 0
	# Laco for que calcula numero de pontos 
	for i in range(7):
			if i == 0 or i == 1 or i == 5 or i == 6:
				for j in range(2,5): # COLUNAS 2, 3 e 4
					if tabuleiro[i][j] == 1:
						nPts += 1
			else:
				for j in range(7): # COLUNAS DE 0 A 6
					
					if tabuleiro[i][j] == 1:
						nPts += 1
	# fim do laco for
	return nPts

# Retorna indices da lista onde ocorre valor minimo
def indicesDeMinimos(listaFa, minimoFa):
	indices = []
	for i in range(len(listaFa)):
		if listaFa[i] == minimoFa:
			indices.append(i)
	return indices

if __name__ == '__main__':
	resolucao()