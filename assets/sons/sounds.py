from pathlib import Path

import pygame


DIR_SONS = Path(__file__).resolve().parent


class AudioManager:

    def __init__(self):
        self.menu_music_volume = 0.45
        self.game_music_volume = 0.22
        self.pause_music_volume = 0.35
        self.victory_music_volume = 0.65
        self.defeat_music_volume = 0.90
        self.hit_hurt_volume = 0.50
        self.powerup_volume = 0.15

        self.master_music_volume = 1.0
        self.master_effects_volume = 1.0

        self._music_files = {
            "menu_music": DIR_SONS / "menu-pause-sound.mp3",
            "game_music": DIR_SONS / "cyborg-ninja-kevin-macleod-main-version-7993-03-00.mp3",
            "pause_music": DIR_SONS / "menu-pause-sound.mp3",
            "victory_music": DIR_SONS / "sound__achievement.wav",
            "defeat_music": DIR_SONS / "death-sound-43894.mp3",
        }
        self._effect_files = {
            "hit_hurt": DIR_SONS / "hitHurt.wav",
            "powerup": DIR_SONS / "powerUp.wav",
        }
        self._music_loops = {
            "menu_music": -1,
            "game_music": -1,
            "pause_music": -1,
            "victory_music": 0,
            "defeat_music": 0,
        }
        self._persistent_music_channels = {"menu_music", "game_music"}

        self._sounds = {}
        self._music_channels = {}
        self._music_channel_volume_keys = {}
        self._audio_available = False
        self._audio_disabled = False
        self._muted = False
        self._volume_before_mute = (self.master_music_volume, self.master_effects_volume)
        self._current_music_key = None
        self._resume_music_key = None

    def initialize(self):
        if self._audio_disabled:
            return False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_num_channels(max(16, pygame.mixer.get_num_channels()))
            self._audio_available = True
            self.load_audio()
            self.refresh_volumes()
            return True
        except (FileNotFoundError, pygame.error) as erro:
            self._audio_available = False
            self._audio_disabled = True
            print(f"Audio desativado: {erro}")
            return False

    def load_audio(self):
        if not self._audio_available:
            return

        for nome, caminho in {**self._music_files, **self._effect_files}.items():
            if not caminho.exists():
                raise FileNotFoundError(f"Arquivo de audio nao encontrado: {caminho}")
            if nome not in self._sounds:
                self._sounds[nome] = pygame.mixer.Sound(str(caminho))

    def play_menu_music(self, restart=False):
        self.play_music("menu_music", restart=restart)

    def play_game_music(self, restart=False):
        self.play_music("game_music", restart=restart)

    def play_pause_music(self, restart=False):
        self.play_music("pause_music", restart=restart, keep_paused=True)

    def play_victory_music(self, restart=True):
        self.play_music("victory_music", restart=restart)

    def play_defeat_music(self, restart=True):
        self.play_music("defeat_music", restart=restart)

    def play_music(self, music_key, restart=False, keep_paused=False):
        if music_key not in self._music_files:
            return
        if not self._ensure_audio():
            return

        channel_key = self._channel_key(music_key)
        canal_atual = self._music_channels.get(channel_key)
        if not restart and canal_atual:
            self.pause_music(except_keys={music_key})
            canal_atual.unpause()
            self._music_channel_volume_keys[channel_key] = music_key
            self._current_music_key = music_key
            self._apply_music_channel_volume(music_key)
            return

        excecoes = {music_key}
        if keep_paused and self._resume_music_key:
            excecoes.add(self._resume_music_key)
        self.pause_music(except_keys=excecoes)

        som = self._sounds.get(music_key)
        if not som:
            return

        canal_anterior = self._music_channels.get(channel_key)
        if canal_anterior:
            canal_anterior.stop()

        canal = som.play(loops=self._music_loops.get(music_key, -1))
        if canal:
            self._music_channels[channel_key] = canal
            self._music_channel_volume_keys[channel_key] = music_key
            self._current_music_key = music_key
            self._apply_music_channel_volume(music_key)

    def enter_pause(self):
        if not self._ensure_audio():
            return
        if self._current_music_key == "pause_music":
            return

        self._resume_music_key = self._current_music_key
        canal_partida = self._music_channels.get(self._resume_music_key)
        if canal_partida:
            canal_partida.pause()
        self._current_music_key = None
        self.play_pause_music(restart=False)

    def resume_after_pause(self):
        if not self._ensure_audio():
            return

        self.pause_music(except_keys={self._resume_music_key} if self._resume_music_key else set())
        canal_partida = self._music_channels.get(self._channel_key(self._resume_music_key))
        if canal_partida:
            canal_partida.unpause()
            self._current_music_key = self._resume_music_key
            self._music_channel_volume_keys[self._channel_key(self._resume_music_key)] = self._resume_music_key
            self._apply_music_channel_volume(self._resume_music_key)
        elif self._resume_music_key:
            self.play_music(self._resume_music_key)
        self._resume_music_key = None

    def pause_music(self, except_keys=None):
        excecoes = {self._channel_key(nome) for nome in (except_keys or ()) if nome}
        for nome, canal in list(self._music_channels.items()):
            if nome in excecoes:
                continue
            if nome in self._persistent_music_channels:
                canal.pause()
            else:
                canal.stop()
                self._music_channels.pop(nome, None)
                self._music_channel_volume_keys.pop(nome, None)
        if self._channel_key(self._current_music_key) not in excecoes:
            self._current_music_key = None

    def stop_music(self, except_keys=None):
        excecoes = {self._channel_key(nome) for nome in (except_keys or ()) if nome}
        for nome, canal in list(self._music_channels.items()):
            if nome in excecoes:
                continue
            canal.stop()
            self._music_channels.pop(nome, None)
            self._music_channel_volume_keys.pop(nome, None)
        if self._channel_key(self._current_music_key) not in excecoes:
            self._current_music_key = None
        if self._channel_key(self._resume_music_key) not in excecoes:
            self._resume_music_key = None

    def stop_all(self):
        self.stop_music()
        if self._audio_available:
            pygame.mixer.stop()

    def play_effect(self, effect_key):
        if effect_key not in self._effect_files:
            return
        if not self._ensure_audio():
            return

        som = self._sounds.get(effect_key)
        if som:
            som.set_volume(self._effective_effect_volume(effect_key))
            som.play()

    def play_hit_hurt(self):
        self.play_effect("hit_hurt")

    def play_powerup(self):
        self.play_effect("powerup")

    def set_master_music_volume(self, volume, unmute=True):
        self.master_music_volume = self._clamp_volume(volume)
        if unmute and self.master_music_volume > 0:
            self._muted = False
            self._volume_before_mute = (self.master_music_volume, self.master_effects_volume)
        self.refresh_volumes()

    def set_master_effects_volume(self, volume):
        self.master_effects_volume = self._clamp_volume(volume)
        self.refresh_volumes()

    def set_master_volume(self, volume, unmute=True):
        volume = self._clamp_volume(volume)
        self.master_music_volume = volume
        self.master_effects_volume = volume
        if unmute and volume > 0:
            self._muted = False
            self._volume_before_mute = (volume, volume)
        self.refresh_volumes()

    def set_individual_volume(self, sound_key, volume):
        atributo = f"{sound_key}_volume"
        if hasattr(self, atributo):
            setattr(self, atributo, self._clamp_volume(volume))
            self.refresh_volumes()

    def toggle_mute(self):
        if self.is_muted:
            self._muted = False
            volume_musica, volume_efeitos = self._volume_before_mute
            if self.master_music_volume <= 0:
                self.master_music_volume = volume_musica or 1.0
            if self.master_effects_volume <= 0:
                self.master_effects_volume = volume_efeitos or self.master_music_volume
        else:
            if self.master_music_volume > 0 or self.master_effects_volume > 0:
                self._volume_before_mute = (self.master_music_volume, self.master_effects_volume)
            self._muted = True
        self.refresh_volumes()

    @property
    def is_muted(self):
        return self._muted

    def refresh_volumes(self):
        if not self._audio_available:
            return
        for channel_key, music_key in self._music_channel_volume_keys.items():
            self._apply_music_channel_volume(music_key)
        for nome in self._effect_files:
            som = self._sounds.get(nome)
            if som:
                som.set_volume(self._effective_effect_volume(nome))

    def _ensure_audio(self):
        return self._audio_available or self.initialize()

    def _apply_music_channel_volume(self, music_key):
        channel_key = self._channel_key(music_key)
        canal = self._music_channels.get(channel_key)
        if canal:
            canal.set_volume(self._effective_music_volume(music_key))

    @staticmethod
    def _channel_key(music_key):
        if music_key == "pause_music":
            return "menu_music"
        return music_key

    def _effective_music_volume(self, music_key):
        if self._muted:
            return 0.0
        volume_individual = getattr(self, f"{music_key}_volume", 1.0)
        return self._clamp_volume(volume_individual * self.master_music_volume)

    def _effective_effect_volume(self, effect_key):
        if self._muted:
            return 0.0
        volume_individual = getattr(self, f"{effect_key}_volume", 1.0)
        return self._clamp_volume(volume_individual * self.master_effects_volume)

    @staticmethod
    def _clamp_volume(volume):
        return max(0.0, min(1.0, float(volume)))


