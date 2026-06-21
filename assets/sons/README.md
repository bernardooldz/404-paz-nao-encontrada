# Sons

Pasta com musicas, efeitos sonoros e o modulo de audio do jogo.

## Arquivos principais

- `sounds.py`: define `AudioManager` e funcoes auxiliares para inicializar audio, tocar musicas/efeitos, pausar, retomar, ajustar volume e alternar mudo.
- `menu-pause-sound.mp3`: musica usada no menu e pausa, "Chip Mode" - Danijel Zambo
- `cyborg-ninja-kevin-macleod-main-version-7993-03-00.mp3`: musica principal da partida, origem: "Cyborg Ninja" - Kevin MacLeod
- `sound__achievement.wav`: som/musica de vitoria, origem: "Achievement 2" - sonically_sound 
- `death-sound-43894.mp3`: som/musica de derrota, origem: "Videogame Death Sound" - freesound_community
- `hitHurt.wav`: efeito de dano, origem: jsfxr
- `powerUp.wav`: efeito de consumivel, origem: jsfxr

## Observacoes

O audio e inicializado por `executar_jogo()` em `src/jogo.py`. Se o mixer nao estiver disponivel ou algum arquivo esperado faltar, o jogo desativa o audio e continua executando.
