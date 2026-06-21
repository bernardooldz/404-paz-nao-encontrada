# Codigo-fonte (`src`)

Esta pasta contem os modulos principais do jogo.

## Modulos

- `jogo.py`: coordena a aplicacao. Contem tela inicial, tutorial, historico, pausa, tela final, loop principal, eventos, spawn de elementos, pontuacao, dano, efeitos de consumiveis e chamadas de audio.
- `config.py`: centraliza constantes de configuracao, como tamanho base da janela, FPS, caminhos de assets/dados, cores, tamanhos dos sprites, duracoes e parametros de dificuldade.
- `funcoes.py`: agrupa funcoes reutilizaveis de regra e renderizacao auxiliar, incluindo pontos, vidas, colisao, obstaculos, consumiveis, dificuldade progressiva, HUD, fundo Matrix e linhas das pistas.
- `sprites.py`: carrega imagens do personagem, coracoes, obstaculos e consumiveis, redimensionando para os tamanhos usados no jogo.
- `dados.py`: salva e carrega recorde e ranking em arquivos texto.
- `__init__.py`: marca a pasta como pacote Python.

## Fluxo principal

`main.py` chama `executar_jogo()` em `jogo.py`. A funcao inicializa Pygame e audio, ajusta a janela ao tamanho do desktop, carrega assets, exibe a tela inicial e inicia partidas ate o jogador sair.

Durante uma partida, o estado fica em um dicionario criado por `_estado_inicial()`. Esse estado controla pista atual, animacao, obstaculos, consumiveis, vidas, pontos, dano temporario e efeitos ativos.

## Cuidados ao alterar

- Mantenha regras testaveis em `funcoes.py` sempre que possivel.
- Ao adicionar asset novo, atualize tambem os caminhos/listas em `sprites.py` ou `jogo.py`.
- Se alterar pontuacao, vidas, colisao, dificuldade ou persistencia, atualize os testes em `tests/`.
