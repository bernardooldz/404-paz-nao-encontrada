import pygame
import random

from src.config import (
    COLUNAS,
    ALTURA_TELA,
    LARGURA_TELA,
    TAMANHO_OBSTACULO_MIN,
    TAMANHO_OBSTACULO_MAX,
    VELOCIDADE_OBSTACULO,
    VELOCIDADE_CONSUMIVEL,
    COR_EFEITO_CAFE,
    COR_EFEITO_MONSTER,
    COR_EFEITO_SPOTIFY,
)


def calcular_pontos(pontos_atual, pontos_ganhos):
    # Soma os pontos ganhos à pontuação atual
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    # Reduz a vida atual com base no dano recebido
    return vida_atual - dano


def jogador_perdeu(vidas):
    # Indica se o jogador ficou sem vidas
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    # Mantém um valor dentro do intervalo [minimo, maximo]
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    # Verifica sobreposição entre dois retângulos do Pygame
    return retangulo_1.colliderect(retangulo_2)


def criar_obstaculo(imagens_originais):
    # Cria um obstáculo aleatório em uma coluna aleatória, nascendo pequeno no topo
    return {
        "imagem_original": random.choice(imagens_originais),
        "coluna": random.randint(0, 2),
        "y": float(-TAMANHO_OBSTACULO_MIN),
        "tamanho": TAMANHO_OBSTACULO_MIN,
    }


def atualizar_obstaculo(obstaculo, velocidade=VELOCIDADE_OBSTACULO):
    # Desce o obstáculo e aumenta seu tamanho conforme se aproxima da base
    obstaculo["y"] += velocidade
    progresso = limitar_valor(obstaculo["y"] / ALTURA_TELA, 0.0, 1.0)
    obstaculo["tamanho"] = int(
        TAMANHO_OBSTACULO_MIN + (TAMANHO_OBSTACULO_MAX - TAMANHO_OBSTACULO_MIN) * progresso
    )


def rect_obstaculo(obstaculo):
    # Retorna o Rect atual do obstáculo, centralizado na sua coluna
    tam = obstaculo["tamanho"]
    x = COLUNAS[obstaculo["coluna"]] - tam // 2
    return pygame.Rect(x, int(obstaculo["y"]), tam, tam)


def desenhar_obstaculo(tela, obstaculo):
    # Redimensiona e desenha o obstáculo na tela
    tam = obstaculo["tamanho"]
    imagem = pygame.transform.scale(obstaculo["imagem_original"], (tam, tam))
    tela.blit(imagem, rect_obstaculo(obstaculo))


def desenhar_vidas(tela, vidas, coracao_cheio, coracao_vazio, total=3):
    # Desenha os ícones de coração no topo da tela
    largura, altura = coracao_cheio.get_size()
    margem = 10
    for i in range(total):
        imagem = coracao_cheio if i < vidas else coracao_vazio
        tela.blit(imagem, (margem + i * (largura + 6), margem))


def desenhar_pontuacao(tela, pontos, largura_tela):
    # Desenha o contador de pontuação centralizado no topo da tela
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(centerx=largura_tela // 2, top=10))


def contagem_regressiva(tela, relogio, largura_tela, altura_tela, fps):
    # Exibe "3", "2", "1", "JÁ!" por 1 segundo cada antes de iniciar a partida
    fonte = pygame.font.SysFont(None, 160)
    etapas = ["3", "2", "1", "JÁ!"]
    for etapa in etapas:
        for _ in range(fps):
            relogio.tick(fps)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
            tela.fill((0, 0, 0))
            texto = fonte.render(etapa, True, (255, 255, 255))
            tela.blit(texto, texto.get_rect(center=(largura_tela // 2, altura_tela // 2)))
            pygame.display.flip()
    return True


def criar_consumivel(imagens_consumiveis):
    # Cria um consumível aleatório em uma coluna aleatória, nascendo no topo
    tipo = random.choice(list(imagens_consumiveis.keys()))
    return {
        "tipo": tipo,
        "imagem": imagens_consumiveis[tipo]["item"],
        "coluna": random.randint(0, 2),
        "y": float(-60),
    }


def atualizar_consumivel(consumivel):
    # Desce o consumível na tela
    consumivel["y"] += VELOCIDADE_CONSUMIVEL


def rect_consumivel(consumivel):
    # Retorna o Rect do consumível centralizado na sua coluna
    w, h = consumivel["imagem"].get_size()
    x = COLUNAS[consumivel["coluna"]] - w // 2
    return pygame.Rect(x, int(consumivel["y"]), w, h)


def desenhar_consumivel(tela, consumivel):
    # Desenha o consumível na tela
    tela.blit(consumivel["imagem"], rect_consumivel(consumivel))


_CORES_EFEITO = {
    "cafe":    COR_EFEITO_CAFE,
    "monster": COR_EFEITO_MONSTER,
    "spotify": COR_EFEITO_SPOTIFY,
}


def desenhar_efeito_ativo(tela, efeito_ativo, timer_efeito, duracao_efeito):
    # Desenha overlay colorido e barra de duração do efeito ativo
    if not efeito_ativo:
        return
    cor = _CORES_EFEITO.get(efeito_ativo)
    if not cor:
        return

    # Overlay semitransparente cobrindo toda a tela
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    overlay.fill(cor)
    tela.blit(overlay, (0, 0))

    # Barra de progresso no canto superior direito
    proporcao = timer_efeito / duracao_efeito
    barra_largura = 120
    barra_altura = 10
    x_barra = LARGURA_TELA - barra_largura - 10
    y_barra = 10
    pygame.draw.rect(tela, (60, 60, 60),  (x_barra, y_barra, barra_largura, barra_altura))
    pygame.draw.rect(tela, cor[:3],       (x_barra, y_barra, int(barra_largura * proporcao), barra_altura))

    # Nome do efeito acima da barra
    nomes = {"cafe": "Cafe: +vida", "monster": "Monster: 2x pts", "spotify": "Spotify: invenc."}
    fonte = pygame.font.SysFont(None, 22)
    texto = fonte.render(nomes[efeito_ativo], True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(right=LARGURA_TELA - 10, bottom=y_barra - 2))
