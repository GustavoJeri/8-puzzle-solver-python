from PIL import Image, ImageTk, ImageDraw, ImageFont

def load_and_slice_image(image_path, grid_size):
    """
    Carrega uma imagem, a divide em 9 peças, e desenha um número em cada uma.

    Retorna um dicionário mapeando o número da peça (0-8) para seu objeto PhotoImage.
    """
    try:
        original_image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Erro: Arquivo de imagem não encontrado em '{image_path}'")
        return None

    resized_image = original_image.resize((grid_size, grid_size), Image.Resampling.LANCZOS)
    
    image_pieces = {}
    tile_width = grid_size // 3
    
    font = ImageFont.truetype("arial.ttf", size=32)

    for i in range(9):
        puzzle_number = i
        
        row = i // 3
        col = i % 3
        
        box = (col * tile_width, row * tile_width, (col + 1) * tile_width, (row + 1) * tile_width)
        piece = resized_image.crop(box)
        
        draw = ImageDraw.Draw(piece)
        text = str(puzzle_number)
        
        try:
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
             text_width, text_height = draw.textsize(text, font)

        text_x = (tile_width - text_width) / 2
        text_y = (tile_width - text_height) / 2
        
        shadow_color = "black"
        draw.text((text_x - 1, text_y - 1), text, font=font, fill=shadow_color)
        draw.text((text_x + 1, text_y - 1), text, font=font, fill=shadow_color)
        draw.text((text_x - 1, text_y + 1), text, font=font, fill=shadow_color)
        draw.text((text_x + 1, text_y + 1), text, font=font, fill=shadow_color)
        
        draw.text((text_x, text_y), text, font=font, fill="white")
        
        image_pieces[puzzle_number] = ImageTk.PhotoImage(piece)
            
    return image_pieces