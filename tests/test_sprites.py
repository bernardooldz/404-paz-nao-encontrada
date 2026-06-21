import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
import types

from src import sprites
from src.config import TAMANHO_PERSONAGEM, TAMANHO_CORACAO, TAMANHO_CONSUMIVEL


class FakeSurface:
    def __init__(self, size=(10, 10)):
        self._size = size

    def convert_alpha(self):
        return self

    def get_size(self):
        return self._size


def test_carregar_imagens_personagem_e_coracoes(monkeypatch):
    # monkeypatch pygame.image.load and pygame.transform.scale
    monkeypatch.setattr(sprites.os, "path", sprites.os.path)

    def fake_load(path):
        return FakeSurface((100, 200))

    def fake_scale(surface, size):
        return FakeSurface(size)

    monkeypatch.setattr(pygame.image, "load", fake_load)
    monkeypatch.setattr(pygame.transform, "scale", fake_scale)

    frames, dr, esq = sprites.carregar_imagens_personagem()
    assert isinstance(frames, list)
    assert len(frames) >= 1
    assert dr.get_size() == TAMANHO_PERSONAGEM
    assert esq.get_size() == TAMANHO_PERSONAGEM

    cheio, vazio = sprites.carregar_imagens_coracoes()
    assert cheio.get_size() == TAMANHO_CORACAO
    assert vazio.get_size() == TAMANHO_CORACAO


def test_carregar_imagens_obstaculos_e_consumiveis(monkeypatch, tmp_path):
    # Fake os.listdir to list some png files
    monkeypatch.setattr(sprites.os, "listdir", lambda d: ["a.png", "b.png", "ignore.txt"])  # for obstaculos

    def fake_load(path):
        return FakeSurface((40, 40))

    def fake_scale(surface, size):
        return FakeSurface(size)

    monkeypatch.setattr(pygame.image, "load", fake_load)
    monkeypatch.setattr(pygame.transform, "scale", fake_scale)

    imgs = sprites.carregar_imagens_obstaculos()
    assert isinstance(imgs, list)
    assert len(imgs) == 2

    consum = sprites.carregar_consumiveis()
    assert isinstance(consum, dict)
    for k, v in consum.items():
        assert "item" in v and "uso" in v
        assert v["item"].get_size() == TAMANHO_CONSUMIVEL
        assert v["uso"].get_size() == TAMANHO_PERSONAGEM
