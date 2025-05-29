import numpy as np
from PIL import Image
import tifffile
import math
import os

def gerar_imagem_tiff_8GB(caminho_imagem, caminho_saida, target_gb=8):
    # Tamanho alvo em bytes
    target_bytes = target_gb * 1024**3

    # Carrega a imagem e converte para RGB
    imagem = Image.open(caminho_imagem).convert("RGB")
    tile_array = np.array(imagem)

    tile_h, tile_w, channels = tile_array.shape
    tile_bytes = tile_h * tile_w * channels

    # Quantas cópias são necessárias
    tiles_needed = target_bytes // tile_bytes
    n = math.ceil(math.sqrt(tiles_needed))  # n x n cópias

    print(f"📐 Imagem original: {tile_w}x{tile_h}px")
    print(f"🎯 Objetivo: ~{target_gb} GB -> {tiles_needed} cópias -> grade {n} x {n}")

    # Gera a imagem final
    row_arrays = [np.concatenate([tile_array] * n, axis=1) for _ in range(n)]
    final_image = np.concatenate(row_arrays, axis=0)

    print(f"🖼️ Imagem final: {final_image.shape} (~{final_image.nbytes / 1024**3:.2f} GB)")

    # Salva como TIFF (BigTIFF)
    tifffile.imwrite(caminho_saida, final_image, bigtiff=True)
    print(f"✅ Imagem TIFF salva em: {caminho_saida}")

# Exemplo de uso:
gerar_imagem_tiff_8GB("./img/imagem.jpg", "starfield_8GB.tiff")
