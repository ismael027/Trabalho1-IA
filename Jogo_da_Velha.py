from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# Começa vazio, com zero em todas posições.
# tam_tabuleiro= define o tamanho do tabuleiro 3 será um tabuleiro 3x3, 4 será um tabuleir 4x4
# estados_gerados_tatal = demonstra a quantidade total de estados gerados no algoritmo minimax durante a busca da melhor jogada
# Dificuldade = define e dificuldade do jogo e a profundidade da busca no algoritmo min-max
HUMANO = -1
COMP = +1
tabuleiro = []
tam_tabuleiro = 0
dificuldade = 0
estados_gerados_total = 0

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: Retorna um valor baseado na quantidade de peças do computador em cada linha coluna, diagonal principal e secundária usando função eval
 """


def avaliacao(estado):

    global tam_tabuleiro
    win_estado = possiveis_estados_vitoria(estado)

    evalVariablesHuman = [0 for z in range(tam_tabuleiro)]
    evalVariablesComputer = [0 for z in range(tam_tabuleiro)]

    for z in range(tam_tabuleiro):
        for w in win_estado:
            if(w.count(1) == z+1 and w.count(0) == (tam_tabuleiro - (z+1))):
                evalVariablesComputer[z] = evalVariablesComputer[z] + 1
            if(w.count(-1) == z+1 and w.count(0) == (tam_tabuleiro - (z+1))):
                evalVariablesHuman[z] = evalVariablesHuman[z] + 1
    resulthuman = 0
    resultcomputer = 0
    for z in range(tam_tabuleiro):
        resultcomputer = resultcomputer + (z+1)*(evalVariablesComputer[z])
        resulthuman = resulthuman + (z+1)*(evalVariablesHuman[z])

    return resultcomputer - resulthuman


""" fim avaliacao (estado)------------------------------------- """

"""
Funcao para gerar os possíveis estados de vitória no tabuleiro.
:parametro (estado): o estado atual do tabuleiro
:returna: lista de listas com as possiveis vitorias no estado atual
 """


def possiveis_estados_vitoria(estado):

    global tam_tabuleiro
    win_estado = []
    diagonal_principal = []
    diagonal_secundaria = []
    for line in range(tam_tabuleiro):
        winLine = []
        winColumn = []
        diagonal_principal.append(estado[line][line])
        diagonal_secundaria.append(estado[line][((tam_tabuleiro - 1) - line)])
        for column in range(tam_tabuleiro):
            winLine.append(estado[line][column])
            winColumn.append(estado[column][line])
        win_estado.append(winLine)
        win_estado.append(winColumn)
    win_estado.append(diagonal_principal)
    win_estado.append(diagonal_secundaria)

    return win_estado


""" fim possiveis_estados_vitoria (estado)------------------------------------- """


def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence.
    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se jogador vence
    """

    global tam_tabuleiro
    win_estado = possiveis_estados_vitoria(estado)

    # Se um, dentre todos os alinhamentos pertence um mesmo jogador,
    # então o jogador vence!
    if [jogador for z in range(tam_tabuleiro)] in win_estado:
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""


def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)


""" ---------------------------------------------------------- """

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""


def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0:
                celulas.append([x, y])
    return celulas


""" ---------------------------------------------------------- """

"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio
"""


def movimento_valido(x, y):
    if [x, y] in celulas_vazias(tabuleiro):
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
"""


def exec_movimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:param time_init: tempo de quando começou a o algoritmo minimax
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""


def minimax(estado, profundidade, jogador, time_init):
    if(time.time() - time_init > 300):
        print("time-out")
        exit()
    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar, 1]

    for cell in celulas_vazias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador, time_init)
        placar[3] = placar[3] + 1
        melhor.append(placar[3])
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
    return melhor


""" ---------------------------------------------------------- """

"""
Limpa o console
"""


def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""


def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    global tam_tabuleiro
    print('----------------')
    for row in estado:
        print("\n")
        print('-----'*tam_tabuleiro)
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n')
    print('-----'*tam_tabuleiro)


""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < tamanho do tabuleiro ao quadrado,
ou escolhe uma coordenada aleatória, caso a profundidade seja menor que a
dificuldade, é passado como paramentro de profundidade a variável profundidade, 
caso contrario a dificuldade.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""


def IA_vez(comp_escolha, humano_escolha):
    global tabuleiro
    global tam_tabuleiro
    global dificuldade

    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    if profundidade == (tam_tabuleiro ** 2):
        x = choice([z for z in range(tam_tabuleiro)])
        y = choice([z for z in range(tam_tabuleiro)])
    else:
        if(profundidade < dificuldade):
            move = minimax(tabuleiro, profundidade, COMP, time.time())
        else:
            move = minimax(tabuleiro, dificuldade, COMP, time.time())
        print(
            f'Foram gerados {move[3]} estados durante a busca para esse movimento')
        global estados_gerados_total
        estados_gerados_total += move[3]
        x, y = move[0], move[1]

    exec_movimento(x, y, COMP)
    time.sleep(1)


""" ---------------------------------------------------------- """


def HUMANO_vez(comp_escolha, humano_escolha):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    global tabuleiro
    global tam_tabuleiro
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    movimento = -1
    movimentos = {}
    movimentos_temp = []

    for line in range(tam_tabuleiro):
        for column in range(tam_tabuleiro):
            movimentos_temp.append([line, column])

    for z in range(len(movimentos_temp)):
        movimentos[(z+1)] = movimentos_temp[z]

    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (movimento < 1 or movimento > tam_tabuleiro**2):
        try:
            movimento = int(input(f'Use numero (1..{tam_tabuleiro**2}): '))
            coord = movimentos[movimento]
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')

    """ ---------------------------------------------------------- """


def criar_tabuleiro(tamanho):
    """
    Cria o tabueliro de acordo com o tamanho selecionado
    :param tamanho: tamanho do tabuleiro
    :return:
    """
    global tabuleiro
    tabuleiro = [[0 for y in range(tamanho)] for x in range(tamanho)]
    print(tabuleiro)


""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""


def main():
    start_time = time.time()
    limpa_console()
    humano_escolha = ''  # Pode ser X ou O
    comp_escolha = ''  # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro
    global tabuleiro
    global tam_tabuleiro
    global dificuldade
    global estados_gerados_total

    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Seleciona o tamanho do tabuleiro
    limpa_console()
    try:
        tam_tabuleiro = int(input('Insira o tamnho do tabuleiro: '))
    except:
        print('Valor inválido')
        exit()
    limpa_console()

    # Seleciona a dificuldade do jogo
    try:
        dificuldade = int(input(
            "Selecione a dificuldade:\n1 - Fácil\n2 - Normal\n"))
        if(dificuldade > 2 or dificuldade <= 0):
            exit()
    except:
        print('bye')
        exit()
    limpa_console()

    # Seta o tamanho do tabuleiro
    criar_tabuleiro(tam_tabuleiro)

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    # Infomra a quantidade total de estados visitados
    print(
        f'Duração do jogo: {(time.time() -start_time):.2f}s')

    exit()


if __name__ == '__main__':
    main()
