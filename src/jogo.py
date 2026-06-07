import pygame
import os

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    CAMINHO_RECORDE,
    COLUNAS,
    DIR_PERSONAGEM,
    TAMANHO_PERSONAGEM,
    FPS_ANIMACAO,
    DURACAO_VIRAR,
)
from src.funcoes import limitar_valor
from src.dados import salvar_recorde, carregar_recorde


def carregar_imagens_personagem():
    """Carrega e redimensiona os sprites do personagem principal."""
    def carregar(nome):
        caminho = os.path.join(DIR_PERSONAGEM, nome)
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, TAMANHO_PERSONAGEM)

    frames_frente = [
        carregar("spritesheet-404-pne-andando-reto-frente-1.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-2.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-3.png"),
    ]
    frame_direita = carregar("spritesheet-404-pne-virando-direita-1.png")
    frame_esquerda = carregar("spritesheet-404-pne-virando-esquerda-1.png")

    return frames_frente, frame_direita, frame_esquerda


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    frames_frente, frame_direita, frame_esquerda = carregar_imagens_personagem()

    # Estado do jogador
    coluna_atual = 1  # 0=esquerda, 1=centro, 2=direita
    largura_sprite, altura_sprite = TAMANHO_PERSONAGEM
    y_jogador = ALTURA_TELA - altura_sprite - 40

    # Animação
    frame_index = 0
    contador_animacao = 0
    intervalo_animacao = FPS // FPS_ANIMACAO

    # Controle de virada
    virando = None   # "esquerda" ou "direita"
    timer_virar = 0

    # Controle para evitar input repetido enquanto tecla pressionada
    pode_mover = True

    recorde = carregar_recorde(CAMINHO_RECORDE)
    pontos = 0

    rodando = True
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

        teclas = pygame.key.get_pressed()

        # Movimento entre colunas (só registra uma vez por pressão)
        if not teclas[pygame.K_LEFT] and not teclas[pygame.K_RIGHT] \
                and not teclas[pygame.K_a] and not teclas[pygame.K_d]:
            pode_mover = True

        if pode_mover:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                coluna_atual = limitar_valor(coluna_atual - 1, 0, 2)
                virando = "esquerda"
                timer_virar = DURACAO_VIRAR
                pode_mover = False
            elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                coluna_atual = limitar_valor(coluna_atual + 1, 0, 2)
                virando = "direita"
                timer_virar = DURACAO_VIRAR
                pode_mover = False

        # Atualiza timer de virada
        if timer_virar > 0:
            timer_virar -= 1
        else:
            virando = None

        # Animação de andar (só avança quando não está virando)
        if virando is None:
            contador_animacao += 1
            if contador_animacao >= intervalo_animacao:
                contador_animacao = 0
                frame_index = (frame_index + 1) % len(frames_frente)

        # Escolhe o sprite a desenhar
        if virando == "direita":
            sprite_atual = frame_direita
        elif virando == "esquerda":
            sprite_atual = frame_esquerda
        else:
            sprite_atual = frames_frente[frame_index]

        # Posição X centralizada na coluna
        x_jogador = COLUNAS[coluna_atual] - largura_sprite // 2

        # Renderização
        tela.fill(PRETO)
        tela.blit(sprite_atual, (x_jogador, y_jogador))
        pygame.display.flip()

    pygame.quit()
