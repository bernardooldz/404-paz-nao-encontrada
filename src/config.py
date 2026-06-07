# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "404: Paz Não Encontrada"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212,212,212)

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"

# Colunas do jogador (posições X centrais)
COLUNAS = [LARGURA_TELA // 4, LARGURA_TELA // 2, 3 * LARGURA_TELA // 4]

# Animação do personagem
DIR_PERSONAGEM = "assets/imagens/personagem-principal"
TAMANHO_PERSONAGEM = (80, 120)
FPS_ANIMACAO = 8
DURACAO_VIRAR = 15