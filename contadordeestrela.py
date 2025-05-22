import cv2
import numpy as np
from skimage.measure import label, regionprops
import os

def preprocess_tile(tile):
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    return binary

def get_star_centroids(tile):
    binary = preprocess_tile(tile)
    labeled = label(binary)
    props = regionprops(labeled)
    centroids = [region.centroid for region in props]
    return centroids  # Lista de (y, x)

def split_image_with_coords(image, tile_size):
    tiles = []
    coords = []
    h, w = image.shape[:2]
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = image[y:y + tile_size, x:x + tile_size]
            if tile.shape[0] > 10 and tile.shape[1] > 10:
                tiles.append(tile)
                coords.append((y, x))  # Coordenadas iniciais do tile na imagem original
    return tiles, coords

def visualize_stars(image_path, tile_size=512, output_path="imagem_com_estrelas.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

    image_copy = image.copy()
    tiles, coords = split_image_with_coords(image, tile_size)
    total_stars = 0

    for tile, (offset_y, offset_x) in zip(tiles, coords):
        centroids = get_star_centroids(tile)
        total_stars += len(centroids)
        for cy, cx in centroids:
            global_x = int(cx + offset_x)
            global_y = int(cy + offset_y)
            # Desenhar círculos maiores para os centros das estrelas detectadas
            cv2.circle(image_copy, (global_x, global_y), radius=6, color=(0, 0, 255), thickness=2)

    cv2.imwrite(output_path, image_copy)
    print(f"✅ Imagem com estrelas salva em: {output_path}")
    return total_stars

# 🧪 Exemplo de uso
if __name__ == "__main__":
    caminho_imagem = "starfield_8GB.tiff"  # Altere para sua imagem
    total = visualize_stars(caminho_imagem)
    print(f"🌟 Total de estrelas detectadas: {total}")
