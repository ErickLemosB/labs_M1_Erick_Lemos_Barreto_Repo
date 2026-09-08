import math

from .imagem import ImagemCinza

#feito para saturar/delimitar os valores entre 0 e 255
def _limitar(valor):
    if valor < 0:
        return 0
    if valor > 255:
        return 255
    return valor



def brilho(imagem, deslocamento):
    saida = bytearray(imagem.largura * imagem.altura)
    for y in range(imagem.altura):
        linha = y * imagem.largura
        for x in range(imagem.largura):
            saida[linha + x] = _limitar(imagem.dados[linha + x] + deslocamento)
    return ImagemCinza(imagem.largura, imagem.altura, saida)
#como na formula passada no md, g(x, y) = f(x, y) + b (deslocamento do brilho)



def contraste(imagem, alfa):
    saida = bytearray(imagem.largura * imagem.altura)
    for y in range(imagem.altura):
        linha = y * imagem.largura
        for x in range(imagem.largura):
            valor = alfa * (imagem.dados[linha + x] - 128) + 128
            saida[linha + x] = _limitar(math.floor(valor + 0.5))
    return ImagemCinza(imagem.largura, imagem.altura, saida)

#novamente, como no md, usado a formula g(x, y) = alfa * (f(x, y) - 128) + 128, com a obs de que o calculo é feito em ponto flutuante
#e o resultado é arredondado para o inteiro mais próximo antes da saturação. .floor


def negativo(imagem):
    saida = bytearray(imagem.largura * imagem.altura)
    for y in range(imagem.altura):
        linha = y * imagem.largura
        for x in range(imagem.largura):
            saida[linha + x] = 255 - imagem.dados[linha + x]
    return ImagemCinza(imagem.largura, imagem.altura, saida)

#aqui usei a formula do md tbm, g(x, y) = 255 - f(x, y)

def limiarizacao(imagem, limiar):
    saida = bytearray(imagem.largura * imagem.altura)
    for y in range(imagem.altura):
        linha = y * imagem.largura
        for x in range(imagem.largura):
            if imagem.dados[linha + x] < limiar:
                saida[linha + x] = 0
            else:
                saida[linha + x] = 255
    return ImagemCinza(imagem.largura, imagem.altura, saida)

#formula g(x, y) = 0 se f(x, y) < T, senão 255, mesma leitura de sempre, aplicando uma fórumula diferente.


def histograma(imagem):
    contagem = [0] * 256
    for y in range(imagem.altura):
        linha = y * imagem.largura
        for x in range(imagem.largura):
            contagem[imagem.dados[linha + x]] += 1
    return contagem
#contando quiantos pixels tem em cada intensidade