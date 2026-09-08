from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

operacoes = [
    "channel_b",
    "channel_g",
    "channel_r",
    "copy",
    "inspect",
    "grayscale_average",
    "grayscale_weighted",
    "quantize",
]


class LabError(Exception):
    """Erro tratado: a mensagem e exibida e o programa encerra com codigo 1."""


def inspect(img: np.ndarray) -> str:
    
    #montagem do texto com info pedida
    
    height, width = img.shape[:2]
    channels = 1 if img.ndim == 2 else img.shape[2]

    linhas = [
        f"width={width}",
        f"height={height}",
        f"channels={channels}",
        f"type={img.dtype}",
        f"pixels={width * height}",
    ]

    if channels == 1:
        linhas += [f"min={img.min()}", f"max={img.max()}", f"mean={img.mean():.4f}"]
    else:
        for nome, indice in (("b", 0), ("g", 1), ("r", 2)):
            canal = img[:, :, indice]
            linhas += [
                f"min_{nome}={canal.min()}",
                f"max_{nome}={canal.max()}",
                f"mean_{nome}={canal.mean():.4f}",
            ]

    return "\n".join(linhas) + "\n"


def copy_image(img: np.ndarray) -> np.ndarray:
    height, width = img.shape[:2]
    saida = np.zeros_like(img)
    for y in range(height): #cópia pixel a pixel
        for x in range(width):
            saida[y, x] = img[y, x]
    return saida


def extract_channel(img: np.ndarray, indice: int) -> np.ndarray:
    if img.ndim != 3 or img.shape[2] != 3: #mantem o indice
        raise LabError("esta operacao exige uma imagem colorida com 3 canais")

    height, width = img.shape[:2]
    saida = np.zeros_like(img)
    for y in range(height):
        for x in range(width):
            saida[y, x, indice] = img[y, x, indice]
    return saida


def grayscale_average(img: np.ndarray) -> np.ndarray:
    if img.ndim != 3 or img.shape[2] != 3:
        raise LabError("esta operacao exige uma imagem colorida com 3 canais")

    height, width = img.shape[:2]
    saida = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            b, g, r = img[y, x]
            saida[y, x] = round((int(r) + int(g) + int(b)) / 3) #RGB/3 pixel a pixel
    return saida


def grayscale_weighted(img: np.ndarray) -> np.ndarray:
    if img.ndim != 3 or img.shape[2] != 3:
        raise LabError("esta operacao exige uma imagem colorida com 3 canais")

    height, width = img.shape[:2]
    saida = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            b, g, r = img[y, x]
            valor = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b) #calculo para o peso da escala do cinza
            saida[y, x] = min(255, max(0, round(valor)))
    return saida


def quantize(img: np.ndarray, levels: int) -> np.ndarray:
    if img.ndim != 2:
        raise LabError("a quantizacao exige uma imagem em niveis de cinza (1 canal)")
    if levels < 2 or levels > 256:
        raise LabError(f"--levels deve estar entre 2 e 256, recebi {levels}")

    passo = 256 // levels
    height, width = img.shape
    saida = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            faixa = int(img[y, x]) // passo
            saida[y, x] = min(255, faixa * passo)
    return saida


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdi_lab", description="Laboratorio M1.1 - representacao, canais e niveis de cinza."
    )
    parser.add_argument("--input", required=True, help="imagem de entrada")
    parser.add_argument("--output", required=True, help="arquivo de saida")
    parser.add_argument("--operation", required=True, choices=operacoes)
    parser.add_argument("--levels", type=int, default=None, help="niveis para --operation quantize")
    return parser

#argumentos para executar.



def run(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    if not input_path.is_file():
        raise LabError(f"arquivo de entrada nao encontrado: {input_path}")

    img = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise LabError(f"nao foi possivel abrir a imagem: {input_path}")
    if img.ndim == 3 and img.shape[2] not in (1, 3):
        raise LabError(f"numero de canais nao suportado: {img.shape[2]}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.operation == "inspect":
        texto = inspect(img)
        output_path.write_text(texto, encoding="utf-8")
        print(texto, end="")
        return

    operacoes_de_imagem = {
        "copy": lambda: copy_image(img),
        "channel_b": lambda: extract_channel(img, 0),
        "channel_g": lambda: extract_channel(img, 1),
        "channel_r": lambda: extract_channel(img, 2),
        "grayscale_average": lambda: grayscale_average(img),
        "grayscale_weighted": lambda: grayscale_weighted(img),
    }

    if args.operation == "quantize":
        if args.levels is None:
            raise LabError("a operacao 'quantize' exige --levels")
        resultado = quantize(img, args.levels)
    else:
        resultado = operacoes_de_imagem[args.operation]()

    if not cv2.imwrite(str(output_path), resultado):
        raise LabError(f"falha ao salvar a imagem em: {output_path}")
    print(f"ok: {args.operation} -> {output_path}")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except LabError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())