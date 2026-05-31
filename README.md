# 404: Paz Não Encontrada

Projeto final da disciplina de Introdução a Algoritmos/Programação, desenvolvido com Python e Pygame.

Este repositório contém a base do jogo "404: Paz Não Encontrada" — um projeto do grupo para a disciplina. A proposta está em `docs/proposta.MD` e o README abaixo resume a ideia e o escopo planejado, sem afirmar implementações não concluídas.

## Integrantes do grupo

- Bernardo Lopes Diniz
- Daniel Heber de Souza Godinho

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
	- Arquivos previstos: `src/jogo.py`, `src/config.py`, `src/funcoes.py`, `src/dados.py`, `src/sprites.py`.
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

"404: Paz Não Encontrada" é um jogo de sobrevivência com temática de programação. O jogador controla um desenvolvedor que tenta encontrar momentos de paz após um longo dia de trabalho. Obstáculos relacionados ao cotidiano da programação (bugs, erros de sintaxe, conflitos de merge, deadlines, etc.) aparecem na tela e devem ser evitados. Itens especiais (ex.: café, testes automatizados) podem ser coletados para obter benefícios.

## Objetivo do jogador

Sobreviver o maior tempo possível, desviando dos obstáculos e acumulando pontos. O jogador deve tentar superar seu recorde anterior para alcançar a condição de vitória prevista na proposta.

## Regras do jogo

- O jogador inicia a partida com 3 vidas.
- Cada colisão com um obstáculo remove 1 vida.
- Itens especiais podem conceder pontos extras ou recuperar vidas.
- A pontuação aumenta com o tempo de sobrevivência e pela coleta de itens especiais.
- A partida termina quando as vidas chegam a zero.

## Controles

- Seta para esquerda ou tecla `a`: mover para a esquerda
- Seta para direita ou tecla `d`: mover para a direita
- Espaço: iniciar/reiniciar a partida
- `ESC`: sair do jogo

> Observação: estes controles fazem parte do escopo mínimo planejado; ajustes podem ocorrer durante a implementação.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
