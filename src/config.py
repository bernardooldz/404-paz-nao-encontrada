# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "404: Paz Não Encontrada"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

CAMINHO_RECORDE = "data/recorde.txt"

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
