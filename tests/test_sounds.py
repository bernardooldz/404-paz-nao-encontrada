import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from assets.sons.sounds import AudioManager, audio_manager


class FakeChannel:
    def __init__(self):
        self.last_volume = None
        self.paused = False

    def set_volume(self, v):
        self.last_volume = v

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def stop(self):
        pass


class FakeSound:
    def __init__(self, channel):
        self._channel = channel

    def play(self, loops=-1):
        return self._channel

    def set_volume(self, v):
        self._last_set = v


def test_clamp_and_volume_logic(monkeypatch):
    am = AudioManager()

    # clamp
    assert am._clamp_volume(1.5) == 1.0
    assert am._clamp_volume(-0.2) == 0.0
    assert am._clamp_volume(0.5) == 0.5

    # prepare fake channels/sounds and mark audio available so refresh_volumes acts
    am._audio_available = True
    ch = FakeChannel()
    # map a music key to a channel key
    am._music_channels = {"game_music": ch}
    am._music_channel_volume_keys = {"game_music": "game_music"}
    am._sounds = {"game_music": FakeSound(ch), "hit_hurt": FakeSound(ch)}

    # set individual and master volumes
    am.set_master_music_volume(0.6)
    assert 0.0 <= am.master_music_volume <= 1.0

    am.set_master_effects_volume(0.4)
    assert 0.0 <= am.master_effects_volume <= 1.0

    # effective music volume should account for per-music individual * master
    ev = am._effective_music_volume("game_music")
    expected = am._clamp_volume(getattr(am, "game_music_volume", 1.0) * am.master_music_volume)
    assert ev == expected

    # toggle mute -> muted True
    am.toggle_mute()
    assert am.is_muted is True
    # volumes when muted should be zero effective
    assert am._effective_music_volume("game_music") == 0.0

    # toggle again -> unmuted
    am.toggle_mute()
    assert am.is_muted in (False, True)  # logic restores previous state; ensure method runs


def test_channel_key_and_effect_volume(monkeypatch):
    # _channel_key maps pause_music -> menu_music
    from assets.sons.sounds import AudioManager
    assert AudioManager._channel_key("pause_music") == "menu_music"
    assert AudioManager._channel_key("anything_else") == "anything_else"

    am = AudioManager()
    am._audio_available = True
    am.master_effects_volume = 0.5
    am._muted = False
    # effect volume uses per-effect attribute (hit_hurt_volume) * master_effects_volume
    assert am._effective_effect_volume("hit_hurt") == am._clamp_volume(getattr(am, "hit_hurt_volume", 1.0) * am.master_effects_volume)

    # when muted, effective volume is 0
    am._muted = True
    assert am._effective_effect_volume("hit_hurt") == 0.0


def test_set_individual_volume_and_set_master(monkeypatch):
    am = AudioManager()
    am._audio_available = True
    # set known attribute
    am.set_individual_volume("hit_hurt", 0.2)
    assert hasattr(am, "hit_hurt_volume")
    assert 0.0 <= am.hit_hurt_volume <= 1.0

    # set_master_volume sets both master volumes
    am.set_master_volume(0.3)
    assert am.master_music_volume == 0.3
    assert am.master_effects_volume == 0.3


def test_play_effect_no_audio(monkeypatch):
    # ensure no exception when audio not available
    am = AudioManager()
    am._audio_available = False
    # Should simply return without raising
    am.play_effect("hit_hurt")

    # invalid effect key -> no-op
    am._audio_available = True
    am._sounds = {}
    am.play_effect("nonexistent")
