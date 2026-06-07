def salvar_recorde(caminho_arquivo, pontuacao):
    # Salva a pontuação recorde em arquivo texto
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    # Carrega o recorde salvo; retorna 0 se não existir valor válido
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            return int(conteudo) if conteudo else 0
    except (FileNotFoundError, ValueError):
        return 0


def salvar_ranking(caminho_arquivo, pontuacao):
    # Acrescenta a pontuação ao arquivo de ranking
    with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao) + "\n")


def carregar_melhor_ranking(caminho_arquivo):
    # Retorna a maior pontuação já registrada no ranking; retorna 0 se vazio
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [l.strip() for l in arquivo if l.strip()]
            return max((int(l) for l in linhas), default=0)
    except (FileNotFoundError, ValueError):
        return 0
