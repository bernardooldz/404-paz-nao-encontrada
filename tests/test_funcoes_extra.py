import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import src.funcoes as funcoes
from src.funcoes import (tomar_dano, verificar_colisao, criar_obstaculo, atualizar_obstaculo, rect_obstaculo, criar_consumivel, atualizar_consumivel, rect_consumivel, calcular_dificuldade)
from src.config import (TAMANHO_OBSTACULO_MIN, TAMANHO_OBSTACULO_MAX, VELOCIDADE_OBSTACULO_INICIAL, VELOCIDADE_OBSTACULO_MAXIMA, INTERVALO_SPAWN_INICIAL, INTERVALO_SPAWN_MINIMO, INTERVALO_SPAWN_CONSUMIVEL_INICIAL, INTERVALO_SPAWN_CONSUMIVEL_MINIMO)

pygame.init()

def test_tomar_dano():
    assert tomar_dano(3, 1) == 2
    assert tomar_dano(1, 5) == -4


def test_verificar_colisao():
    r1 = pygame.Rect(0, 0, 10, 10)
    r2 = pygame.Rect(5, 5, 10, 10)
    r3 = pygame.Rect(20, 20, 5, 5)
    assert verificar_colisao(r1, r2) is True
    assert verificar_colisao(r1, r3) is False


def test_criar_e_atualizar_obstaculo(monkeypatch):
    # Forçar escolha e coluna previsíveis
    monkeypatch.setattr(funcoes.random, "choice", lambda lst: "IMG")
    monkeypatch.setattr(funcoes.random, "randint", lambda a, b: 1)

    obst = criar_obstaculo(["img1", "img2"])  # imagem original será "IMG"
    assert obst["imagem_original"] == "IMG"
    assert obst["coluna"] == 1
    assert obst["tamanho"] == TAMANHO_OBSTACULO_MIN
    assert obst["y"] <= 0

    # Atualizar obstáculo deve incrementar y e alterar tamanho proporcionalmente
    y_inicial = obst["y"]
    atualizar_obstaculo(obst, velocidade=2)
    assert obst["y"] == y_inicial + 2
    assert TAMANHO_OBSTACULO_MIN <= obst["tamanho"] <= TAMANHO_OBSTACULO_MAX


def test_rect_obstaculo():
    obst = {"coluna": 1, "tamanho": 40, "y": 10}
    r = rect_obstaculo(obst)
    assert isinstance(r, pygame.Rect)
    assert r.height == 40 and r.width == 40


def test_criar_consumivel_e_rect_e_atualizar():
    # imagens_consumiveis simples: item precisa de get_size
    class FakeImg:
        def __init__(self, w, h):
            self._size = (w, h)

        def get_size(self):
            return self._size

    imagens = {"cafe": {"item": FakeImg(50, 68), "uso": FakeImg(80, 120)}}
    consumivel = criar_consumivel(imagens, colunas_ocupadas=())
    assert consumivel["tipo"] in imagens
    assert consumivel["imagem"] is imagens[consumivel["tipo"]]["item"]
    assert consumivel["coluna"] in (0, 1, 2)

    y0 = consumivel["y"]
    atualizar_consumivel(consumivel)
    assert consumivel["y"] == y0 + funcoes.VELOCIDADE_CONSUMIVEL

    rc = rect_consumivel(consumivel)
    assert isinstance(rc, pygame.Rect)


def test_calcular_dificuldade_extremos():
    # pontos = 0 -> valores iniciais
    vel, intervalo, intervalo_con = calcular_dificuldade(0)
    assert vel == round(VELOCIDADE_OBSTACULO_INICIAL, 2)
    assert intervalo == INTERVALO_SPAWN_INICIAL
    assert intervalo_con == INTERVALO_SPAWN_CONSUMIVEL_INICIAL

    # pontos no limite máximo -> valores máximos/minimos
    pontos_max = funcoes._PONTOS_DIFICULDADE_MAX
    vel2, intervalo2, intervalo_con2 = calcular_dificuldade(pontos_max)
    assert vel2 == round(VELOCIDADE_OBSTACULO_MAXIMA, 2)
    assert intervalo2 == INTERVALO_SPAWN_MINIMO
    assert intervalo_con2 == INTERVALO_SPAWN_CONSUMIVEL_MINIMO
