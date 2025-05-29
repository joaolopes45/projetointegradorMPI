import numpy as np
<<<<<<< HEAD
import tifffile as tiff
import cv2
import time
=======
from skimage.measure import label, regionprops
>>>>>>> 1c35f9e1aff0895457423432d7037b0557407f84
import os
from skimage.measure import label, regionprops
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    centroids = [region.centroid for region in props]
<<<<<<< HEAD
    return centroids

def process_tile(tile, x_offset, y_offset):
    centroids = get_star_centroids(tile)
    adjusted = [(cy + y_offset, cx + x_offset) for cy, cx in centroids]
    return adjusted

def process_large_image_parallel(image_path, tile_size=1024, max_workers=8, output_path="imagem_com_estrelas.jpg", show_progress=True):
    start_time = time.time()

    ext = os.path.splitext(image_path)[1].lower()
    print(f"📂 Abrindo imagem: {image_path} (extensão: {ext})")

    if ext in [".tif", ".tiff"]:
        print("🔄 Abrindo TIFF com memmap...")
        with tiff.TiffFile(image_path) as tif:
            page = tif.pages[0]
            shape = page.shape
            is_color = len(shape) == 3
            height, width = shape[:2]
            memmap_img = tif.asarray(out='memmap')
            image = memmap_img
    else:
        print("🔄 Abrindo imagem normal com OpenCV...")
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError(f"Imagem não encontrada ou formato inválido: {image_path}")
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        height, width = image.shape[:2]
        is_color = True

    print(f"📐 Dimensões da imagem: {width} x {height}")
    print(f"🎨 Colorida? {'Sim' if is_color else 'Não'}")

    output_image = np.zeros((height, width, 3), dtype=np.uint8)

    tasks = []
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            y_end = min(y + tile_size, height)
            x_end = min(x + tile_size, width)
            tile_region = image[y:y_end, x:x_end]

            if not is_color:
                tile = cv2.cvtColor(tile_region, cv2.COLOR_GRAY2BGR)
            else:
                tile = tile_region

            tasks.append((tile, x, y))

    total_stars = 0
    print(f"🧵 Iniciando processamento com {max_workers} thread(s)...")

    if max_workers == 8:
        for tile, x, y in tqdm(tasks, desc="Processando tiles", unit="tile"):
            centroids = process_tile(tile, x, y)
            total_stars += len(centroids)
            for cy, cx in centroids:
                cv2.circle(output_image, (int(cx), int(cy)), radius=6, color=(0, 0, 255), thickness=2)
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_tile, tile, x, y) for tile, x, y in tasks]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processando tiles", unit="tile"):
                centroids = future.result()
                total_stars += len(centroids)
                for cy, cx in centroids:
                    cv2.circle(output_image, (int(cx), int(cy)), radius=6, color=(0, 0, 255), thickness=2)

    cv2.imwrite(output_path, output_image)

    elapsed_time = time.time() - start_time
    print(f"✅ Processamento finalizado!")
    print(f"🌟 Total de estrelas detectadas: {total_stars}")
    print(f"⏱️ Tempo total: {elapsed_time:.2f} segundos")

    return elapsed_time, total_stars

def main_speedup_test(image_path, tile_size=1024, max_workers=8, output_path="imagem_com_estrelas.jpg"):
    print("\n🔹 Rodando processo SERIAL (1 thread)...")
    t_serial, stars_serial = process_large_image_parallel(image_path, tile_size, max_workers=1, output_path="serial_" + output_path)

    print("\n🔹 Rodando processo PARALLEL ({} threads)...".format(max_workers))
    t_parallel, stars_parallel = process_large_image_parallel(image_path, tile_size, max_workers=max_workers, output_path="parallel_" + output_path)

    if stars_serial != stars_parallel:
        print("⚠️ Aviso: A contagem de estrelas é diferente entre serial e paralelo!")

    speedup = t_serial / t_parallel if t_parallel > 0 else float('inf')
    efficiency = speedup / max_workers

    print("\n📊 Relatório de Performance:")
    print(f"  Tempo Serial  (1 thread): {t_serial:.2f} s")
    print(f"  Tempo Paralelo ({max_workers} threads): {t_parallel:.2f} s")
    print(f"  Speedup: {speedup:.2f}x")
    print(f"  Eficiência: {efficiency:.2f} (speedup / threads)")
=======
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
>>>>>>> 1c35f9e1aff0895457423432d7037b0557407f84

if __name__ == "__main__":
<<<<<<< HEAD
    caminho_imagem = "imagem_gigante_20GB.tiff"
    main_speedup_test(caminho_imagem, tile_size=1024, max_workers=8)
=======
    caminho_imagem = "starfield_8GB.tiff"  # Altere para sua imagem
    total = visualize_stars(caminho_imagem)
    print(f"🌟 Total de estrelas detectadas: {total}")
>>>>>>> 1c35f9e1aff0895457423432d7037b0557407f84
