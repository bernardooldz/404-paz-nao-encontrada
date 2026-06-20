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
from src.dados import salvar_recorde, carregar_recorde, salvar_ranking, carregar_melhor_ranking, carregar_ranking

from assets.sons.sounds import (
    audio_manager,
    inicializar_audio,
    preparar_mixer,
    tocar_som_dano,
    tocar_som_power_up,
)


VERDE   = (100, 220, 100)
AMARELO = (255, 220,  50)
CINZA   = (130, 130, 130)

# Imagens carregadas uma vez e reusadas em todas as telas
_logo         = None
_img_personagem = None
_imgs_obstaculos_deco = None
_imgs_consumiveis_deco = None
_arrastando_volume = False


def _carregar_assets_telas():
    # Carrega imagens usadas nas telas estáticas (logo, personagem, decorações)
    global _logo, _img_personagem, _imgs_obstaculos_deco, _imgs_consumiveis_deco
    import os

    logo_orig = pygame.image.load("assets/imagens/sistema/Logo-404pne-removebg-preview.png").convert_alpha()
    lw = int(LARGURA_TELA * 0.80)
    lh = int(logo_orig.get_height() * lw / logo_orig.get_width())
    _logo = pygame.transform.scale(logo_orig, (lw, lh))

    # Personagem com café na tela inicial
    ph = int(ALTURA_TELA * 0.22)
    pw = int(ph * 134 / 222)
    p = pygame.image.load("assets/imagens/sistema/spritesheet-404-pne-personagem-cafe-removebg-preview.png").convert_alpha()
    _img_personagem = pygame.transform.scale(p, (pw, ph))

    tamanho_deco = int(LARGURA_TELA * 0.07)
    _imgs_obstaculos_deco = []
    for arq in sorted(os.listdir("assets/imagens/obstaculos")):
        if arq.endswith(".png"):
            img = pygame.image.load(f"assets/imagens/obstaculos/{arq}").convert_alpha()
            _imgs_obstaculos_deco.append(pygame.transform.scale(img, (tamanho_deco, tamanho_deco)))

    tamanho_con = int(LARGURA_TELA * 0.07)
    _imgs_consumiveis_deco = []
    for arq in sorted(os.listdir("assets/imagens/consumiveis")):
        if arq.endswith(".png"):
            img = pygame.image.load(f"assets/imagens/consumiveis/{arq}").convert_alpha()
            _imgs_consumiveis_deco.append(pygame.transform.scale(img, (tamanho_con, tamanho_con)))


def _fundo(tela, colunas_matrix, fonte_matrix):
    # Desenha fundo preto + efeito matrix. Base de todas as telas estáticas
    tela.fill(PRETO)
    atualizar_matrix(colunas_matrix)
    desenhar_matrix(tela, colunas_matrix, fonte_matrix)


def _desenhar_decoracao_lateral(tela):
    # Desenha obstáculos e consumíveis como decoração nas bordas da tela inicial
    if not _imgs_obstaculos_deco or not _imgs_consumiveis_deco:
        return
    todas = _imgs_obstaculos_deco + _imgs_consumiveis_deco
    tam = todas[0].get_width()
    margem_x = int(LARGURA_TELA * 0.04)
    espacamento = int(ALTURA_TELA * 0.12)
    inicio_y = int(ALTURA_TELA * 0.30)
    for i, img in enumerate(todas):
        y = inicio_y + i * espacamento
        if y + tam > ALTURA_TELA - 40:
            break
        # Alterna entre coluna esquerda e direita
        if i % 2 == 0:
            tela.blit(img, (margem_x, y))
        else:
            tela.blit(img, (LARGURA_TELA - margem_x - tam, y))


def _retangulos_controle_volume():
    slider_largura = max(90, int(LARGURA_TELA * 0.15))
    slider_altura = 8
    icon_tamanho = 28
    margem_x = 20
    margem_y = 4
    espaco = 8
    y_centro = margem_y + icon_tamanho // 2
    slider = pygame.Rect(
        LARGURA_TELA - margem_x - slider_largura,
        y_centro - slider_altura // 2,
        slider_largura,
        slider_altura,
    )
    icone = pygame.Rect(slider.left - espaco - icon_tamanho, margem_y, icon_tamanho, icon_tamanho)
    area_slider = slider.inflate(12, 22)
    return icone, slider, area_slider


