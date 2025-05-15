import cv2
import numpy as np
from skimage.measure import label
from concurrent.futures import ProcessPoolExecutor
import os

def preprocess_tile(tile):
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    return binary

def count_stars_in_tile(tile):
    binary = preprocess_tile(tile)
    labeled = label(binary)
    return labeled.max()  # Número de regiões conectadas (estrelas)

def split_image(image, tile_size):
    tiles = []
    h, w = image.shape[:2]
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = image[y:y + tile_size, x:x + tile_size]
            if tile.shape[0] > 10 and tile.shape[1] > 10:  # Ignora pedaços muito pequenos
                tiles.append(tile)
    return tiles

def count_stars_parallel(image_path, tile_size=512):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    tiles = split_image(image, tile_size)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(count_stars_in_tile, tiles))

    total_stars = sum(results)
    return total_stars

# 🧪 Exemplo de uso
if __name__ == "__main__":
    caminho_imagem = "imagem_do_ceu_pesada.jpg"  # Altere para seu arquivo
    estrelas = count_stars_parallel(caminho_imagem)
    print(f"🌟 Total de estrelas detectadas: {estrelas}")
