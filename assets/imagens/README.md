# Imagens

Pasta de recursos visuais do jogo.

## Organizacao atual

- `personagem-principal/`: frames do personagem andando, virando, tomando dano e usando consumiveis.
- `obstaculos/`: imagens dos obstaculos que descem pelas pistas.
- `consumiveis/`: imagens de cafe, Monster e Spotify.
- `sistema/`: logo, coracoes e sprites usados em telas auxiliares.
- Arquivos `.png` na raiz: spritesheets de referencia do projeto.

## Observacoes

`src/sprites.py` carrega os assets principais da partida e aplica os tamanhos definidos em `src/config.py`. Algumas telas tambem carregam imagens diretamente em `src/jogo.py`.
