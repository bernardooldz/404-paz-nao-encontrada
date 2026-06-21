import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pygame
from src import jogo


def test_retangulos_controle_volume_and_definir(monkeypatch):
    # Test _retangulos_controle_volume returns three rects and proportions consistent
    icone, slider, area = jogo._retangulos_controle_volume()
    assert hasattr(icone, "width") and hasattr(slider, "width")

    # Monkeypatch audio_manager.set_master_volume to capture value
    calls = {}

    def fake_set_master_volume(v):
        calls['v'] = v

    monkeypatch.setattr(jogo.audio_manager, "set_master_volume", fake_set_master_volume)

    # choose a mouse x in the middle of the slider
    x_mouse = slider.left + slider.width // 2
    jogo._definir_volume_pelo_mouse(x_mouse)
    assert 'v' in calls
    assert 0.0 <= calls['v'] <= 1.0


def test_processar_evento_controle_volume_toggle_and_drag(monkeypatch):
    # prepare fake audio_manager methods
    toggled = {'mute': 0}

    def fake_toggle_mute():
        toggled['mute'] += 1

    def fake_set_master_volume(v):
        toggled['last_vol'] = v

    monkeypatch.setattr(jogo.audio_manager, "toggle_mute", fake_toggle_mute)
    monkeypatch.setattr(jogo.audio_manager, "set_master_volume", fake_set_master_volume)

    # build events for clicking icon and clicking slider
    icone, slider, area = jogo._retangulos_controle_volume()
    # click on icon -> should toggle
    ev_down_icon = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=icone.center)
    handled = jogo._processar_evento_controle_volume(ev_down_icon)
    assert handled is True
    assert toggled['mute'] == 1

    # click on slider area -> start dragging and set volume
    ev_down_slider = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=area.center)
    handled2 = jogo._processar_evento_controle_volume(ev_down_slider)
    assert handled2 is True
    assert 'last_vol' in toggled

    # motion while dragging should call set_master_volume
    ev_motion = pygame.event.Event(pygame.MOUSEMOTION, pos=(slider.left + 1, slider.top + 1))
    jogo._arrastando_volume = True
    handled3 = jogo._processar_evento_controle_volume(ev_motion)
    assert handled3 is True

    # mouse up stops dragging
    ev_up = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=(0, 0))
    jogo._processar_evento_controle_volume(ev_up)
    assert jogo._arrastando_volume is False
