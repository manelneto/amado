# Amado

Este projeto foi desenvolvido no âmbito da Unidade Curricular **Inteligência Artificial (IA)** do 2º semestre do 3º ano da **Licenciatura em Engenharia Informática e Computação (LEIC)** da **Faculdade de Engenharia da Universidade do Porto (FEUP)**, no ano letivo 2023/2024.

## Identificação do Grupo

Grupo: **Group A1_42**

* António Marujo Rama - up202108801
* Manuel Ramos Leite Carvalho Neto - up202108744
* Matilde Isabel da Silva Simões - up202108782

## Como correr o programa

Para iniciar o jogo, é necessário instalar a biblioteca `pygame` e correr os comandos:
```bash
pip install pygame
python main.py
```

Para ter acesso à análise dos algoritmos, é necessário instalar a biblioteca `memory_profiler` e correr os comandos:
```bash
pip install memory_profiler
python analysis.py
```

## Como usar o programa

O jogo começa com um menu no qual o jogador pode escolher o nível que pretende jogar. Existem 10 níveis com diferentes dificuldades, sendo que o nível 1 é o mais fácil e o nível 10 é o mais difícil. Para selecionar o nível pretendido, usam-se as setas do teclado e, para confirmar a seleção, usa-se a tecla *Enter*.

![Menu](photos/mainMenu.png)

Após a seleção do nível, o jogador é redirecionado para a página do jogo, onde encontra o tabuleiro inicial (à esquerda), que deve corresponder ao tabuleiro final (exibido à direita). Para mover o cursor, o jogador utiliza as setas do teclado, sendo o quadrado com bordas verdes o atualmente selecionado. Do lado esquerdo do separador, também é observado o número de movimentos realizados até ao momento. À direita, juntamente com os algoritmos disponíveis para selecionar, existe a opção de solicitar dicas sobre como resolver o jogo, estando tudo isto acessível através do rato. É possível sair do nível pressionando a tecla *ESC*.

![Jogo](photos/game.png)

Depois de escolher um algoritmo para resolver o nível, o jogador pode interagir com o programa. Pode, assim, utilizar as setas representadas no ecrã para realizar o movimento anterior ou o seguinte, clicar em *Auto Run* para visualizar a resolução do nível automaticamente, ou clicar em *Exit Algorithm* para sair do menu do algoritmo e voltar a jogar manualmente.

![Algoritmo](photos/runAlgorithms.png)

Ao selecionar algoritmos com profundidade limitada, é pedido que o jogador indique a profundidade máxima que deseja. Se for selecionado um algoritmo que utiliza heurísticas, é solicitada ao jogador a escolha da heurística a utilizar.

![Profundidade](photos/depth.png)
![Heurística](photos/heuristic.png)

Ao clicar na opção de dicas *Hint*, é fornecida a melhor jogada a realizar.

![Dicas](photos/hint.png)

Quando o jogador termina o nível, é redirecionado para a página de conclusão do nível, onde é possível visualizar o número de movimentos realizados, representado pelo *Score*. Para voltar ao menu principal, o jogador deve pressionar a tecla *ESC* e, aí, pode escolher um novo nível.

![Conclusão](photos/finalMenu.png)
