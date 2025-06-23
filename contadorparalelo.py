import numpy as np
import tifffile as tiff
import cv2
import time
import os
from skimage.measure import label, regionprops
from tqdm import tqdm
import multiprocessing

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

def process_tile_wrapper(args):
    tile, x, y = args
    centroids = get_star_centroids(tile)
    return x, y, centroids

def process_large_image_parallel(image_path, tile_size=1024, output_path="resultado_estrelas_paralelo.tiff", num_threads=4, chunk_size=10):
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

    print(f"📐 Dimensões da imagem: {width}x{height}")
    print(f"⚙️ Usando {num_threads} threads para processamento paralelo.")

    tiles_data = []
    ys = list(range(0, height, tile_size))
    xs = list(range(0, width, tile_size))
    for y in ys:
        for x in xs:
            tile = img[y:min(y+tile_size, height), x:min(x+tile_size, width)]
            tiles_data.append((tile, x, y))

    output = np.zeros((height, width, 3), dtype=np.uint8)
    total_stars_detected = 0

    print("▶️ Processando tiles (paralelo)...")

    with multiprocessing.Pool(processes=num_threads) as pool:
        # chunk_size ajuda a controlar quantas tarefas cada thread pega por vez
        results = pool.imap_unordered(process_tile_wrapper, tiles_data, chunksize=chunk_size)

        for x_coord, y_coord, centroids in tqdm(results, total=len(tiles_data), desc="Tiles Processados", unit="tile"):
            total_stars_detected += len(centroids)
            for cy, cx in centroids:
                cv2.circle(output, (int(cx)+x_coord, int(cy)+y_coord), 6, (0,0,255), 2)

    cv2.imwrite(output_path, output)
    elapsed = time.time() - start
    print(f"✅ Processamento Paralelo Concluído: {total_stars_detected} estrelas detectadas em {elapsed:.2f} segundos.")
    return elapsed, total_stars_detected

if __name__ == "__main__":
    image_to_process = "imagem_gigante_20GB.tiff"  # altere aqui o caminho da sua imagem
    output_image_name_parallel = "resultado_estrelas_paralelo.tiff"
    tile_dimension = 1024

    # Defina quantas threads quer usar (ex: 2, 4, 6, 8, 16)
    num_parallel_threads = 4

    elapsed, stars = process_large_image_parallel(
        image_to_process,
        tile_size=tile_dimension,
        output_path=output_image_name_parallel,
        num_threads=num_parallel_threads,
        chunk_size=10  # ajuste aqui pra controlar a granularidade
    )
    print(f"Imagem salva em: {output_image_name_parallel}")
