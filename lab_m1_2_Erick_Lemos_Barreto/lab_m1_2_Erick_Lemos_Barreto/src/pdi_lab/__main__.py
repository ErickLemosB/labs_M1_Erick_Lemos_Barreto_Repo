import argparse
import os
import sys

from . import operacoes
from .imagem import ErroPdi, carregar_cinza, salvar_cinza

OPERACOES = ("brightness", "contrast", "negative", "threshold", "histogram")

def criar_parser():
    parser = argparse.ArgumentParser(
        prog="pdi_lab",
        description="Laboratório M1.2 - transformações de intensidade",
    )
    parser.add_argument("--input", required=True, help="imagem de entrada")
    parser.add_argument(
        "--output", required=True, help="arquivo de saída (imagem ou CSV)"
    )
    parser.add_argument(
        "--operation", required=True, choices=OPERACOES, help="operação aplicada"
    )
    parser.add_argument("--value", type=int, help="deslocamento b de brightness")
    parser.add_argument("--alpha", type=float, help="ganho alfa de contrast")
    parser.add_argument("--threshold", type=int, help="limiar T de threshold")
    return parser


def escrever_histograma(contagem, caminho):
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    try:
        with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
            arquivo.write("intensity,count\n")
            for intensidade in range(256):
                arquivo.write("%d,%d\n" % (intensidade, contagem[intensidade]))
    except OSError as erro:
        raise ErroPdi("falha ao gravar o histograma %s (%s)" % (caminho, erro))




def executar(args):
    imagem = carregar_cinza(args.input)

    if args.operation == "brightness":
        if args.value is None:
            raise ErroPdi("a operação brightness exige --value")
        salvar_cinza(operacoes.brilho(imagem, args.value), args.output)

    elif args.operation == "contrast":
        if args.alpha is None:
            raise ErroPdi("a operação contrast exige --alpha")
        if args.alpha < 0:
            raise ErroPdi("--alpha deve ser maior ou igual a 0")
        salvar_cinza(operacoes.contraste(imagem, args.alpha), args.output)

    elif args.operation == "negative":
        salvar_cinza(operacoes.negativo(imagem), args.output)

    elif args.operation == "threshold":
        if args.threshold is None:
            raise ErroPdi("a operação threshold exige --threshold")
        if args.threshold < 0 or args.threshold > 255:
            raise ErroPdi("--threshold deve estar entre 0 e 255")
        salvar_cinza(operacoes.limiarizacao(imagem, args.threshold), args.output)

    else:
        escrever_histograma(operacoes.histograma(imagem), args.output)


def main(argv=None):
    args = criar_parser().parse_args(argv)
    try:
        executar(args)
    except ErroPdi as erro:
        print("erro: %s" % erro, file=sys.stderr)
        return 1
    print("saída gravada em %s" % args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
