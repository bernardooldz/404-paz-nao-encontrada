# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "404: Paz Não Encontrada"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_RANKING = "data/ranking.txt"

PONTOS_POR_SEGUNDO = 10  # pontos ganhos a cada segundo sobrevivido

# Colunas do jogador (posições X centrais)
COLUNAS = [LARGURA_TELA // 4, LARGURA_TELA // 2, 3 * LARGURA_TELA // 4]

# Animação do personagem
DIR_PERSONAGEM = "assets/imagens/personagem-principal"
TAMANHO_PERSONAGEM = (80, 120)
FPS_ANIMACAO = 8
DURACAO_VIRAR = 15

# Obstáculos
DIR_OBSTACULOS = "assets/imagens/obstaculos"
TAMANHO_OBSTACULO_MIN = 30   # tamanho ao nascer ("longe")
TAMANHO_OBSTACULO_MAX = 110  # tamanho ao chegar na base ("perto")
INTERVALO_SPAWN = 90         # frames entre cada novo obstáculo
VELOCIDADE_OBSTACULO = 3     # pixels por frame que desce

# Sistema de vidas e dano
DIR_SISTEMA = "assets/imagens/sistema"
TAMANHO_CORACAO = (36, 36)
DURACAO_DANO = 120           # frames que o efeito de dano dura (~2s)
VELOCIDADE_SLOW = 1          # velocidade dos obstáculos durante o slow
INTERVALO_PISCAR = 8         # frames entre cada piscar do personagem

# Consumíveis
DIR_CONSUMIVEIS = "assets/imagens/consumiveis"
TAMANHO_CONSUMIVEL = (50, 68)
INTERVALO_SPAWN_CONSUMIVEL = 300  # frames entre tentativas de spawn (~5s)
VELOCIDADE_CONSUMIVEL = 3
DURACAO_EFEITO = 300              # frames que o efeito dura (~5s)
DURACAO_FRAME_USO = 40            # frames que o sprite de "usando item" fica visível

# Cores dos efeitos ativos (sobreposição semitransparente na tela)
COR_EFEITO_CAFE    = (255, 200,  50,  35)  # dourado
COR_EFEITO_MONSTER = ( 80, 220,  80,  35)  # verde
COR_EFEITO_SPOTIFY = (140,  60, 220,  35)  # roxo
