from PIL import Image, ImageTk

def load_and_slice_image(image_path, grid_size):
    """
    Carrega uma imagem, a redimensiona e a divide em 8 peças para o puzzle.
    ...
    """
    try:
        original_image = Image.open(image_path)
    except FileNotFoundError:
        # A mensagem de erro agora mostrará o caminho absoluto, o que é ótimo para depuração.
        print(f"Erro: Arquivo de imagem não encontrado em '{image_path}'")
        return None

    resized_image = original_image.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    image_pieces = {}
    tile_width = grid_size // 3
    for i in range(9):
        if i < 8: # Apenas peças de 1 a 8
            puzzle_number = i + 1
            row, col = divmod(i, 3)
            box = (col * tile_width, row * tile_width, (col + 1) * tile_width, (row + 1) * tile_width)
            piece = resized_image.crop(box)
            image_pieces[puzzle_number] = ImageTk.PhotoImage(piece)
    return image_pieces