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
    DURACAO_DANO,
    VELOCIDADE_SLOW,
    INTERVALO_PISCAR,
    PONTOS_POR_SEGUNDO,
    DURACAO_EFEITO,
    DURACAO_FRAME_USO,
    TAMANHO_FONTE_MATRIX,
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
    contagem_regressiva,
    criar_consumivel,
    atualizar_consumivel,
    rect_consumivel,
    desenhar_consumivel,
    desenhar_efeito_ativo,
    calcular_dificuldade,
    criar_estado_matrix,
    atualizar_matrix,
    desenhar_matrix,
    desenhar_linhas_pista,
)
from src.sprites import (
    carregar_imagens_personagem,
    carregar_imagens_dano,
    carregar_imagens_coracoes,
    carregar_imagens_obstaculos,
    carregar_consumiveis,
)
from src.dados import salvar_recorde, carregar_recorde, salvar_ranking, carregar_melhor_ranking

from assets.sons.sounds import (
    inicializar_audio,
    preparar_mixer,
    tocar_musica_fundo,
    tocar_som_dano,
    tocar_som_power_up,
)


VERDE   = (100, 220, 100)
AMARELO = (255, 220,  50)


def tela_final(tela, relogio, vitoria, pontos, recorde):
    # Exibe tela de vitória ou derrota. Retorna True para jogar novamente
    fonte_titulo  = pygame.font.SysFont(None, 68)
    fonte_media   = pygame.font.SysFont(None, 40)
    fonte_pequena = pygame.font.SysFont(None, 32)

    cor_titulo = VERDE if vitoria else (220, 60, 60)
    titulo = "200 OK: Paz Encontrada!" if vitoria else "404: Paz Não Encontrada"

    texto_titulo    = fonte_titulo.render(titulo, True, cor_titulo)
    texto_pontos    = fonte_media.render(f"Pontuação: {pontos}", True, BRANCO)
    texto_recorde   = fonte_media.render(f"Recorde: {recorde}", True, AMARELO)
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
    # Retorna dicionário com o estado zerado de uma partida
    return {
        "coluna_atual": 1,
        "frame_index": 0,
        "contador_animacao": 0,
        "virando": None,
        "timer_virar": 0,
        "pode_mover": True,
        "obstaculos": [],
        "timer_spawn": 0,
        "consumiveis": [],
        "timer_spawn_consumivel": 0,
        "vidas": 3,
        "pontos": 0,
        "timer_pontos": 0,
        "timer_dano": 0,
        "frame_dano_index": 0,
        "efeito_ativo": None, # efeito ativo: None | "cafe" | "monster" | "spotify"
        "timer_efeito": 0,
        "frame_uso": None, # frame de uso do item (flash visual breve)
        "timer_uso": 0,
    }


