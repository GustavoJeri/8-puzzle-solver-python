from PIL import Image, ImageTk, ImageDraw, ImageFont

def carregar_e_fatiar_imagem(caminho_da_imagem, tamanho_da_grade):
    """
    Carrega uma imagem, a divide em 9 peças e desenha um número em cada uma.

    Parametros:
        caminho_da_imagem (str): O caminho para o arquivo de imagem.
        tamanho_da_grade (int): O tamanho (largura e altura) da grade do puzzle.

    Retorno:
            Um dicionário que mapeia o número da peça (0-8) para seu
            objeto PhotoImage, pronto para ser usado no Tkinter.
            Retorna None se a imagem não for encontrada.
    """
    
    # Tenta abrir o arquivo de imagem. Se não encontrar, retorna None.
    try:
        imagem_original = Image.open(caminho_da_imagem)
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{caminho_da_imagem}'")
        return None

    # Redimensiona a imagem para o tamanho exato da grade do quebra-cabeça
    imagem_redimensionada = imagem_original.resize((tamanho_da_grade, tamanho_da_grade), Image.Resampling.LANCZOS)
    
    # Dicionário para armazenar as peças finais com as imagens
    pecas_de_imagem = {}
    
    # Calcula a largura de cada peça individual (a grade é 3x3)
    largura_da_peca = tamanho_da_grade // 3
    
    # Carrega uma fonte para desenhar os números.
    fonte = ImageFont.truetype("arial.ttf", size=32)

    # Itera sobre as 9 posições da grade (0 a 8)
    for indice in range(9):
        numero_da_peca = indice
        
        # Calcula a linha e a coluna da peça atual na grade 3x3
        linha = indice // 3
        coluna = indice % 3
        
        # Define a caixa (box) para cortar a peça da imagem redimensionada
        caixa_de_corte = (coluna * largura_da_peca, linha * largura_da_peca, (coluna + 1) * largura_da_peca, (linha + 1) * largura_da_peca)
        peca = imagem_redimensionada.crop(caixa_de_corte)
        
        # Prepara para desenhar na peça que acabamos de cortar
        desenhador = ImageDraw.Draw(peca)
        texto_do_numero = str(numero_da_peca)
        
        # Calcula o tamanho do texto para poder centralizá-lo
        caixa_delimitadora_texto = desenhador.textbbox((0, 0), texto_do_numero, font=fonte)
        largura_do_texto = caixa_delimitadora_texto[2] - caixa_delimitadora_texto[0]
        altura_do_texto = caixa_delimitadora_texto[3] - caixa_delimitadora_texto[1]

        # Calcula a posição (x, y) para o canto superior esquerdo do texto, para que ele fique centralizado
        posicao_x = (largura_da_peca - largura_do_texto) / 2
        posicao_y = (largura_da_peca - altura_do_texto) / 2
        
        # Desenha uma "sombra" preta para o texto, garantindo que ele seja legível
        cor_da_sombra = "black"
        desenhador.text((posicao_x - 1, posicao_y - 1), texto_do_numero, font=fonte, fill=cor_da_sombra)
        desenhador.text((posicao_x + 1, posicao_y - 1), texto_do_numero, font=fonte, fill=cor_da_sombra)
        desenhador.text((posicao_x - 1, posicao_y + 1), texto_do_numero, font=fonte, fill=cor_da_sombra)
        desenhador.text((posicao_x + 1, posicao_y + 1), texto_do_numero, font=fonte, fill=cor_da_sombra)
        
        # Desenha o texto principal em branco sobre a sombra
        desenhador.text((posicao_x, posicao_y), texto_do_numero, font=fonte, fill="white")
        
        # Converte a peça (agora com o número desenhado) para um formato que o Tkinter entende
        pecas_de_imagem[numero_da_peca] = ImageTk.PhotoImage(peca)
            
    return pecas_de_imagem