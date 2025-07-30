from PIL import Image, ImageTk

def load_and_slice_image(image_path, grid_size):
    """
    Carrega uma imagem, a redimensiona e a divide em 8 peças para o puzzle.

    Args:
        image_path (str): O caminho para o arquivo de imagem.
        grid_size (int): O tamanho (largura e altura) da grade do puzzle em pixels.

    Returns:
        dict: Um dicionário mapeando o número da peça (1-8) para seu objeto
              PhotoImage correspondente, pronto para ser usado no Tkinter.
              Retorna None se a imagem não for encontrada.
    """

    original_image = Image.open(image_path)


    # Redimensiona a imagem para o tamanho da grade do puzzle
    img_redimensionada = original_image.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    
    imagem_pecas = {}
    tile_width = grid_size // 3
    
    # Corta a imagem em uma grade 3x3
    for i in range(9):
        puzzle_number = i + 1
        
        row = i // 3
        col = i % 3
        
        # Define a caixa de corte (left, upper, right, lower)
        left = col * tile_width
        upper = row * tile_width
        right = left + tile_width
        lower = upper + tile_width
        
        box = (left, upper, right, lower)
        piece = img_redimensionada.crop(box)
        
        # Converte a peça da imagem PIL para um formato que o Tkinter entende
        # A peça 9 (i=8) não é usada no dicionário, pois o estado resolvido usa 1-8.
        if puzzle_number <= 8:
            imagem_pecas[puzzle_number] = ImageTk.PhotoImage(piece)
            
    return imagem_pecas