def executar_jogo():
    # Executa o loop principal do jogo, suportando reinício de partida
    preparar_mixer()
    pygame.init()
    inicializar_audio()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()

    frames_frente, frame_direita, frame_esquerda = carregar_imagens_personagem()
    frames_dano       = carregar_imagens_dano()
    coracao_cheio, coracao_vazio = carregar_imagens_coracoes()
    imagens_obstaculos = carregar_imagens_obstaculos()
    imagens_consumiveis = carregar_consumiveis()

    largura_sprite, altura_sprite = TAMANHO_PERSONAGEM
    y_jogador = ALTURA_TELA - altura_sprite - 40
    intervalo_animacao = FPS // FPS_ANIMACAO
    fonte_matrix = pygame.font.SysFont("courier", TAMANHO_FONTE_MATRIX)
    colunas_matrix = criar_estado_matrix()

    tocar_musica_fundo()

    jogando = True
    while jogando:
        s = _estado_inicial()
        recorde_anterior = carregar_melhor_ranking(CAMINHO_RANKING)

        if not contagem_regressiva(tela, relogio, LARGURA_TELA, ALTURA_TELA, FPS):
            break

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

            # Input
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

            # Pontuação por tempo (dobro se Monster ativo)
            s["timer_pontos"] += 1
            if s["timer_pontos"] >= FPS:
                s["timer_pontos"] = 0
                ganho = PONTOS_POR_SEGUNDO * (2 if s["efeito_ativo"] == "monster" else 1)
                s["pontos"] = calcular_pontos(s["pontos"], ganho)

            # Timer do efeito ativo
            if s["efeito_ativo"]:
                s["timer_efeito"] -= 1
                if s["timer_efeito"] <= 0:
                    s["efeito_ativo"] = None
                    s["timer_efeito"] = 0

            # Timer do frame de uso (flash visual)
            if s["timer_uso"] > 0:
                s["timer_uso"] -= 1
                if s["timer_uso"] == 0:
                    s["frame_uso"] = None

            # Animação do personagem
            em_dano = s["timer_dano"] > 0

            if s["timer_uso"] > 0 and not em_dano:
                # Flash do item coletado: mostra sprite de uso piscando
                piscar_visivel = (s["timer_uso"] // INTERVALO_PISCAR) % 2 == 0
                sprite_atual = s["frame_uso"]
            elif em_dano:
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

            # Dificuldade progressiva
            vel_obs, intervalo_spawn, intervalo_con = calcular_dificuldade(s["pontos"])

            # Obstáculos (slow durante dano)
            velocidade_atual = VELOCIDADE_SLOW if em_dano else vel_obs

            s["timer_spawn"] += 1
            if s["timer_spawn"] >= intervalo_spawn:
                s["timer_spawn"] = 0
                s["obstaculos"].append(criar_obstaculo(imagens_obstaculos))

            for obs in s["obstaculos"]:
                atualizar_obstaculo(obs, velocidade_atual)
            s["obstaculos"] = [
                obs for obs in s["obstaculos"] if obs["y"] < ALTURA_TELA + TAMANHO_OBSTACULO_MAX
            ]

            # Consumíveis: spawn em colunas livres de obstáculos próximos
            colunas_ocupadas = {
                obs["coluna"] for obs in s["obstaculos"]
                if obs["y"] > -80 and obs["y"] < 200
            }
            s["timer_spawn_consumivel"] += 1
            if s["timer_spawn_consumivel"] >= intervalo_con:
                s["timer_spawn_consumivel"] = 0
                s["consumiveis"].append(criar_consumivel(imagens_consumiveis, colunas_ocupadas))

            for con in s["consumiveis"]:
                atualizar_consumivel(con)
            s["consumiveis"] = [
                con for con in s["consumiveis"] if con["y"] < ALTURA_TELA + 80
            ]

            # Colisão com obstáculos (ignorada se Spotify ativo ou em dano)
            x_jogador = COLUNAS[s["coluna_atual"]] - largura_sprite // 2
            rect_jogador = pygame.Rect(x_jogador, y_jogador, largura_sprite, altura_sprite)

            invencivel = em_dano or s["efeito_ativo"] == "spotify"
            if not invencivel:
                colidiu = next(
                    (obs for obs in s["obstaculos"]
                     if verificar_colisao(rect_jogador, rect_obstaculo(obs))),
                    None
                )
                if colidiu:
                    s["vidas"] = tomar_dano(s["vidas"], 1)
                    s["obstaculos"].remove(colidiu)
                    s["timer_dano"] = DURACAO_DANO
                    tocar_som_dano()

            # Colisão com consumíveis
            coletou = next(
                (con for con in s["consumiveis"]
                 if verificar_colisao(rect_jogador, rect_consumivel(con))),
                None
            )
            if coletou:
                tipo = coletou["tipo"]
                s["consumiveis"].remove(coletou)
                tocar_som_power_up()
                s["frame_uso"] = imagens_consumiveis[tipo]["uso"]
                s["timer_uso"] = DURACAO_FRAME_USO

                if tipo == "cafe":
                    # Restaura 1 vida, máximo 3
                    s["vidas"] = limitar_valor(s["vidas"] + 1, 0, 3)
                else:
                    # Monster e Spotify: ativa efeito por DURACAO_EFEITO frames
                    s["efeito_ativo"] = tipo
                    s["timer_efeito"] = DURACAO_EFEITO

            if jogador_perdeu(s["vidas"]):
                rodando = False

            # Renderização
            tela.fill(PRETO)
            atualizar_matrix(colunas_matrix)
            desenhar_matrix(tela, colunas_matrix, fonte_matrix)
            desenhar_linhas_pista(tela)

            for obs in s["obstaculos"]:
                desenhar_obstaculo(tela, obs)
            for con in s["consumiveis"]:
                desenhar_consumivel(tela, con)

            if piscar_visivel:
                tela.blit(sprite_atual, (x_jogador, y_jogador))

            # Overlay e barra do efeito ativo (desenhado após sprites, antes do HUD)
            desenhar_efeito_ativo(tela, s["efeito_ativo"], s["timer_efeito"], DURACAO_EFEITO)

            desenhar_vidas(tela, s["vidas"], coracao_cheio, coracao_vazio)
            desenhar_pontuacao(tela, s["pontos"], LARGURA_TELA)
            pygame.display.flip()

        # Fim de partida
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
