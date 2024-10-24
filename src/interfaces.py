import pygame
import sys
from button import Button

# DEFINIÇÃO DE CONSTANTES -----------------------------------------------------------

pygame.init()
TAMANHO_JANELA = (600, 600)
TAMANHO_QUADRADO = TAMANHO_JANELA[0] // 3
LARGURA_LINHA = 15
TELA = pygame.display.set_mode(TAMANHO_JANELA)


# ------------------------------------------------------------------------------------

def desenhaLinhaVencedora(ponto_inicial, ponto_final):
    # desenha uma linha sobre o jogador vitorioso
    x1 = ponto_inicial[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    y1 = ponto_inicial[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    x2 = ponto_final[0] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    y2 = ponto_final[1] * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2
    pygame.draw.line(TELA, "#02c222", (x1, y1), (x2, y2), 5)


def desenhaTabuleiro():
    # desenha as linhas do tabuleiro
    for i in range(1, 3):
        pygame.draw.line(TELA, "white", (0, TAMANHO_QUADRADO * i), (TAMANHO_JANELA[0], TAMANHO_QUADRADO * i),
                         LARGURA_LINHA)
        pygame.draw.line(TELA, "white", (TAMANHO_QUADRADO * i, 0), (TAMANHO_QUADRADO * i, TAMANHO_JANELA[1]),
                         LARGURA_LINHA)


def desenhaJogadores(jogo):
    # itera sobre as posições do tabuleiro e desenha os jogadores
    for i in range(3):
        for j in range(3):

            if jogo.tabuleiro[i][j] == 'O':
                JOGADOR_O = getFont(115).render("O", True, "white")
                JOGADOR_RECT = JOGADOR_O.get_rect(center=(int(j * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2),
                                                          int(i * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2)))
                TELA.blit(JOGADOR_O, JOGADOR_RECT)

            elif jogo.tabuleiro[i][j] == 'X':
                JOGADOR_X = getFont(115).render("X", True, "white")
                JOGADOR_RECT = JOGADOR_X.get_rect(center=(int(j * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2),
                                                          int(i * TAMANHO_QUADRADO + TAMANHO_QUADRADO // 2)))
                TELA.blit(JOGADOR_X, JOGADOR_RECT)


def getFont(size):  # retorna a fonte no tamanho desenhado
    return pygame.font.Font("fontes/SuperPixel-m2L8j.ttf", size)


def reiniciaJogo(jogo):
    # redesenha o tabuleiro vazio
    TELA.fill("black")
    desenhaTabuleiro()
    for i in range(3):
        for j in range(3):
            jogo.tabuleiro[i][j] = '-'
    jogo.jogador = 'X'


def menuPrincipal(jogo):
    # interface gráfica do menu principal
    TELA.fill("black")
    pygame.display.set_caption("Jogo da Velha")

    while True:
        # loop do menu principal
        TEXTO_MENU = getFont(55).render("JOGO DA VELHA", True, "#5180D2")
        TEXTO_RECT = TEXTO_MENU.get_rect(center=(300, 90))

        POS_MOUSE = pygame.mouse.get_pos()

        # definição dos botões
        JOGAR_LOCAL = Button(image=None, pos=(300, 200), text_input="JOGO LOCAL", font=getFont(55),
                             base_color="white",
                             hovering_color="Gray")
        JOGAR_IA = Button(image=None, pos=(300, 300), text_input="JOGAR vs IA", font=getFont(55),
                          base_color="white",
                          hovering_color="Gray")
        OPCOES = Button(image=None, pos=(300, 400), text_input="OPÇÕES", font=getFont(55),
                        base_color="white",
                        hovering_color="Gray")
        SAIR = Button(image=None, pos=(300, 500), text_input="SAIR", font=getFont(55), base_color="#db0202",
                      hovering_color="Gray")

        TELA.blit(TEXTO_MENU, TEXTO_RECT)
        for botao in [JOGAR_IA, JOGAR_LOCAL, OPCOES, SAIR]:
            # itera sobre os botões para mudar a cor caso o mouse passe por cima
            botao.changeColor(POS_MOUSE)
            botao.update(TELA)

        for event in pygame.event.get():
            #  tratador de eventos
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if JOGAR_LOCAL.checkForInput(POS_MOUSE):
                    jogoLocal(jogo)
                if JOGAR_IA.checkForInput(POS_MOUSE):
                    jogoIA(jogo)
                if OPCOES.checkForInput(POS_MOUSE):
                    opcoes(jogo)
                if SAIR.checkForInput(POS_MOUSE):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def jogoLocal(jogo):
    # interface gráfica do jogo local
    reiniciaJogo(jogo)  # limpa o tabuleiro
    pygame.display.set_caption("Modo Local")
    rodando = True
    TELA.fill("black")
    desenhaTabuleiro()
    while True:
        for event in pygame.event.get():
            # tratador de eventos
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and rodando:
                mouseX = event.pos[0] // TAMANHO_QUADRADO
                mouseY = event.pos[1] // TAMANHO_QUADRADO
                if jogo.checarEspaco(mouseY, mouseX):
                    jogo.marcarEspaco(mouseY, mouseX, jogo.jogador)
                    if jogo.checarVencedor('X') or jogo.checarVencedor('O') or jogo.checarVelha():
                        rodando = False
                    jogo.trocarJogador()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciaJogo(jogo)
                    rodando = True
                    jogo.jogador = 'X'
                if event.key == pygame.K_TAB:
                    menuPrincipal(jogo)

        desenhaJogadores(jogo)  # desenha os jogadores após cada rodada

        if not rodando:
            # se o jogo for encerrado:
            if jogo.checarVencedor('X') or jogo.checarVencedor('O'):
                # se um dos jogadores vencer, desenha uma linha sobre o vencedor
                coordenadas = jogo.coordenadasVencedor()
                desenhaLinhaVencedora(coordenadas[0], coordenadas[1])

            POS_MOUSE = pygame.mouse.get_pos()
            # após o término do jogo, mostra um botão para reiniciar e um para voltar para o menu
            SAIR = Button(image=None, pos=(300, 460), text_input="SAIR", font=getFont(75), base_color="#db0202",
                          hovering_color="Gray")
            SAIR.update(TELA)
            REINICIAR = Button(image=None, pos=(300, 360), text_input="REINICIAR", font=getFont(75),
                               base_color="#db0202",
                               hovering_color="Gray")

            REINICIAR.update(TELA)

            for botao in [REINICIAR, SAIR]:
                # muda a cor dos botões caso o jogador passe o mouse por cima
                botao.changeColor(POS_MOUSE)
                botao.update(TELA)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SAIR.checkForInput(POS_MOUSE):
                        menuPrincipal(jogo)
                    if REINICIAR.checkForInput(POS_MOUSE):
                        reiniciaJogo(jogo)
                        rodando = True
                        jogo.jogador = 'X'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reiniciaJogo(jogo)
                        rodando = True
                        jogo.jogador = 'X'
                    if event.key == pygame.K_TAB:
                        menuPrincipal(jogo)
        pygame.display.update()


def desenhaTextoDebug():
    # desenha um texto no tabuleiro indicando que o modo debug esta ligado
    TEXTO_DEBUG = getFont(15).render("MODO DEBUG", True, "white")
    DEBUG_RECT = TEXTO_DEBUG.get_rect(center=(510, 20))
    TELA.blit(TEXTO_DEBUG, DEBUG_RECT)


def jogoIA(jogo):
    # interface gráfica do modo VS IA
    reiniciaJogo(jogo)
    pygame.display.set_caption("Modo VS IA")
    rodando = True
    TELA.fill("black")
    if jogo.debug:
        desenhaTextoDebug()
    desenhaTabuleiro()
    while True:
        # loop do jogo VS IA
        for event in pygame.event.get():
            # tratador de eventos
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and rodando:
                mouseX = event.pos[0] // TAMANHO_QUADRADO
                mouseY = event.pos[1] // TAMANHO_QUADRADO

                if jogo.checarEspaco(mouseY, mouseX):
                    jogo.marcarEspaco(mouseY, mouseX, jogo.jogador)
                    if jogo.checarVencedor('X'):
                        rodando = False
                    jogo.trocarJogador()

                    if rodando:
                        if jogo.melhorJogada():  # IA tenta marcar uma jogada
                            if jogo.checarVencedor('O'):  # se conseguir, checa se foi vitoriosa
                                # se a IA for vitoriosa, encerra o jogo
                                rodando = False
                            jogo.trocarJogador()
                    if rodando:
                        if jogo.checarVelha():
                            # checa por empate
                            rodando = False
            if event.type == pygame.KEYDOWN:
                # checa por inputs do teclado
                if event.key == pygame.K_r:
                    reiniciaJogo(jogo)
                    rodando = True
                    jogo.jogador = 'X'
                    if jogo.debug:
                        desenhaTextoDebug()
                if event.key == pygame.K_TAB:
                    menuPrincipal(jogo)
        desenhaJogadores(jogo)
        if not rodando:  # se o jogo foi encerrado:
            if jogo.checarVencedor('X') or jogo.checarVencedor('O'):  # se o jogo terminou em vitória:
                # desenha uma linha sobre o jogador vitorioso
                coordenadas = jogo.coordenadasVencedor()
                desenhaLinhaVencedora(coordenadas[0], coordenadas[1])

            POS_MOUSE = pygame.mouse.get_pos()
            SAIR = Button(image=None, pos=(300, 460), text_input="SAIR", font=getFont(75), base_color="#db0202",
                          hovering_color="Gray")
            SAIR.update(TELA)
            REINICIAR = Button(image=None, pos=(300, 360), text_input="REINICIAR", font=getFont(75),
                               base_color="#db0202",
                               hovering_color="Gray")

            REINICIAR.update(TELA)
            for botao in [REINICIAR, SAIR]:
                # muda a cor dos botões caso o jogador passe o mouse por cima
                botao.changeColor(POS_MOUSE)
                botao.update(TELA)
            for event in pygame.event.get():
                #  tratador de eventos
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SAIR.checkForInput(POS_MOUSE):
                        menuPrincipal(jogo)
                    if REINICIAR.checkForInput(POS_MOUSE):
                        reiniciaJogo(jogo)
                        rodando = True
                        jogo.jogador = 'X'
                        if jogo.debug:
                            desenhaTextoDebug()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reiniciaJogo(jogo)
                        rodando = True
                        jogo.jogador = 'X'
                        if jogo.debug:
                            desenhaTextoDebug()
                    if event.key == pygame.K_TAB:
                        menuPrincipal(jogo)
        pygame.display.update()


def opcoes(jogo):
    # interface gráfica do menu de opções
    TELA.fill("black")

    # design dos textos
    TEXTO_DIF = getFont(65).render("DIFICULDADE", True, "white")
    DIF_RECT = TEXTO_DIF.get_rect(center=(300, 90))
    TELA.blit(TEXTO_DIF, DIF_RECT)

    TEXTO_DEBUG = getFont(60).render("MODO DEBUG", True, "white")
    DEBUG_RECT = TEXTO_DEBUG.get_rect(center=(300, 440))
    TELA.blit(TEXTO_DEBUG, DEBUG_RECT)

    pygame.display.set_caption("Opções")
    while True:
        # loop do menu de opções
        POS_MOUSE = pygame.mouse.get_pos()

        FACIL = None
        MEDIO = None
        DIFICIL = None

        # checa qual dificuldade está selecionada
        # destaca o texto de acordo com a dificuldade selecionada
        if jogo.profundidade_máxima == 8:
            FACIL = Button(image=None, pos=(300, 180), text_input="FÁCIL", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            MEDIO = Button(image=None, pos=(300, 265), text_input="MÉDIO", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            DIFICIL = Button(image=None, pos=(300, 350), text_input=">DIFÍCIL", font=getFont(60), base_color="#5180D2",
                             hovering_color="Gray")

        elif jogo.profundidade_máxima == 2:
            FACIL = Button(image=None, pos=(300, 180), text_input=">FÁCIL", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            MEDIO = Button(image=None, pos=(300, 265), text_input="MÉDIO", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            DIFICIL = Button(image=None, pos=(300, 350), text_input="DIFÍCIL", font=getFont(60), base_color="#5180D2",
                             hovering_color="Gray")

        elif jogo.profundidade_máxima == 4:
            FACIL = Button(image=None, pos=(300, 180), text_input="FÁCIL", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            MEDIO = Button(image=None, pos=(300, 265), text_input=">MÉDIO", font=getFont(60), base_color="#5180D2",
                           hovering_color="Gray")

            DIFICIL = Button(image=None, pos=(300, 350), text_input="DIFÍCIL", font=getFont(60), base_color="#5180D2",
                             hovering_color="Gray")
        FACIL.update(TELA)
        MEDIO.update(TELA)
        DIFICIL.update(TELA)

        # checa se o modo debug foi selecionado
        if not jogo.debug:
            # se não tiver sido selecionado, mostra o botão para ligar
            MODO_DEBUG = Button(image=None, pos=(300, 520), text_input="LIGAR DEBUG", font=getFont(40),
                                base_color="#02c222",
                                hovering_color="Gray")
            MODO_DEBUG.update(TELA)
        else:
            # se tiver sido selecionado, mostra o botão para desligar
            MODO_DEBUG = Button(image=None, pos=(300, 520), text_input="DESLIGAR DEBUG", font=getFont(40),
                                base_color="#cf0000",
                                hovering_color="Gray")
            MODO_DEBUG.update(TELA)

        VOLTAR = Button(image=None, pos=(80, 30), text_input="<-- VOLTAR", font=getFont(20),
                        base_color="WHITE",
                        hovering_color="Gray")
        VOLTAR.update(TELA)

        for botao in [FACIL, MEDIO, DIFICIL, MODO_DEBUG, VOLTAR]:
            # muda a cor dos botões caso o jogador passe o mouse por cima
            botao.changeColor(POS_MOUSE)
            botao.update(TELA)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # se alguma dificuldade for selecionada, muda a dificuldade e chama o menu novamente para atualizar a UI
                if FACIL.checkForInput(POS_MOUSE):
                    jogo.definir_dificuldade(2)
                    opcoes(jogo)
                if MEDIO.checkForInput(POS_MOUSE):
                    jogo.definir_dificuldade(4)
                    opcoes(jogo)
                if DIFICIL.checkForInput(POS_MOUSE):
                    jogo.definir_dificuldade(8)
                    opcoes(jogo)
                if MODO_DEBUG.checkForInput(POS_MOUSE):
                    # checa se o botão de ligar/desligar modo debug foi selecionado
                    if not jogo.debug:
                        jogo.debug = True
                        opcoes(jogo)
                    else:
                        jogo.debug = False
                        opcoes(jogo)

                if VOLTAR.checkForInput(POS_MOUSE):
                    menuPrincipal(jogo)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    menuPrincipal(jogo)
        pygame.display.update()
