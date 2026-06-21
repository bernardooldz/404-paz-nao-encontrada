# Dados

Esta pasta guarda persistencia simples em arquivos texto.

## Arquivos

- `recorde.txt`: melhor pontuacao salva quando o jogador supera o recorde anterior.
- `ranking.txt`: historico de pontuacoes, uma por linha.

## Como o jogo usa

`src/dados.py` le e escreve estes arquivos. Se algum arquivo nao existir ou tiver conteudo invalido, as funcoes retornam valores seguros (`0` ou lista vazia), evitando que o jogo quebre ao iniciar.

Evite versionar dados pessoais reais dos jogadores.
