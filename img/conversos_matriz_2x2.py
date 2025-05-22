from PIL import Image

def juntar_n_copias_quadraticamente(caminho_imagem, caminho_saida, n):
    """
    Junta n x n cópias da imagem original em uma nova imagem maior.

    :param caminho_imagem: Caminho da imagem original
    :param caminho_saida: Caminho onde a nova imagem será salva
    :param n: Número de cópias por lado (n x n total)
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size

    nova_largura = largura * n
    nova_altura = altura * n

    nova_imagem = Image.new('RGB', (nova_largura, nova_altura))

    for i in range(n):
        for j in range(n):
            nova_imagem.paste(imagem, (j * largura, i * altura))

    nova_imagem.save(caminho_saida)
    print(f"✅ Imagem criada com sucesso com {n*n} cópias: {caminho_saida}")

# Exemplo de uso:
juntar_n_copias_quadraticamente("./img/imagem.jpg", "imagem_quadrada.jpg", n=125)
