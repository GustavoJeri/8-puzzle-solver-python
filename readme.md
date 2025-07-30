# 8-Puzzle Solver com Lógica SAT

Este projeto é uma aplicação de desktop com interface gráfica que resolve o clássico quebra-cabeça de 8 peças (8-Puzzle). A principal característica deste solver é a utilização de um Resolvedor de Satisfatibilidade Booleana (SAT Solver) para modelar e encontrar a solução para o quebra-cabeça.

A aplicação permite ao usuário embaralhar o quebra-cabeça e, em seguida, invocar o solver SAT para encontrar a sequência de movimentos mais curta que leva ao estado resolvido. A solução é então exibida através de uma animação visual das peças se movendo.

## Funcionalidades

- **Interface Gráfica Intuitiva:** Desenvolvida com `Tkinter` para uma experiência de usuário simples e direta.
- **Visualização com Imagem:** O quebra-cabeça é renderizado usando uma imagem personalizada, que é dividida em 8 peças, tornando a visualização mais agradável.
- **Lógica Baseada em SAT:** Utiliza a biblioteca `PySAT` para modelar as regras do jogo (estados, movimentos, transições) como um problema de satisfatibilidade booleana.
- **Resolução Passo a Passo:** O solver tenta encontrar uma solução incrementando o número máximo de passos permitidos, garantindo a solução mais curta.
- **Animação da Solução:** Após encontrar uma solução, o aplicativo anima a sequência de movimentos, mostrando visualmente como o quebra-cabeça é resolvido.

## Estrutura do Projeto

O projeto segue uma arquitetura bem definida para separar responsabilidades (Model-View-Controller), facilitando a manutenção e a testabilidade:

-   **`main.py`**: O ponto de entrada da aplicação.
-   **`solver_sat/`**: O **Model**, contendo toda a lógica pura do resolvedor SAT.
    -   `core.py`: Encapsula a modelagem do problema, a geração de cláusulas e a interface com o `PySAT`.
-   **`gui/`**: A **View/Controller**, responsável por toda a interface gráfica e interação com o usuário.
    -   `app.py`: A classe principal da aplicação Tkinter.
    -   `image_handler.py`: Módulo responsável por carregar e fatiar a imagem do quebra-cabeça.
    -   `puzzle_image.png`: A imagem padrão usada para o quebra-cabeça.

## Pré-requisitos

-   Python 3.6 ou superior

## Instalação

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

**1. Instale as Dependências**

Todas as dependências necessárias estão listadas no arquivo `requirements.txt`. Para instalá-las, execute o seguinte comando em um terminal:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` deve conter:
```
Pillow
pysat
```

## Como Usar

Inicie a aplicação executando o arquivo `main.py` na raiz do projeto:

```bash
python main.py
```

Ou dê "run" pelo vscode o arquivo `main.py`,

A janela do aplicativo será aberta. Siga as instruções abaixo:

1.  **Embaralhar:** Clique no botão **"Embaralhar"** para gerar um novo quebra-cabeça aleatório.
2.  **Resolver:** Clique no botão **"Resolver (SAT)"** para iniciar o processo de resolução. O solver tentará encontrar uma solução no menor número de passos possível (até um limite pré-definido no código).
3.  **Animação:** Aguarde a conclusão do solver. Se uma solução for encontrada, a sequência de movimentos será animada na tela.

**Nota:** O solver SAT pode levar de alguns segundos, dependendo da complexidade do quebra-cabeça e da velocidade do seu computador. A interface indicará que o solver está "pensando".

## Personalização

Para usar sua própria imagem no quebra-cabeça, basta substituir o arquivo `gui/puzzle_image.png` por qualquer outra imagem quadrada (PNG ou JPG) de sua preferência. O aplicativo a redimensionará e a fatiará automaticamente.