import pygame
import os

from src.config import (
    DIR_PERSONAGEM, DIR_OBSTACULOS, DIR_SISTEMA, DIR_CONSUMIVEIS,
    TAMANHO_PERSONAGEM, TAMANHO_CORACAO, TAMANHO_CONSUMIVEL,
)


def carregar_imagens_personagem():
    # Carrega e redimensiona os sprites do personagem principal
    def carregar(nome):
        caminho = os.path.join(DIR_PERSONAGEM, nome)
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, TAMANHO_PERSONAGEM)

    frames_frente = [
        carregar("spritesheet-404-pne-andando-reto-frente-1.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-2.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-3.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-4.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-5.png"),
        carregar("spritesheet-404-pne-andando-reto-frente-6.png"),
    ]
    frame_direita  = carregar("spritesheet-404-pne-virando-direita-1.png")
    frame_esquerda = carregar("spritesheet-404-pne-virando-esquerda-1.png")
    return frames_frente, frame_direita, frame_esquerda


def carregar_imagens_dano():
    # Carrega os frames de dano do personagem
    def carregar(nome):
        caminho = os.path.join(DIR_PERSONAGEM, nome)
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, TAMANHO_PERSONAGEM)

    return [
        carregar("spritesheet-404-pne-consumiveis-_-dano-sofrendando-dano-1.png"),
        carregar("spritesheet-404-pne-consumiveis-_-dano-sofrendando-dano-2.png"),
    ]


def carregar_imagens_coracoes():
    # Carrega os ícones de coração cheio e vazio
    def carregar(nome):
        caminho = os.path.join(DIR_SISTEMA, nome)
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, TAMANHO_CORACAO)

    cheio = carregar("spritesheet-404-pne-consumiveis-&-dano-coracao-cheio.png")
    vazio = carregar("spritesheet-404-pne-consumiveis-&-dano-coracao-vazio.png")
    return cheio, vazio


def carregar_imagens_obstaculos():
    # Carrega as imagens originais dos obstáculos sem redimensionar
    arquivos = [f for f in os.listdir(DIR_OBSTACULOS) if f.endswith(".png")]
    imagens = []
    for arquivo in arquivos:
        caminho = os.path.join(DIR_OBSTACULOS, arquivo)
        imagens.append(pygame.image.load(caminho).convert_alpha())
    return imagens


def carregar_consumiveis():
    # Carrega imagens dos consumiveis e dos frames de uso do personagem
    # Retorna dicionario: tipo -> {"item": Surface, "uso": Surface}
    nomes = {
        "cafe":    ("spritesheet-404-pne-consumiveis-_-dano-cafe.png",    "spritesheet-404-pne-consumiveis-_-dano-usando-cafe.png"),
        "monster": ("spritesheet-404-pne-consumiveis-_-dano-monster.png", "spritesheet-404-pne-consumiveis-_-dano-usando-monster.png"),
        "spotify": ("spritesheet-404-pne-consumiveis-_-dano-spotify.png", "spritesheet-404-pne-consumiveis-_-dano-usando-spotify.png"),
    }
    resultado = {}
    for tipo, (arq_item, arq_uso) in nomes.items():
        img_item = pygame.image.load(os.path.join(DIR_CONSUMIVEIS, arq_item)).convert_alpha()
        img_item = pygame.transform.scale(img_item, TAMANHO_CONSUMIVEL)
        img_uso  = pygame.image.load(os.path.join(DIR_PERSONAGEM, arq_uso)).convert_alpha()
        img_uso  = pygame.transform.scale(img_uso, TAMANHO_PERSONAGEM)
        resultado[tipo] = {"item": img_item, "uso": img_uso}
    return resultado
