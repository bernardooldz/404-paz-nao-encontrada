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


def atualizar_obstaculo(obstaculo):
    # Desce o obstáculo e aumenta seu tamanho conforme se aproxima da base
    obstaculo["y"] += VELOCIDADE_OBSTACULO
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
