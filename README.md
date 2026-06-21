# 404: Paz Nao Encontrada

Projeto final da disciplina de Introducao a Algoritmos/Programacao, desenvolvido em Python com Pygame.

O jogo e uma experiencia arcade de sobrevivencia em tres pistas: o jogador controla um desenvolvedor tentando encontrar paz enquanto desvia de problemas comuns do dia a dia de programacao. A proposta do projeto fica em `docs/proposta.MD`.

## Integrantes

- Bernardo Diniz
- Daniel Heber de Souza Godinho
- Thiago de Castro

## Como jogar

O jogador comeca com 3 vidas e ganha 10 pontos por segundo sobrevivido. Obstaculos descem pela tela e causam 1 ponto de dano ao colidir com o personagem. A partida termina quando as vidas chegam a zero.

A dificuldade aumenta progressivamente conforme a pontuacao: os obstaculos ficam mais rapidos, aparecem com mais frequencia e os consumiveis tambem mudam de ritmo.

Consumiveis disponiveis:

- Cafe: restaura 1 vida, respeitando o maximo de 3 vidas.
- Monster: dobra os pontos recebidos por alguns segundos.
- Spotify: deixa o jogador invencivel por alguns segundos.

Ao tomar dano, o personagem pisca, fica temporariamente invencivel e os obstaculos desaceleram por um curto periodo.

## Controles

- `A` ou seta para esquerda: mover para a pista da esquerda.
- `D` ou seta para direita: mover para a pista da direita.
- `Espaco`: iniciar a partida, pausar durante o jogo, retomar ou jogar novamente.
- `T`: abrir o tutorial na tela inicial.
- `H`: abrir o historico de pontuacoes na tela inicial.
- `ESC`: voltar, sair da tela atual ou encerrar o jogo.
- Mouse no canto superior direito: ajustar volume ou alternar mudo.

## Execucao

Requisitos:

- Python 3.10 ou superior recomendado.
- Dependencias em `requirements.txt`.

Instalacao e execucao:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Em Linux/macOS, ative o ambiente com:

```bash
source .venv/bin/activate
```

## Testes

```bash
python -m pytest
```

Os testes cobrem funcoes puras de logica, colisao, criacao e atualizacao de obstaculos/consumiveis, dificuldade progressiva e persistencia simples de dados.

## Estrutura

- `main.py`: ponto de entrada da aplicacao.
- `src/jogo.py`: telas, loop principal, eventos, renderizacao, regras de partida e integracao entre modulos.
- `src/config.py`: constantes de tela, FPS, caminhos, cores, tamanhos e parametros de dificuldade.
- `src/funcoes.py`: funcoes auxiliares de logica, colisao, HUD, obstaculos, consumiveis e fundo Matrix.
- `src/sprites.py`: carregamento e redimensionamento de sprites.
- `src/dados.py`: leitura e escrita de recorde/ranking.
- `assets/`: imagens, sons e fontes.
- `data/`: arquivos de persistencia em texto.
- `tests/`: testes automatizados com pytest.
- `docs/`: documentos de planejamento e apoio.

## Persistencia

O projeto usa arquivos texto simples:

- `data/ranking.txt`: recebe uma pontuacao por linha ao fim de cada partida.
- `data/recorde.txt`: guarda o recorde usado como referencia historica.

O historico exibido no jogo ordena as pontuacoes do ranking da maior para a menor.
