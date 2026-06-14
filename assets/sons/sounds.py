from pathlib import Path

import pygame

from src.config import VOLUME_EFEITOS, VOLUME_MUSICA


DIR_SONS = Path(__file__).resolve().parent
ARQUIVO_MUSICA_FUNDO = DIR_SONS / "cyborg-ninja-kevin-macleod-main-version-7993-03-00.mp3"
ARQUIVOS_EFEITOS = {
    "hit_hurt": DIR_SONS / "hitHurt.wav",
    "power_up": DIR_SONS / "powerUp.wav",
}

_efeitos = {}
_musica_carregada = False
_audio_disponivel = False
_audio_desativado = False
_volume_musica = VOLUME_MUSICA
_volume_efeitos = VOLUME_EFEITOS


def preparar_mixer():
    # Deve ser chamado antes de pygame.init() para aplicar buffer menor.
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)


def inicializar_audio(volume_musica=VOLUME_MUSICA, volume_efeitos=VOLUME_EFEITOS):
    global _audio_disponivel, _audio_desativado, _volume_musica, _volume_efeitos

    _volume_musica = volume_musica
    _volume_efeitos = volume_efeitos

    if _audio_desativado:
        return False

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        _audio_disponivel = True
        carregar_audio()
        definir_volume_musica(_volume_musica)
        definir_volume_efeitos(_volume_efeitos)
        return True
    except (FileNotFoundError, pygame.error) as erro:
        _audio_disponivel = False
        _audio_desativado = True
        print(f"Audio desativado: {erro}")
        return False


def carregar_audio():
    global _musica_carregada

    if not _audio_disponivel:
        return

    if not ARQUIVO_MUSICA_FUNDO.exists():
        raise FileNotFoundError(f"Musica de fundo nao encontrada: {ARQUIVO_MUSICA_FUNDO}")

    if not _musica_carregada:
        pygame.mixer.music.load(str(ARQUIVO_MUSICA_FUNDO))
        _musica_carregada = True

    for nome, caminho in ARQUIVOS_EFEITOS.items():
        if not caminho.exists():
            raise FileNotFoundError(f"Efeito sonoro nao encontrado: {caminho}")
        if nome not in _efeitos:
            _efeitos[nome] = pygame.mixer.Sound(str(caminho))


def definir_volume_musica(volume):
    global _volume_musica

    _volume_musica = max(0.0, min(1.0, volume))
    if _audio_disponivel:
        pygame.mixer.music.set_volume(_volume_musica)


def definir_volume_efeitos(volume):
    global _volume_efeitos

    _volume_efeitos = max(0.0, min(1.0, volume))
    for som in _efeitos.values():
        som.set_volume(_volume_efeitos)


def tocar_musica_fundo():
    if not _audio_disponivel and not inicializar_audio(_volume_musica, _volume_efeitos):
        return

    pygame.mixer.music.set_volume(_volume_musica)
    pygame.mixer.music.play(loops=-1)


def tocar_efeito(nome):
    if not _audio_disponivel and not inicializar_audio(_volume_musica, _volume_efeitos):
        return

    som = _efeitos.get(nome)
    if som:
        som.play()


def tocar_som_dano():
    tocar_efeito("hit_hurt")


def tocar_som_power_up():
    tocar_efeito("power_up")
