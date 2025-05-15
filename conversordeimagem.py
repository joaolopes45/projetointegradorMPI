import numpy as np
import tifffile
from PIL import Image

# Carregar imagem base
tile_image = Image.open("./img/imagem.jpg")  # substitua com seu caminho
tile_array = np.array(tile_image)

# Cálculo de cópias necessárias
tile_h, tile_w, channels = tile_array.shape
tile_bytes = tile_h * tile_w * channels
target_bytes = 8 * 1024**3  # 8 GB
tiles_needed = target_bytes // tile_bytes
tiles_per_row = int(np.sqrt(tiles_needed))
tiles_per_col = int(np.ceil(tiles_needed / tiles_per_row))

# Criar TIFF em blocos
with tifffile.TiffWriter("starfield_8GB.tiff", bigtiff=True) as tiff:
    for row in range(tiles_per_col):
        row_tiles = []
        for col in range(tiles_per_row):
            row_tiles.append(tile_array)
        row_stack = np.concatenate(row_tiles, axis=1)
        tiff.write(row_stack, contiguous=True)

print("Imagem TIFF de ~8GB salva como starfield_8GB.tiff")