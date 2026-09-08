import os

from PIL import Image, UnidentifiedImageError

class ErroPdi(Exception):
    """caso tenha alg erro de entrada ou formato."""


class ImagemCinza:

    def __init__(self, largura, altura, dados):
        self.largura = largura
        self.altura = altura
        self.dados = dados


def carregar_cinza(caminho):
    if not os.path.isfile(caminho):
        raise ErroPdi("arquivo de input não encontrado: %s" % caminho)

    try:
        foto = Image.open(caminho)
        foto.load()
    except (OSError, UnidentifiedImageError) as erro:
        raise ErroPdi("erro ao abrir a imagem %s (%s)" % (caminho, erro))

    largura, altura = foto.size

    if foto.mode == "L":
        return ImagemCinza(largura, altura, bytearray(foto.tobytes()))

    if foto.mode not in ("RGB", "RGBA"):
        raise ErroPdi(
            "modo de imagem não suportado: %s (são aceitos L, RGB e RGBA)" % foto.mode
        )
#basicamente só implementei suporte pra RGB, RGBA e L que seria o cinza, caso esteja de outra maneira, dá esse erro.

#caso caia nos canais que tenham RBG = converte para cinza assim:
    canais = len(foto.getbands())
    bruto = foto.tobytes()
    dados = bytearray(largura * altura)
    origem = 0
    for posicao in range(largura * altura):
        vermelho = bruto[origem]
        verde = bruto[origem + 1]
        azul = bruto[origem + 2]
        dados[posicao] = (299 * vermelho + 587 * verde + 114 * azul) // 1000
        origem += canais

    return ImagemCinza(largura, altura, dados)


def salvar_cinza(imagem, caminho):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    try:
        saida = Image.frombytes(
            "L", (imagem.largura, imagem.altura), bytes(imagem.dados)
        )
        saida.save(caminho)
    except (OSError, ValueError) as erro:
        raise ErroPdi("falha ao salvar a imagem %s (%s)" % (caminho, erro))
