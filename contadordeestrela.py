import numpy as np
import tifffile as tiff
import cv2
import time
import os
from skimage.measure import label, regionprops
from tqdm import tqdm

def preprocess_tile(tile):
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)
    return binary

def get_star_centroids(tile):
    binary = preprocess_tile(tile)
    labeled = label(binary)
    props = regionprops(labeled)
    return [region.centroid for region in props]

def process_large_image_sequential(image_path, tile_size=1024, output_path="imagem_gigante_20GB.tiff", delay_per_tile_seconds=0.05):
    # Indica início do carregamento
    print(f"🔄 Carregando imagem: {image_path}")
    start = time.time()

    ext = os.path.splitext(image_path)[1].lower()
    if ext in [".tif", ".tiff"]:
        with tiff.TiffFile(image_path) as tif:
            page = tif.pages[0]
            height, width = page.shape[:2]
            img = tif.asarray(out='memmap')
    else:
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        height, width = img.shape[:2]

    print(f"📐 Dimensões: {width}x{height}")

    print("🧩 Gerando lista de tiles...")
    tiles = []
    ys = list(range(0, height, tile_size))
    xs = list(range(0, width, tile_size))
    for y in tqdm(ys, desc="Linhas", unit="linha"):
        for x in xs:
            tile = img[y:min(y+tile_size, height), x:min(x+tile_size, width)]
            tiles.append((tile, x, y))

    output = np.zeros((height, width, 3), dtype=np.uint8)

    print("▶️ Processando tiles (sequencial)...")
    total_stars_detected = 0
    for tile, x, y in tqdm(tiles, desc="Tiles", unit="tile"):
        centroids = get_star_centroids(tile)
        total_stars_detected += len(centroids)
        for cy, cx in centroids:
            cv2.circle(output, (int(cx)+x, int(cy)+y), 6, (0,0,255), 2)
        
        # Adiciona um pequeno atraso artificial
        time.sleep(delay_per_tile_seconds) # <--- NOVIDADE AQUI!

    cv2.imwrite(output_path, output)
    elapsed = time.time() - start
    print(f"✅ Processamento Sequencial Concluído: {total_stars_detected} estrelas detectadas em {elapsed:.2f} segundos.")
    return elapsed, total_stars_detected

if __name__ == "__main__":
    image_to_process = "imagem_gigante_20GB.tiff" # <-- ALTERE AQUI PARA O CAMINHO DA SUA IMAGEM!
    output_image_name = "resultado_estrelas_sequencial.tiff"
    tile_dimension = 1024
    
    # Novo parâmetro: atraso em segundos por tile.
    # Experimente valores como 0.01, 0.05, 0.1 para ver o efeito.
    delay_per_tile = 0.05 # Atraso de 50 milissegundos por tile

    try:
        process_large_image_sequential(image_to_process, 
                                       tile_size=tile_dimension, 
                                       output_path=output_image_name,
                                       delay_per_tile_seconds=delay_per_tile)
        print(f"Imagem de saída salva em: {output_image_name}")
    except FileNotFoundError as e:
        print(f"Erro: {e}. Por favor, verifique se o caminho da imagem está correto.")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")