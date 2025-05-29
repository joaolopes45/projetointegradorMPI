import numpy as np
from PIL import Image
import tifffile
import math
import os

def gerar_imagem_gigante(caminho_imagem, caminho_saida, target_gb=20):
    target_bytes = target_gb * 1024**3

    # Abre e converte para RGB
    imagem = Image.open(caminho_imagem).convert("RGB")
    tile_array = np.array(imagem, dtype=np.uint8)

    tile_h, tile_w, channels = tile_array.shape
    tile_bytes = tile_h * tile_w * channels  # uint8 = 1 byte por canal

    print(f"Imagem original: {tile_w}x{tile_h}px, canais: {channels}, ~{tile_bytes / 1024**2:.2f} MB por cópia")

    # Número total de cópias necessárias
    tiles_needed = target_bytes / tile_bytes
    # Replicação nas duas dimensões - aproximação para distribuir replicações igualmente
    n = math.sqrt(tiles_needed)

    # Separar n em repetições inteiras nas dimensões X e Y, para ficar o mais próximo possível de target_bytes
    n_x = math.ceil(n)
    n_y = math.ceil(tiles_needed / n_x)

    print(f"Objetivo: ~{target_gb} GB → {tiles_needed:.2f} cópias → grade {n_x} x {n_y} = {n_x * n_y} cópias")

    # Construir a imagem final replicando
    linha = np.concatenate([tile_array] * n_x, axis=1)
    final_image = np.concatenate([linha] * n_y, axis=0)

    tamanho_gb = final_image.nbytes / 1024**3
    print(f"Imagem final: {final_image.shape}, tamanho na memória: {tamanho_gb:.2f} GB")

    # Salvar como bigtiff
    tifffile.imwrite(caminho_saida, final_image, bigtiff=True)
    print(f"Imagem gigante salva em: {caminho_saida}")
    print(f"Tamanho do arquivo salvo: {os.path.getsize(caminho_saida) / 1024**3:.2f} GB")

if __name__ == "__main__":
    gerar_imagem_gigante("./img/imagem.jpg", "imagem_gigante_20GB.tiff", target_gb=20)