audio_manager = AudioManager()


def preparar_mixer():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)


def inicializar_audio(volume_musica=None, volume_efeitos=None):
    if volume_musica is not None:
        audio_manager.set_master_music_volume(volume_musica, unmute=False)
    if volume_efeitos is not None:
        audio_manager.set_master_effects_volume(volume_efeitos)
    return audio_manager.initialize()


def definir_volume_musica(volume):
    audio_manager.set_master_music_volume(volume)


def definir_volume_efeitos(volume):
    audio_manager.set_master_effects_volume(volume)


def alternar_mudo():
    audio_manager.toggle_mute()


def tocar_musica_menu():
    audio_manager.play_menu_music()


def tocar_musica_jogo(restart=False):
    audio_manager.play_game_music(restart=restart)


def tocar_musica_pausa():
    audio_manager.play_pause_music()


def tocar_musica_vitoria():
    audio_manager.play_victory_music()


def tocar_musica_derrota():
    audio_manager.play_defeat_music()


def pausar_musica_jogo():
    audio_manager.enter_pause()


def retomar_musica_jogo():
    audio_manager.resume_after_pause()


def tocar_musica_fundo():
    audio_manager.play_game_music()


def tocar_efeito(nome):
    audio_manager.play_effect(nome)


def tocar_som_dano():
    audio_manager.play_hit_hurt()


def tocar_som_power_up():
    audio_manager.play_powerup()
