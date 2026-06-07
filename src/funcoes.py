import pygame
import random

from src.config import (
    COLUNAS,
    ALTURA_TELA,
    TAMANHO_OBSTACULO_MIN,
    TAMANHO_OBSTACULO_MAX,
    VELOCIDADE_OBSTACULO,
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
    """Desenha o contador de pontuação centralizado no topo da tela."""
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(centerx=largura_tela // 2, top=10))