def _definir_volume_pelo_mouse(x_mouse):
    _, slider, _ = _retangulos_controle_volume()
    proporcao = (x_mouse - slider.left) / slider.width
    audio_manager.set_master_volume(proporcao)


def _processar_evento_controle_volume(evento):
    global _arrastando_volume

    icone, _, area_slider = _retangulos_controle_volume()
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if icone.collidepoint(evento.pos):
            audio_manager.toggle_mute()
            return True
        if area_slider.collidepoint(evento.pos):
            _arrastando_volume = True
            _definir_volume_pelo_mouse(evento.pos[0])
            return True

    if evento.type == pygame.MOUSEMOTION and _arrastando_volume:
        _definir_volume_pelo_mouse(evento.pos[0])
        return True

    if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
        _arrastando_volume = False

    return False


def _desenhar_icone_volume(tela, rect, ativo):
    cor = VERDE if ativo else (210, 70, 70)
    x, y = rect.topleft
    corpo = pygame.Rect(x + 3, y + 10, 7, 9)
    pygame.draw.rect(tela, cor, corpo)
    pygame.draw.polygon(tela, cor, [
        (x + 10, y + 9),
        (x + 18, y + 4),
        (x + 18, y + 24),
        (x + 10, y + 19),
    ])

    if ativo:
        pygame.draw.arc(tela, cor, (x + 14, y + 8, 12, 12), -0.9, 0.9, 2)
        pygame.draw.arc(tela, cor, (x + 11, y + 4, 20, 20), -0.8, 0.8, 2)
    else:
        pygame.draw.line(tela, cor, (x + 21, y + 9), (x + 27, y + 19), 3)
        pygame.draw.line(tela, cor, (x + 27, y + 9), (x + 21, y + 19), 3)


def _desenhar_controle_volume(tela):
    icone, slider, _ = _retangulos_controle_volume()
    ativo = not audio_manager.is_muted
    volume = audio_manager.master_music_volume

    painel = pygame.Surface((icone.width + 8 + slider.width + 14, 38), pygame.SRCALPHA)
    painel.fill((0, 0, 0, 145))
    tela.blit(painel, (icone.left - 7, 1))

    _desenhar_icone_volume(tela, icone, ativo)

    pygame.draw.rect(tela, (60, 60, 60), slider, border_radius=4)
    preenchimento = pygame.Rect(slider.left, slider.top, int(slider.width * volume), slider.height)
    if preenchimento.width > 0:
        pygame.draw.rect(tela, VERDE if ativo else CINZA, preenchimento, border_radius=4)

    x_botao = slider.left + int(slider.width * volume)
    pygame.draw.circle(tela, BRANCO, (x_botao, slider.centery), 7)
    pygame.draw.circle(tela, (30, 30, 30), (x_botao, slider.centery), 7, 1)


