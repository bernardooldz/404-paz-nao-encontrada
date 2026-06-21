# Testes

Esta pasta contem testes automatizados do projeto usando `pytest`.

## Arquivos

- `test_logica.py`: valida funcoes basicas de pontuacao, derrota e limitacao de valores.
- `test_funcoes_extra.py`: valida dano, colisao, criacao/atualizacao de obstaculos e consumiveis, retangulos de colisao e dificuldade progressiva.
- `test_dados.py`: valida salvamento e carregamento de recorde/ranking em arquivos temporarios.

## Como executar

```bash
python -m pytest
```

## Boas praticas

- Prefira testar regras puras em `src/funcoes.py` e persistencia em `src/dados.py`.
- Use `tmp_path` para testes que criam arquivos.
- Ao alterar constantes de dificuldade em `src/config.py`, revise os testes de `calcular_dificuldade`.
