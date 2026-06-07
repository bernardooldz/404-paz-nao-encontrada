import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    CAMINHO_RECORDE,
    COLUNAS,
    TAMANHO_PERSONAGEM,
    FPS_ANIMACAO,
    DURACAO_VIRAR,
    TAMANHO_OBSTACULO_MAX,
    INTERVALO_SPAWN,
)
from src.funcoes import (
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    jogador_perdeu,
    criar_obstaculo,
    atualizar_obstaculo,
    rect_obstaculo,
    desenhar_obstaculo,
)
from src.sprites import carregar_imagens_personagem, carregar_imagens_obstaculos
from src.dados import salvar_recorde, carregar_recorde


def tela_game_over(tela, relogio):
    # Exibe a tela de game over e aguarda tecla para encerrar
    fonte_grande  = pygame.font.SysFont(None, 72)
    fonte_pequena = pygame.font.SysFont(None, 36)
    texto_titulo    = fonte_grande.render("404: Paz Não Encontrada", True, BRANCO)
    texto_subtitulo = fonte_pequena.render("Pressione qualquer tecla para sair", True, BRANCO)

    esperando = True
    while esperando:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
            if evento.type == pygame.KEYDOWN:
                esperando = False
        tela.fill(PRETO)
        tela.blit(texto_titulo,    texto_titulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 40)))
        tela.blit(texto_subtitulo, texto_subtitulo.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 30)))
        pygame.display.flip()


def executar_jogo():
    # Executa o loop principal do jogo
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    frames_frente, frame_direita, frame_esquerda = carregar_imagens_personagem()
    imagens_obstaculos = carregar_imagens_obstaculos()

    largura_sprite, altura_sprite = TAMANHO_PERSONAGEM
    y_jogador = ALTURA_TELA - altura_sprite - 40
    coluna_atual = 1

    frame_index = 0
    contador_animacao = 0
    intervalo_animacao = FPS // FPS_ANIMACAO
    virando = None
    timer_virar = 0
    pode_mover = True

    obstaculos = []
    timer_spawn = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    rodando = True
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False

        # Input
        teclas = pygame.key.get_pressed()
        if not (teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]
                or teclas[pygame.K_a] or teclas[pygame.K_d]):
            pode_mover = True

        if pode_mover:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                coluna_atual = limitar_valor(coluna_atual - 1, 0, 2)
                virando, timer_virar, pode_mover = "esquerda", DURACAO_VIRAR, False
            elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                coluna_atual = limitar_valor(coluna_atual + 1, 0, 2)
                virando, timer_virar, pode_mover = "direita", DURACAO_VIRAR, False

        # Animação
        if timer_virar > 0:
            timer_virar -= 1
        else:
            virando = None

        if virando is None:
            contador_animacao += 1
            if contador_animacao >= intervalo_animacao:
                contador_animacao = 0
                frame_index = (frame_index + 1) % len(frames_frente)

        if virando == "direita":
            sprite_atual = frame_direita
        elif virando == "esquerda":
            sprite_atual = frame_esquerda
        else:
            sprite_atual = frames_frente[frame_index]

        # Obstáculos
        timer_spawn += 1
        if timer_spawn >= INTERVALO_SPAWN:
            timer_spawn = 0
            obstaculos.append(criar_obstaculo(imagens_obstaculos))

        for obs in obstaculos:
            atualizar_obstaculo(obs)
        obstaculos = [obs for obs in obstaculos if obs["y"] < ALTURA_TELA + TAMANHO_OBSTACULO_MAX]

        # Colisão
        x_jogador = COLUNAS[coluna_atual] - largura_sprite // 2
        rect_jogador = pygame.Rect(x_jogador, y_jogador, largura_sprite, altura_sprite)

        colidiu = next(
            (obs for obs in obstaculos if verificar_colisao(rect_jogador, rect_obstaculo(obs))),
            None
        )
        if colidiu:
            vidas = tomar_dano(vidas, 1)
            obstaculos.remove(colidiu)

        if jogador_perdeu(vidas):
            rodando = False

        if vidas < 3 and vidas > recorde:
            recorde = vidas
            salvar_recorde(CAMINHO_RECORDE, recorde)

        # Renderização
        tela.fill(PRETO)
        for obs in obstaculos:
            desenhar_obstaculo(tela, obs)
        tela.blit(sprite_atual, (x_jogador, y_jogador))
        pygame.display.flip()

    tela_game_over(tela, relogio)
    pygame.quit()
