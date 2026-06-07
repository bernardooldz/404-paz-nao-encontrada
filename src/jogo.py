import pygame

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    PRETO,
    BRANCO,
    CAMINHO_RECORDE,
    CAMINHO_RANKING,
    COLUNAS,
    TAMANHO_PERSONAGEM,
    FPS_ANIMACAO,
    DURACAO_VIRAR,
    TAMANHO_OBSTACULO_MAX,
    INTERVALO_SPAWN,
    DURACAO_DANO,
    VELOCIDADE_SLOW,
    VELOCIDADE_OBSTACULO,
    INTERVALO_PISCAR,
    PONTOS_POR_SEGUNDO,
)
from src.funcoes import (
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    jogador_perdeu,
    calcular_pontos,
    criar_obstaculo,
    atualizar_obstaculo,
    rect_obstaculo,
    desenhar_obstaculo,
    desenhar_vidas,
    desenhar_pontuacao,
)
from src.sprites import (
    carregar_imagens_personagem,
    carregar_imagens_dano,
    carregar_imagens_coracoes,
    carregar_imagens_obstaculos,
)
from src.dados import salvar_recorde, carregar_recorde, salvar_ranking, carregar_melhor_ranking


VERDE = (100, 220, 100)
AMARELO = (255, 220, 50)


