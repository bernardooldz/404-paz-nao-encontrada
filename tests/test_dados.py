import os
from src.dados import salvar_recorde, carregar_recorde, salvar_ranking, carregar_melhor_ranking


def test_salvar_e_carregar_recorde(tmp_path):
    arquivo = tmp_path / "recorde.txt"
    salvar_recorde(str(arquivo), 123)
    assert carregar_recorde(str(arquivo)) == 123


def test_carregar_recorde_arquivo_inexistente(tmp_path):
    arquivo = tmp_path / "nao_existe.txt"
    assert carregar_recorde(str(arquivo)) == 0


def test_salvar_ranking_e_carregar_melhor(tmp_path):
    arquivo = tmp_path / "ranking.txt"
    salvar_ranking(str(arquivo), 10)
    salvar_ranking(str(arquivo), 50)
    salvar_ranking(str(arquivo), 30)
    assert carregar_melhor_ranking(str(arquivo)) == 50