def tela_tutorial(tela, relogio, colunas_matrix, fonte_matrix):
    # Tutorial multi-etapa. Seta direita / SPACE avanca, seta esquerda volta, ESC sai.
    cx = LARGURA_TELA // 2
    f_titulo  = pygame.font.SysFont(None, int(ALTURA_TELA * 0.058))
    f_texto   = pygame.font.SysFont(None, int(ALTURA_TELA * 0.036))
    f_detalhe = pygame.font.SysFont(None, int(ALTURA_TELA * 0.030))
    f_nav     = pygame.font.SysFont(None, int(ALTURA_TELA * 0.030))

    tam_img   = int(LARGURA_TELA * 0.13)
    tam_char  = int(ALTURA_TELA  * 0.20)

    def escalar(caminho, h=None, w=None):
        img = pygame.image.load(caminho).convert_alpha()
        ow, oh = img.get_size()
        if h:
            return pygame.transform.scale(img, (int(ow * h / oh), h))
        if w:
            return pygame.transform.scale(img, (w, int(oh * w / ow)))
        return img

    # Pre-carrega imagens usadas no tutorial
    char_normal  = escalar("assets/imagens/personagem-principal/spritesheet-404-pne-andando-reto-frente-1.png", h=tam_char)
    char_dano    = escalar("assets/imagens/sistema/spritesheet-404-pne-personagem-sofrendo-dano-removebg-preview.png", h=tam_char)
    char_cafe    = escalar("assets/imagens/sistema/spritesheet-404-pne-personagem-cafe-removebg-preview.png", h=tam_char)
    char_monster = escalar("assets/imagens/sistema/spritesheet-404-pne-personagem-monster-removebg-preview.png", h=tam_char)
    char_spotify = escalar("assets/imagens/sistema/spritesheet-404-pne-personagem-spotify-removebg-preview.png", h=tam_char)

    item_cafe    = escalar("assets/imagens/consumiveis/spritesheet-404-pne-consumiveis-_-dano-cafe.png",    w=tam_img)
    item_monster = escalar("assets/imagens/consumiveis/spritesheet-404-pne-consumiveis-_-dano-monster.png", w=tam_img)
    item_spotify = escalar("assets/imagens/consumiveis/spritesheet-404-pne-consumiveis-_-dano-spotify.png", w=tam_img)

    obs_imgs = []
    import os
    for arq in sorted(os.listdir("assets/imagens/obstaculos")):
        if arq.endswith(".png"):
            obs_imgs.append(escalar(f"assets/imagens/obstaculos/{arq}", w=tam_img))

    coracao = escalar("assets/imagens/sistema/spritesheet-404-pne-consumiveis-&-dano-coracao-cheio.png", w=int(tam_img * 0.55))

    # Cada etapa: (titulo, [(imagem, x_rel, y_rel), ...], [(linha_texto, cor), ...])
    # x_rel e y_rel sao proporcoes de LARGURA/ALTURA_TELA
    etapas = [
        {
            "titulo": "Bem-vindo ao 404: Paz Não Encontrada!",
            "imagens": [(char_normal, 0.5, 0.32)],
            "linhas": [
                ("Você é um dev tentando encontrar paz", BRANCO),
                ("após um longo dia de trabalho.", BRANCO),
                ("", BRANCO),
                ("Use  <- / ->  ou  A / D  para se mover", VERDE),
                ("entre as 3 pistas e desviar dos obstáculos.", VERDE),
            ],
        },
        {
            "titulo": "Obstáculos — evite a todo custo!",
            "imagens": [(img, 0.15 + i * 0.175, 0.30) for i, img in enumerate(obs_imgs[:5])],
            "linhas": [
                ("Bugs, conflitos de merge, código legado,", BRANCO),
                ("dependências quebradas e notificações do Slack", BRANCO),
                ("vêm descendo em sua direção.", BRANCO),
                ("", BRANCO),
                ("Cada colisão remove 1 vida.", (220, 80, 80)),
                ("Você começa com 3 vidas.", (220, 80, 80)),
            ],
        },
        {
            "titulo": "Vidas e dano",
            "imagens": [(char_dano, 0.5, 0.28)],
            "linhas": [
                ("Ao ser atingido, o personagem pisca", BRANCO),
                ("e os obstáculos ficam mais lentos por 2s.", BRANCO),
                ("", BRANCO),
                ("Durante esse tempo você é invencível!", VERDE),
                ("", BRANCO),
                ("Se as 3 vidas acabarem... game over.", (220, 80, 80)),
            ],
        },
        {
            "titulo": "Itens especiais",
            "layout": "itens",
            "fileiras": [
                (item_cafe, char_cafe, "Cafe -> restaura 1 vida", (255, 200, 80)),
                (item_monster, char_monster, "2x pontos por 5s", (80, 220, 80)),
                (item_spotify, char_spotify, "Invencivel por 5s", (160, 80, 220)),
            ],
        },
        {
            "titulo": "Pontuação e vitória",
            "imagens": [(char_cafe, 0.5, 0.30)],
            "linhas": [
                ("Você ganha 10 pontos por segundo.", BRANCO),
                ("Monster dobra esse valor.", (80, 220, 80)),
                ("", BRANCO),
                ("Supere seu recorde anterior", AMARELO),
                ("para ver a mensagem de vitória:", AMARELO),
                ("\"200 OK: Paz Encontrada!\"", VERDE),
            ],
        },
    ]

    etapa_atual = 0
    total = len(etapas)
    pode_navegar = True

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            _processar_evento_controle_volume(evento)
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_SPACE):
                    if etapa_atual < total - 1:
                        etapa_atual += 1
                    else:
                        return True  # terminou tutorial, volta para tela inicial
                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    etapa_atual = max(0, etapa_atual - 1)
                elif evento.key == pygame.K_ESCAPE:
                    return True

        etapa = etapas[etapa_atual]
        _fundo(tela, colunas_matrix, fonte_matrix)

        # Painel central
        painel = pygame.Surface((int(LARGURA_TELA * 0.92), int(ALTURA_TELA * 0.90)), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 190))
        tela.blit(painel, painel.get_rect(center=(cx, ALTURA_TELA // 2)))

        # Titulo
        txt_tit = f_titulo.render(etapa["titulo"], True, VERDE)
        tela.blit(txt_tit, txt_tit.get_rect(centerx=cx, top=int(ALTURA_TELA * 0.05)))

        # Linha divisora
        pygame.draw.line(tela, (0, 120, 0),
                         (int(LARGURA_TELA * 0.08), int(ALTURA_TELA * 0.14)),
                         (int(LARGURA_TELA * 0.92), int(ALTURA_TELA * 0.14)), 1)

        # Layout especial para etapa de itens: cada linha eh uma fileira item+char+texto
        if etapa.get("layout") == "itens":
            fileiras = etapa["fileiras"]
            n = len(fileiras)
            y_inicio = int(ALTURA_TELA * 0.20)
            espaco_fileira = int((ALTURA_TELA * 0.68) / n)
            for i, (img_item, img_char, texto, cor) in enumerate(fileiras):
                cy_row = y_inicio + i * espaco_fileira + espaco_fileira // 2
                # Item na esquerda
                tela.blit(img_item, img_item.get_rect(centerx=int(LARGURA_TELA * 0.20), centery=cy_row))
                # Personagem no centro
                tela.blit(img_char, img_char.get_rect(centerx=int(LARGURA_TELA * 0.48), centery=cy_row))
                # Texto na direita
                surf = f_texto.render(texto, True, cor)
                tela.blit(surf, surf.get_rect(left=int(LARGURA_TELA * 0.62), centery=cy_row))
                # Linha separadora entre fileiras
                if i < n - 1:
                    y_sep = y_inicio + (i + 1) * espaco_fileira
                    pygame.draw.line(tela, (0, 60, 0),
                                     (int(LARGURA_TELA * 0.10), y_sep),
                                     (int(LARGURA_TELA * 0.90), y_sep), 1)
        else:
            # Layout padrao: imagens no topo, texto embaixo
            for img, xr, yr in etapa["imagens"]:
                tela.blit(img, img.get_rect(centerx=int(LARGURA_TELA * xr), centery=int(ALTURA_TELA * yr)))

            y_texto = int(ALTURA_TELA * 0.58)
            for linha, cor in etapa["linhas"]:
                if linha:
                    surf = f_texto.render(linha, True, cor)
                    tela.blit(surf, surf.get_rect(centerx=cx, top=y_texto))
                y_texto += int(ALTURA_TELA * 0.048)

        # Indicador de etapa (bolinhas)
        raio = int(LARGURA_TELA * 0.012)
        espaco = raio * 3
        x_dot = cx - (total - 1) * espaco // 2
        y_dot = int(ALTURA_TELA * 0.91)
        for i in range(total):
            cor_dot = VERDE if i == etapa_atual else (60, 60, 60)
            pygame.draw.circle(tela, cor_dot, (x_dot + i * espaco, y_dot), raio)

        # Navegacao
        nav = "ESC / <- voltar" if etapa_atual > 0 else "ESC  para fechar"
        avancar = "SPACE / -> proximo" if etapa_atual < total - 1 else "SPACE / -> fechar tutorial"
        tela.blit(f_nav.render(nav,     True, CINZA), (int(LARGURA_TELA * 0.08), int(ALTURA_TELA * 0.94)))
        txt_av = f_nav.render(avancar, True, CINZA)
        tela.blit(txt_av, txt_av.get_rect(right=int(LARGURA_TELA * 0.92), top=int(ALTURA_TELA * 0.94)))

        _desenhar_controle_volume(tela)
        pygame.display.flip()


def tela_historico(tela, relogio, colunas_matrix, fonte_matrix):
    # Exibe lista de pontuacoes com fundo Matrix
    fonte_titulo  = pygame.font.SysFont(None, int(ALTURA_TELA * 0.06))
    fonte_recorde = pygame.font.SysFont(None, int(ALTURA_TELA * 0.045))
    fonte_item    = pygame.font.SysFont(None, int(ALTURA_TELA * 0.038))

    pontuacoes = carregar_ranking(CAMINHO_RANKING)
    pontuacoes_exibidas = pontuacoes[:10]
    recorde    = max(pontuacoes, default=0)
    cx = LARGURA_TELA // 2

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            _processar_evento_controle_volume(evento)
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_h):
                    return True

        _fundo(tela, colunas_matrix, fonte_matrix)

        # Overlay escuro central para legibilidade
        painel = pygame.Surface((int(LARGURA_TELA * 0.80), int(ALTURA_TELA * 0.82)), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 180))
        tela.blit(painel, painel.get_rect(center=(cx, ALTURA_TELA // 2)))

        y = int(ALTURA_TELA * 0.08)
        tela.blit(fonte_titulo.render("Histórico", True, VERDE),
                  fonte_titulo.render("Histórico", True, VERDE).get_rect(centerx=cx, top=y))

        y += int(ALTURA_TELA * 0.09)
        tela.blit(fonte_recorde.render(f"Recorde: {recorde} pts", True, AMARELO),
                  fonte_recorde.render(f"Recorde: {recorde} pts", True, AMARELO).get_rect(centerx=cx, top=y))

        y += int(ALTURA_TELA * 0.06)
        pygame.draw.line(tela, (0, 100, 0), (int(LARGURA_TELA * 0.15), y), (int(LARGURA_TELA * 0.85), y), 1)
        y += int(ALTURA_TELA * 0.02)

        if not pontuacoes_exibidas:
            tela.blit(fonte_item.render("Nenhuma partida registrada ainda.", True, CINZA),
                      fonte_item.render("Nenhuma partida registrada ainda.", True, CINZA).get_rect(centerx=cx, top=y))
        else:
            passo = int(ALTURA_TELA * 0.05)
            for i, pts in enumerate(pontuacoes_exibidas, start=1):
                cor = AMARELO if pts == recorde and i == 1 else BRANCO
                txt = fonte_item.render(f"{i:>2}.   {pts} pts", True, cor)
                tela.blit(txt, txt.get_rect(centerx=cx, top=y))
                y += passo
                if y > ALTURA_TELA - int(ALTURA_TELA * 0.10):
                    break

        txt_v = fonte_item.render("H / ESC  para  voltar", True, CINZA)
        tela.blit(txt_v, txt_v.get_rect(centerx=cx, bottom=ALTURA_TELA - int(ALTURA_TELA * 0.03)))
        _desenhar_controle_volume(tela)
        pygame.display.flip()


def tela_inicial(tela, relogio, colunas_matrix, fonte_matrix):
    # Tela de entrada com logo, personagem, decoracoes e fundo Matrix
    fonte_recorde = pygame.font.SysFont(None, int(ALTURA_TELA * 0.042))
    fonte_acao    = pygame.font.SysFont(None, int(ALTURA_TELA * 0.048))
    fonte_pequena = pygame.font.SysFont(None, int(ALTURA_TELA * 0.034))
    cx = LARGURA_TELA // 2

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            _processar_evento_controle_volume(evento)
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key == pygame.K_h:
                    if not tela_historico(tela, relogio, colunas_matrix, fonte_matrix):
                        return False
                if evento.key == pygame.K_t:
                    if not tela_tutorial(tela, relogio, colunas_matrix, fonte_matrix):
                        return False

        recorde = carregar_melhor_ranking(CAMINHO_RANKING)
        _fundo(tela, colunas_matrix, fonte_matrix)
        _desenhar_decoracao_lateral(tela)

        # Logo no topo
        y_logo = int(ALTURA_TELA * 0.06)
        if _logo:
            tela.blit(_logo, _logo.get_rect(centerx=cx, top=y_logo))
            y_apos_logo = y_logo + _logo.get_height() + int(ALTURA_TELA * 0.03)
        else:
            y_apos_logo = int(ALTURA_TELA * 0.20)

        # Personagem centralizado
        if _img_personagem:
            tela.blit(_img_personagem, _img_personagem.get_rect(centerx=cx, top=y_apos_logo))
            y_apos_char = y_apos_logo + _img_personagem.get_height() + int(ALTURA_TELA * 0.03)
        else:
            y_apos_char = y_apos_logo + int(ALTURA_TELA * 0.10)

        # Linha divisora
        pygame.draw.line(tela, (0, 120, 0), (int(LARGURA_TELA * 0.15), y_apos_char),
                         (int(LARGURA_TELA * 0.85), y_apos_char), 1)
        y = y_apos_char + int(ALTURA_TELA * 0.04)

        # Recorde
        txt_rec = fonte_recorde.render(
            f"Recorde: {recorde} pts" if recorde else "Nenhum recorde ainda!", True, AMARELO)
        tela.blit(txt_rec, txt_rec.get_rect(centerx=cx, top=y))
        y += int(ALTURA_TELA * 0.07)

        # Controles
        for texto, cor in [
            ("ESPACO  para  jogar",    VERDE),
            ("T  para  tutorial",       CINZA),
            ("H  para  historico",      CINZA),
            ("ESC  para  sair",         CINZA),
        ]:
            t = fonte_acao.render(texto, True, cor) if cor == VERDE else fonte_pequena.render(texto, True, cor)
            tela.blit(t, t.get_rect(centerx=cx, top=y))
            y += int(ALTURA_TELA * 0.055)

        _desenhar_controle_volume(tela)
        pygame.display.flip()


def tela_pausada(tela, relogio, colunas_matrix, fonte_matrix):
    # Overlay de pausa sobre o jogo congelado
    fonte_titulo  = pygame.font.SysFont(None, int(ALTURA_TELA * 0.07))
    fonte_pequena = pygame.font.SysFont(None, int(ALTURA_TELA * 0.04))
    cx = LARGURA_TELA // 2
    cy = ALTURA_TELA // 2

    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))

    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            _processar_evento_controle_volume(evento)
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False

        tela.blit(overlay, (0, 0))
        for texto, y in [
            (fonte_titulo.render("PAUSADO",               True, BRANCO),        cy - int(ALTURA_TELA * 0.07)),
            (fonte_pequena.render("ESPAÇO  para  retomar", True, VERDE),         cy + int(ALTURA_TELA * 0.02)),
            (fonte_pequena.render("ESC  para  sair",        True, (200, 80, 80)), cy + int(ALTURA_TELA * 0.07)),
        ]:
            tela.blit(texto, texto.get_rect(centerx=cx, top=y))
        _desenhar_controle_volume(tela)
        pygame.display.flip()


def tela_final(tela, relogio, vitoria, pontos, recorde, colunas_matrix, fonte_matrix):
    # Tela de fim de partida com fundo Matrix
    fonte_titulo  = pygame.font.SysFont(None, int(ALTURA_TELA * 0.072))
    fonte_media   = pygame.font.SysFont(None, int(ALTURA_TELA * 0.048))
    fonte_pequena = pygame.font.SysFont(None, int(ALTURA_TELA * 0.038))
    cx = LARGURA_TELA // 2
    cy = ALTURA_TELA // 2

    cor_titulo = VERDE if vitoria else (220, 60, 60)
    titulo = "200 OK: Paz Encontrada!" if vitoria else "404: Paz Não Encontrada"

    esperando = True
    while esperando:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            _processar_evento_controle_volume(evento)
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return True
                if evento.key == pygame.K_ESCAPE:
                    return False

        _fundo(tela, colunas_matrix, fonte_matrix)

        # Painel semitransparente central
        painel = pygame.Surface((int(LARGURA_TELA * 0.86), int(ALTURA_TELA * 0.60)), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 185))
        tela.blit(painel, painel.get_rect(center=(cx, cy)))

        for texto, y in [
            (fonte_titulo.render(titulo,                        True, cor_titulo),  cy - int(ALTURA_TELA * 0.22)),
            (fonte_media.render(f"Pontuação: {pontos}",         True, BRANCO),      cy - int(ALTURA_TELA * 0.10)),
            (fonte_media.render(f"Recorde: {recorde}",          True, AMARELO),     cy - int(ALTURA_TELA * 0.03)),
            (fonte_pequena.render("ESPAÇO  para  jogar novamente", True, VERDE),       cy + int(ALTURA_TELA * 0.08)),
            (fonte_pequena.render("ESC  para  sair",               True, CINZA),       cy + int(ALTURA_TELA * 0.14)),
        ]:
            tela.blit(texto, texto.get_rect(centerx=cx, top=y))

        _desenhar_controle_volume(tela)
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

    # Calcula janela baseada na area utilizavel do desktop (desconta barra de tarefas)
    info = pygame.display.Info()
    tamanhos = pygame.display.get_desktop_sizes()
    largura_desktop = tamanhos[0][0] if tamanhos else info.current_w
    altura_desktop  = tamanhos[0][1] if tamanhos else info.current_h
    # Usa 92% da altura disponivel para garantir que a janela nao saia da tela
    _altura  = int(altura_desktop * 0.92)
    _largura = int(_altura * 750 / 900)
    # Garante que a largura tambem cabe no desktop
    if _largura > largura_desktop * 0.95:
        _largura = int(largura_desktop * 0.95)
        _altura  = int(_largura * 900 / 750)
    import src.config as _cfg
    import src.funcoes as _fn
    _cfg.LARGURA_TELA = _largura
    _cfg.ALTURA_TELA  = _altura
    _cfg.COLUNAS      = [_cfg.LARGURA_TELA // 6, _cfg.LARGURA_TELA // 2, 5 * _cfg.LARGURA_TELA // 6]
    _cfg.X_LINHAS_PISTA = [0, _cfg.LARGURA_TELA // 3, 2 * _cfg.LARGURA_TELA // 3, _cfg.LARGURA_TELA - 1]
    _fn.LARGURA_TELA   = _cfg.LARGURA_TELA
    _fn.ALTURA_TELA    = _cfg.ALTURA_TELA
    _fn.COLUNAS        = _cfg.COLUNAS
    _fn.X_LINHAS_PISTA = _cfg.X_LINHAS_PISTA
    global LARGURA_TELA, ALTURA_TELA, COLUNAS
    LARGURA_TELA = _cfg.LARGURA_TELA
    ALTURA_TELA  = _cfg.ALTURA_TELA
    COLUNAS      = _cfg.COLUNAS

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
    _carregar_assets_telas()

    audio_manager.play_menu_music()

    if not tela_inicial(tela, relogio, colunas_matrix, fonte_matrix):
        audio_manager.stop_all()
        pygame.quit()
        return

    jogando = True
    while jogando:
        s = _estado_inicial()
        recorde_anterior = carregar_melhor_ranking(CAMINHO_RANKING)

        audio_manager.play_game_music(restart=True)
        if not contagem_regressiva(tela, relogio, LARGURA_TELA, ALTURA_TELA, FPS):
            break

        rodando = True
        pausado = False
        while rodando:
            relogio.tick(FPS)

            for evento in pygame.event.get():
                _processar_evento_controle_volume(evento)
                if evento.type == pygame.QUIT:
                    rodando = False
                    jogando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        rodando = False
                        jogando = False
                    elif evento.key == pygame.K_SPACE:
                        audio_manager.enter_pause()
                        pausado = True

            if pausado:
                if not tela_pausada(tela, relogio, colunas_matrix, fonte_matrix):
                    audio_manager.stop_all()
                    rodando = False
                    jogando = False
                else:
                    audio_manager.resume_after_pause()
                pausado = False
                continue

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
            _desenhar_controle_volume(tela)
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

        if vitoria:
            audio_manager.play_victory_music()
        else:
            audio_manager.play_defeat_music()
        jogando = tela_final(tela, relogio, vitoria, pontos_finais, melhor, colunas_matrix, fonte_matrix)

    audio_manager.stop_all()
    pygame.quit()
