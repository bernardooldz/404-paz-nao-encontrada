# Proposta Inicial do Jogo

## 1. Nome do jogo

404: Paz Nao Encontrada

## 2. Integrantes do grupo

- Bernardo Diniz
- Daniel Heber de Souza Godinho
- Thiago de Castro

## 3. Tipo de jogo

Jogo arcade de sobrevivencia em tres pistas, com movimentacao lateral, obstaculos, consumiveis e pontuacao por tempo.

## 4. Descricao geral do jogo

O jogo "404: Paz Nao Encontrada" tem tematica de programacao. O jogador controla um desenvolvedor tentando encontrar paz depois de um longo dia de trabalho, enquanto problemas do cotidiano de software descem pela tela.

Durante a partida, o jogador deve alternar entre tres pistas para desviar de obstaculos como bugs, conflitos de merge, codigo legado, dependencias quebradas e notificacoes. Consumiveis aparecem ocasionalmente e oferecem vantagens temporarias.

## 5. Objetivo do jogador

Sobreviver o maior tempo possivel, acumular pontos e superar o recorde anterior. Quando a pontuacao final passa o melhor resultado salvo antes da partida, o jogo exibe a mensagem de vitoria "200 OK: Paz Encontrada!".

## 6. Regras principais

- O jogador inicia cada partida com 3 vidas.
- Cada colisao com obstaculo remove 1 vida.
- A pontuacao aumenta em 10 pontos por segundo.
- O consumivel Cafe restaura 1 vida, ate o maximo de 3.
- O consumivel Monster dobra a pontuacao recebida por tempo limitado.
- O consumivel Spotify concede invencibilidade por tempo limitado.
- Apos tomar dano, o jogador fica temporariamente invencivel e os obstaculos desaceleram por alguns segundos.
- A dificuldade aumenta conforme a pontuacao: obstaculos ficam mais rapidos e aparecem com maior frequencia.
- A partida termina quando as vidas chegam a zero.

## 7. Condicao de vitoria

O jogador vence quando termina uma partida com pontuacao maior que o recorde existente antes daquela partida. A tela final mostra "200 OK: Paz Encontrada!".

## 8. Condicao de derrota ou encerramento

A partida termina quando o jogador perde todas as vidas ao colidir com obstaculos. Se a pontuacao final nao superar o recorde anterior, a tela final mostra "404: Paz Nao Encontrada".

O jogador tambem pode encerrar o jogo com `ESC`.

## 9. Elementos do jogo

## Jogador

Um desenvolvedor representado por sprites animados, movendo-se entre tres pistas com o teclado.

## Obstaculos

Imagens relacionadas a problemas de desenvolvimento, como bug, conflito de merge, codigo legado, dependencias quebradas e Slack. Eles surgem no topo da tela, descem pelas pistas e aumentam de tamanho visualmente conforme se aproximam.

## Consumiveis

- Cafe: recupera vida.
- Monster: ativa multiplicador de pontos.
- Spotify: ativa invencibilidade.

## Pontuacao, vidas e progresso

O progresso e medido pela pontuacao acumulada e pelo historico de ranking salvo em `data/ranking.txt`. O jogo tambem salva recorde em `data/recorde.txt`.

## 10. Controles

- `A` ou seta para esquerda: mover para a esquerda.
- `D` ou seta para direita: mover para a direita.
- `Espaco`: iniciar partida, pausar, retomar ou jogar novamente.
- `T`: abrir tutorial na tela inicial.
- `H`: abrir historico na tela inicial.
- `ESC`: voltar, sair da tela atual ou encerrar o jogo.
- Mouse no controle de volume: ajustar volume ou alternar mudo.

## 11. Organizacao do codigo

- `main.py`: ponto de entrada da aplicacao.
- `src/jogo.py`: telas, loop principal, eventos, renderizacao, regras de partida e integracao com audio/dados.
- `src/config.py`: constantes globais, caminhos, tamanhos, FPS, cores e parametros de dificuldade.
- `src/funcoes.py`: funcoes auxiliares de pontuacao, vidas, colisao, obstaculos, consumiveis, HUD e fundo Matrix.
- `src/sprites.py`: carregamento e redimensionamento de sprites.
- `src/dados.py`: leitura e escrita de recorde/ranking.
- `assets/sons/sounds.py`: gerenciamento de musicas, efeitos, pausa, volume e mudo.

## 12. Recursos externos

O projeto utiliza imagens e sons em `assets/`. As musicas e efeitos devem ter origem/licenca documentada quando forem externos. No estado atual, o jogo usa fontes do sistema via Pygame.

## 13. Principais dificuldades

- Implementar colisao consistente entre jogador, obstaculos e consumiveis.
- Controlar spawn aleatorio sem gerar situacoes injustas entre obstaculos e consumiveis.
- Organizar estados de jogo, telas, pausa, tutorial, historico e tela final.
- Integrar audio de forma robusta, permitindo que o jogo continue mesmo sem mixer ou arquivo de som.
- Balancear dificuldade progressiva e efeitos temporarios.

## 14. Escopo minimo para entrega final

A versao minima inclui personagem controlado pelo teclado, tres pistas, obstaculos aleatorios, sistema de vidas, pontuacao por tempo, consumiveis, recorde/ranking, tela inicial, pausa, tutorial, historico, tela de vitoria e tela de derrota.

## 15. Possiveis melhorias

- Tela de configuracoes com volume separado para musica e efeitos.
- Selecao visual de personagem.
- Novos tipos de obstaculos e consumiveis.
- Ranking com nome do jogador.
- Ajustes finos de balanceamento por dificuldade.
