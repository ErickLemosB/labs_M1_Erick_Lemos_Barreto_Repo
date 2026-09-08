"""Testes do Laboratorio M1.1."""

import cv2
import numpy as np
import pytest

from pdi_lab.main import (
    LabError,
    copy_image,
    extract_channel,
    grayscale_average,
    grayscale_weighted,
    main,
    quantize,
)


def imagem_colorida():
    """Imagem 2x2 em BGR com valores distintos em cada canal e pixel."""
    img = np.zeros((2, 2, 3), dtype=np.uint8)
    img[0, 0] = (10, 20, 30)   # b, g, r
    img[0, 1] = (0, 0, 255)    # vermelho puro
    img[1, 0] = (255, 255, 255)
    img[1, 1] = (0, 0, 0)
    return img


def test_copy_e_identica_pixel_a_pixel():
    img = imagem_colorida()
    saida = copy_image(img)
    assert np.array_equal(saida, img)
    assert not np.shares_memory(saida, img)  # e uma copia de verdade



def test_ordem_dos_canais_b_g_r():
    img = imagem_colorida()  

    canal_b = extract_channel(img, 0)
    assert tuple(canal_b[0, 0]) == (10, 0, 0)

    canal_g = extract_channel(img, 1)
    assert tuple(canal_g[0, 0]) == (0, 20, 0)

    canal_r = extract_channel(img, 2)
    assert tuple(canal_r[0, 0]) == (0, 0, 30)


def test_channel_exige_imagem_colorida():
    cinza = np.zeros((2, 2), dtype=np.uint8)
    with pytest.raises(LabError):
        extract_channel(cinza, 0)



def test_grayscale_average_formula():
    img = np.zeros((1, 1, 3), dtype=np.uint8)
    img[0, 0] = (30, 60, 90)#BGR
    assert grayscale_average(img)[0, 0] == 60


def test_grayscale_weighted_formula():
    img = np.zeros((1, 1, 3), dtype=np.uint8)
    img[0, 0] = (0, 0, 255)
    assert grayscale_weighted(img)[0, 0] == 76


def test_media_e_ponderada_diferem_no_mesmo_pixel():
    """Em pixels nao neutros as duas formulas devem divergir."""
    img = np.zeros((1, 1, 3), dtype=np.uint8)
    img[0, 0] = (0, 0, 255)
    assert grayscale_average(img)[0, 0] != grayscale_weighted(img)[0, 0]


def test_cinza_no_pixel_neutro_e_igual_nas_duas_formulas():
    img = np.zeros((1, 1, 3), dtype=np.uint8)
    img[0, 0] = (128, 128, 128)
    assert grayscale_average(img)[0, 0] == 128
    assert grayscale_weighted(img)[0, 0] == 128


def test_grayscale_exige_imagem_colorida():
    cinza = np.zeros((2, 2), dtype=np.uint8)
    with pytest.raises(LabError):
        grayscale_average(cinza)
    with pytest.raises(LabError):
        grayscale_weighted(cinza)


@pytest.mark.parametrize("levels", [16, 8, 4, 2])
def test_quantize_reduz_a_quantidade_de_niveis(levels):
    rampa = np.arange(256, dtype=np.uint8).reshape(1, 256)  # todas as intensidades
    saida = quantize(rampa, levels)
    assert len(np.unique(saida)) <= levels


def test_quantize_valores_proximos_dos_limites():
    """0 e 255 sao os casos de borda do intervalo valido."""
    img = np.array([[0, 255]], dtype=np.uint8)
    saida = quantize(img, 2)
    assert saida[0, 0] == 0
    assert saida[0, 1] == 128


def test_quantize_exige_imagem_em_niveis_de_cinza():
    colorida = np.zeros((2, 2, 3), dtype=np.uint8)
    with pytest.raises(LabError):
        quantize(colorida, 8)


@pytest.mark.parametrize("levels", [0, 1, 257])
def test_quantize_niveis_invalidos(levels):
    cinza = np.zeros((2, 2), dtype=np.uint8)
    with pytest.raises(LabError):
        quantize(cinza, levels)



def test_cli_arquivo_inexistente(tmp_path):
    codigo = main(
        ["--input", str(tmp_path / "nao_existe.png"), "--output", str(tmp_path / "o.png"), "--operation", "copy"]
    )
    assert codigo != 0


def test_cli_copy_gera_arquivo_identico(tmp_path):
    entrada = tmp_path / "in.png"
    cv2.imwrite(str(entrada), imagem_colorida())

    saida = tmp_path / "sub" / "out.png"
    codigo = main(["--input", str(entrada), "--output", str(saida), "--operation", "copy"])

    assert codigo == 0
    assert saida.exists()
    assert np.array_equal(cv2.imread(str(saida)), imagem_colorida())


def test_cli_quantize_sem_levels(tmp_path):
    entrada = tmp_path / "in.png"
    cv2.imwrite(str(entrada), np.zeros((2, 2), dtype=np.uint8))

    codigo = main(["--input", str(entrada), "--output", str(tmp_path / "o.png"), "--operation", "quantize"])
    assert codigo != 0


def test_cli_inspect_escreve_texto(tmp_path):
    entrada = tmp_path / "in.png"
    cv2.imwrite(str(entrada), imagem_colorida())

    saida = tmp_path / "inspect.txt"
    codigo = main(["--input", str(entrada), "--output", str(saida), "--operation", "inspect"])

    assert codigo == 0
    texto = saida.read_text(encoding="utf-8")
    assert "width=2" in texto
    assert "height=2" in texto
    assert "channels=3" in texto