def tela_final(tela, relogio, vitoria, pontos, recorde):
    """Exibe tela de vitória ou derrota com pontuação. Retorna True para jogar novamente."""
    fonte_titulo  = pygame.font.SysFont(None, 68)
    fonte_media   = pygame.font.SysFont(None, 40)
    fonte_pequena = pygame.font.SysFont(None, 32)

    cor_titulo = VERDE if vitoria else (220, 60, 60)
    titulo = "200 OK: Paz Encontrada!" if vitoria else "404: Paz Não Encontrada"

    texto_titulo   = fonte_titulo.render(titulo, True, cor_titulo)
    texto_pontos   = fonte_media.render(f"Pontuação: {pontos}", True, BRANCO)
    texto_recorde  = fonte_media.render(f"Recorde: {recorde}", True, AMARELO)
    texto_reiniciar = fonte_pequena.render("ESPAÇO  para  jogar novamente", True, BRANCO)
    texto_sair      = fonte_pequena.render("ESC  para  sair", True, BRANCO)

    cy = ALTURA_TELA // 2
    posicoes = [
        (texto_titulo,    cy - 100),
        (texto_pontos,    cy - 20),
        (texto_recorde,   cy + 30),
        (texto_reiniciar, cy + 90),
        (texto_sair,      cy + 130),
    ]

    esperando = True
    while esperando:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False

        tela.fill(PRETO)
        for texto, y in posicoes:
            tela.blit(texto, texto.get_rect(centerx=LARGURA_TELA // 2, top=y))
        pygame.display.flip()

    return False


def _estado_inicial():
    """Retorna um dicionário com o estado zerado de uma partida."""
    return {
        "coluna_atual": 1,
        "frame_index": 0,
        "contador_animacao": 0,
        "virando": None,
        "timer_virar": 0,
        "pode_mover": True,
        "obstaculos": [],
        "timer_spawn": 0,
        "vidas": 3,
        "pontos": 0,
        "timer_pontos": 0,
        "timer_dano": 0,
        "frame_dano_index": 0,
    }


def executar_jogo():
    """Executa o loop principal do jogo, suportando reinício de partida."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    frames_frente, frame_direita, frame_esquerda = carregar_imagens_personagem()
    frames_dano = carregar_imagens_dano()
    coracao_cheio, coracao_vazio = carregar_imagens_coracoes()
    imagens_obstaculos = carregar_imagens_obstaculos()

    largura_sprite, altura_sprite = TAMANHO_PERSONAGEM
    y_jogador = ALTURA_TELA - altura_sprite - 40
    intervalo_animacao = FPS // FPS_ANIMACAO

    jogando = True
    while jogando:
        s = _estado_inicial()
        recorde_anterior = carregar_melhor_ranking(CAMINHO_RANKING)

        rodando = True
        while rodando:
            relogio.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    jogando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False
                    jogando = False

            # --- Input ---
            teclas = pygame.key.get_pressed()
            if not (teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]
                    or teclas[pygame.K_a] or teclas[pygame.K_d]):
                s["pode_mover"] = True

            if s["pode_mover"]:
                if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                    s["coluna_atual"] = limitar_valor(s["coluna_atual"] - 1, 0, 2)
                    s["virando"], s["timer_virar"], s["pode_mover"] = "esquerda", DURACAO_VIRAR, False
                elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                    s["coluna_atual"] = limitar_valor(s["coluna_atual"] + 1, 0, 2)
                    s["virando"], s["timer_virar"], s["pode_mover"] = "direita", DURACAO_VIRAR, False

            # --- Pontuação por tempo ---
            s["timer_pontos"] += 1
            if s["timer_pontos"] >= FPS:
                s["timer_pontos"] = 0
                s["pontos"] = calcular_pontos(s["pontos"], PONTOS_POR_SEGUNDO)

            # --- Animação do personagem ---
            em_dano = s["timer_dano"] > 0

            if em_dano:
                s["timer_dano"] -= 1
                s["frame_dano_index"] = (DURACAO_DANO - s["timer_dano"]) // INTERVALO_PISCAR % 2
                sprite_atual = frames_dano[s["frame_dano_index"]]
                piscar_visivel = ((DURACAO_DANO - s["timer_dano"]) // INTERVALO_PISCAR) % 2 == 0
            else:
                if s["timer_virar"] > 0:
                    s["timer_virar"] -= 1
                else:
                    s["virando"] = None

                if s["virando"] is None:
                    s["contador_animacao"] += 1
                    if s["contador_animacao"] >= intervalo_animacao:
                        s["contador_animacao"] = 0
                        s["frame_index"] = (s["frame_index"] + 1) % len(frames_frente)

                if s["virando"] == "direita":
                    sprite_atual = frame_direita
                elif s["virando"] == "esquerda":
                    sprite_atual = frame_esquerda
                else:
                    sprite_atual = frames_frente[s["frame_index"]]

                piscar_visivel = True

            # --- Obstáculos ---
            velocidade_atual = VELOCIDADE_SLOW if em_dano else VELOCIDADE_OBSTACULO

            s["timer_spawn"] += 1
            if s["timer_spawn"] >= INTERVALO_SPAWN:
                s["timer_spawn"] = 0
                s["obstaculos"].append(criar_obstaculo(imagens_obstaculos))

            for obs in s["obstaculos"]:
                atualizar_obstaculo(obs, velocidade_atual)
            s["obstaculos"] = [
                obs for obs in s["obstaculos"] if obs["y"] < ALTURA_TELA + TAMANHO_OBSTACULO_MAX
            ]

            # --- Colisão ---
            x_jogador = COLUNAS[s["coluna_atual"]] - largura_sprite // 2
            rect_jogador = pygame.Rect(x_jogador, y_jogador, largura_sprite, altura_sprite)

            if not em_dano:
                colidiu = next(
                    (obs for obs in s["obstaculos"]
                     if verificar_colisao(rect_jogador, rect_obstaculo(obs))),
                    None
                )
                if colidiu:
                    s["vidas"] = tomar_dano(s["vidas"], 1)
                    s["obstaculos"].remove(colidiu)
                    s["timer_dano"] = DURACAO_DANO

            if jogador_perdeu(s["vidas"]):
                rodando = False

            # --- Renderização ---
            tela.fill(PRETO)
            for obs in s["obstaculos"]:
                desenhar_obstaculo(tela, obs)
            if piscar_visivel:
                tela.blit(sprite_atual, (x_jogador, y_jogador))
            desenhar_vidas(tela, s["vidas"], coracao_cheio, coracao_vazio)
            desenhar_pontuacao(tela, s["pontos"], LARGURA_TELA)
            pygame.display.flip()

        # --- Fim de partida ---
        if not jogando:
            break

        pontos_finais = s["pontos"]
        salvar_ranking(CAMINHO_RANKING, pontos_finais)

        melhor = carregar_melhor_ranking(CAMINHO_RANKING)
        vitoria = pontos_finais > recorde_anterior
        if vitoria:
            salvar_recorde(CAMINHO_RECORDE, pontos_finais)

        jogando = tela_final(tela, relogio, vitoria, pontos_finais, melhor)

    pygame.quit()
