class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [['-', '-', '-'],  # inicia o tabuleiro vazio
                          ['-', '-', '-'],
                          ['-', '-', '-']]
        self.jogador = 'X'
        self.profundidade_máxima = 8  # inicia com dificuldade difícil
        self.debug = False  # inicia com modo debug desligado

    def definir_dificuldade(self, dif):
        # recebe um numero inteiro e limita a profundidade que o minimax vai percorrer na árvore
        if dif == 2:  # fácil
            self.profundidade_máxima = 2
        elif dif == 4:  # médio
            self.profundidade_máxima = 4
        elif dif == 8:  # difícil
            self.profundidade_máxima = 8

    def checarVencedor(self, jogador):
        # checa todas as possibilidades de vitória no tabuleiro e retorna true se algum jogador ganhou
        for j in range(3):
            # checa vitória vertical
            if self.tabuleiro[0][j] == jogador and self.tabuleiro[1][j] == jogador and self.tabuleiro[2][j] == jogador:
                return True

        for i in range(3):
            # checa vitória horizontal
            if self.tabuleiro[i][0] == jogador and self.tabuleiro[i][1] == jogador and self.tabuleiro[i][2] == jogador:
                return True
        # checa diagonais
        if self.tabuleiro[0][0] == jogador and self.tabuleiro[1][1] == jogador and self.tabuleiro[2][2] == jogador:
            return True

        if self.tabuleiro[0][2] == jogador and self.tabuleiro[1][1] == jogador and self.tabuleiro[2][0] == jogador:
            return True
        # retorna False se ainda não houve vencedor
        return False

    def checarEspaco(self, i, j):
        # checa se o espaço está vazio
        return self.tabuleiro[i][j] == '-'

    def checarVelha(self):
        # checa se o jogo empatou
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == '-':
                    return False
        if not self.checarVencedor('O') and not self.checarVencedor('X'):
            # checagem para saber se o tabuleiro está cheio porém algum jogador venceu
            return True

    def trocarJogador(self):
        # troca o jogador atual
        if self.jogador == 'X':
            self.jogador = 'O'
        else:
            self.jogador = 'X'

    def marcarEspaco(self, i, j, jogador):
        # marca um jogador no tabuleiro
        self.tabuleiro[i][j] = jogador

    def melhorJogada(self):
        # inicia variável baixa para ser comparada com pontuação do minimax
        melhor_pontuação = -1000
        # inicia com uma jogada impossível para ser comparada posteriormente
        jogada = (-1, -1)
        for i in range(3):
            for j in range(3):
                if self.checarEspaco(i, j):
                    self.marcarEspaco(i, j, 'O')
                    pontuaçao = self.minimax(0, False, -1000, 1000)  # avalia a pontuação da jogada
                    self.tabuleiro[i][j] = '-'
                    if self.debug:
                        # se o modo debug estiver ligado, mostra a jogada que foi feita e a respectiva pontuação
                        print(f"Posição ({i}, {j}) avaliada em {pontuaçao} pontos")
                    if pontuaçao > melhor_pontuação:  # compara a pontuação da jogada atual e a maior histórica
                        # se for maior, armazena a jogada e muda a maior ponntuação histórica
                        melhor_pontuação = pontuaçao
                        jogada = (i, j)
        if jogada != (-1, -1):  # se uma melhor jogada foi encontrada:
            self.marcarEspaco(jogada[0], jogada[1], 'O')  # marca a jogada definitivamente no tabuleiro
            if self.debug:
                # se o modo debug estiver ligado, imprime a melhor jogada encontrada e sua pontuação
                print(f"\nPosição {jogada} determinada como melhor\n")
            return True
        if self.debug:
            # se nenhuma jogada foi determinada como melhor:
            print(f"Nenhuma posição marcada\n")
        return False

    def minimax(self, profundidade, maximizando, alfa, beta):
        # pontos de parada
        # se a IA vencer:
        if self.checarVencedor('O'):
            return 10 - profundidade

        # se o jogador humano vencer:
        elif self.checarVencedor('X'):
            return profundidade - 10

        # se o jogo empatar ou a profundidade máxima for atingida:
        elif self.checarVelha() or profundidade >= self.profundidade_máxima:
            return 0

        # se for nó Max:
        if maximizando:
            # inicia a variável com pontuação baixa
            melhor_pontuação = -1000
            for i in range(3):
                for j in range(3):  # itera sobre o tabuleiro
                    if self.tabuleiro[i][j] == '-':
                        self.tabuleiro[i][j] = 'O'
                        # se for um espaço vazio, marca a posição
                        pontuação = self.minimax(profundidade + 1, False, alfa, beta)  # chama recursivamente
                        self.tabuleiro[i][j] = '-'  # esvazia a posição
                        melhor_pontuação = max(pontuação, melhor_pontuação)  # armazena a maior pontuação
                        alfa = max(alfa, melhor_pontuação)  # alfa recebe a maior pontuação
                        if alfa >= beta:  # interrompe a avaliação de ramos desnecessários
                            return melhor_pontuação
            return melhor_pontuação
        else:
            # se for nó Min:
            melhor_pontuação = 1000
            for i in range(3):
                for j in range(3):
                    if self.tabuleiro[i][j] == '-':
                        self.tabuleiro[i][j] = 'X'
                        pontuação = self.minimax(profundidade + 1, True, alfa, beta)
                        self.tabuleiro[i][j] = '-'
                        melhor_pontuação = min(pontuação, melhor_pontuação)
                        beta = min(beta, melhor_pontuação)
                        if alfa >= beta:
                            return melhor_pontuação
            return melhor_pontuação

    def coordenadasVencedor(self):
        #   checa as coordenadas do jogador vitorioso, usado na interface gráfica
        for j in range(3):
            # checa vitória vertical
            if self.tabuleiro[0][j] == self.tabuleiro[1][j] == self.tabuleiro[2][j] and self.tabuleiro[0][j] != '-':
                return (j, 0), (j, 2)

        for i in range(3):
            # checa vitória horizontal
            if self.tabuleiro[i][0] == self.tabuleiro[i][1] == self.tabuleiro[i][2] and self.tabuleiro[i][0] != '-':
                return (0, i), (2, i)

        # checa diagonais
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] and self.tabuleiro[0][0] != '-':
            return (0, 0), (2, 2)

        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] and self.tabuleiro[0][2] != '-':
            return (2, 0), (0, 2)
        return None
