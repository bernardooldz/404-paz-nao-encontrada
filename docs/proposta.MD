# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na Semana 1 do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com Python e Pygame dentro do prazo disponível.

## 1. Nome provisório do jogo

404: Paz Não Encontrada

## 2. Integrantes do grupo

- Nome 1: Bernardo Diniz
- Nome 2: Daniel Heber de Souza Godinho

## 3. Tipo de jogo

Nave desviando de meteoros

## 4. Descrição geral do jogo

O jogo "404: Paz Não Encontrada" é um jogo de sobrevivência com temática de programação. O jogador controla um desenvolvedor que tenta encontrar alguns momentos de paz após um longo dia de trabalho. Durante a partida, diversos obstáculos relacionados ao cotidiano da programação caem pela tela, como bugs, erros de sintaxe, conflitos de merge e deadlines. O objetivo é desviar desses obstáculos, coletar itens úteis e sobreviver o maior tempo possível.

## 5. Objetivo do jogador

Sobreviver o maior tempo possível, desviando dos obstáculos e acumulando pontos. O jogador deverá alcançar uma pontuação superior ao seu último recorde para finalmente encontrar a paz e concluir o jogo.

## 6. Regras principais

- Regra 1: O jogador inicia a partida com 3 vidas.
- Regra 2: Cada obstáculo atingido remove 1 vida.
- Regra 3: Itens especiais podem conceder pontos extras ou recuperar vidas.
- Regra 4: A pontuação aumenta conforme o tempo de sobrevivência.
- Regra 5: O jogador vence ao alcançar uma pontuação superior ao seu último recorde ou perde ao ficar sem vidas.

## 7. Condição de vitória

O jogador vence ao atingir uma pontuação superior ao seu último recorde, representando o momento em que finalmente encontra a paz. Ao vencer, será exibida uma mensagem indicando "200 OK: Paz Encontrada".

## 8. Condição de derrota ou encerramento

A partida termina quando o jogador perde todas as suas vidas ao colidir com obstáculos. Nesse momento será exibida a mensagem "404: Paz Não Encontrada".

## 9. Elementos previstos no jogo

## Jogador ou elemento principal

Um desenvolvedor representado por um personagem simples controlado pelo teclado, que pode se mover horizontalmente pela tela.

## Obstáculos, inimigos ou desafios

Bugs, erros de sintaxe, conflitos de merge, reuniões inesperadas e deadlines aparecerão aleatoriamente e deverão ser evitados.

## Itens, alvos ou objetos de interação

Itens especiais como café, testes automatizados e ChatGPT poderão aparecer durante a partida oferecendo benefícios ao jogador.

## Pontuação, vidas, tempo ou progresso

O jogador começa com 3 vidas. A pontuação aumenta conforme o tempo de sobrevivência e pela coleta de itens especiais. O progresso é medido pela quantidade de pontos acumulados até atingir uma pontuação superior ao seu último recorde.

## 10. Controles previstos

- Seta para esquerda ou a tecla "a": mover para a esquerda
- Seta para direita ou a tecla "d": mover para a direita
- Espaço: iniciar/reiniciar a partida
- ESC: sair do jogo

## 11. Organização inicial do código

- `main.py`: inicia o jogo;
- `src/jogo.py`: contém o loop principal;
- `src/config.py`: guarda configurações como tamanho da tela e cores;
- `src/funcoes.py`: contém funções auxiliares;
- `src/dados.py`: contém funções de leitura e escrita de arquivos.

## 12. Recursos externos previstos

- imagens obtidas de banco gratuito;
- sons gratuitos;
- fonte personalizada.

## 13. Principais dificuldades esperadas

- Dificuldade 1: Implementação do sistema de colisão entre jogador e obstáculos.
- Dificuldade 2: Criação do sistema de geração aleatória de obstáculos e itens.
- Dificuldade 3: Organização do código em módulos e implementação do sistema de pontuação e ranking.

## 14. Escopo mínimo para a entrega final

A versão mínima do jogo terá um personagem controlado pelo teclado, obstáculos surgindo aleatoriamente, sistema de vidas, sistema de pontuação, tela de vitória ao alcançar uma pontuação superior ao seu último recorde e tela de derrota quando as vidas chegarem a zero.

## 15. Possíveis melhorias, caso haja tempo

- Melhoria 1: Aumento gradual da dificuldade com obstáculos mais rápidos conforme a pontuação aumenta.
- Melhoria 2: Implementação de itens especiais com efeitos temporários, como invencibilidade por alguns segundos ou redução da velocidade dos obstáculos.
- Melhoria 3: Usuário poder mudar o visual de seu personagem.
