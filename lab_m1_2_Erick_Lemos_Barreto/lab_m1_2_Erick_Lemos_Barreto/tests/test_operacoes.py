import pytest

from pdi_lab import operacoes
from pdi_lab.__main__ import main
from pdi_lab.imagem import ErroPdi, ImagemCinza, carregar_cinza


def imagem_exemplo():
    return ImagemCinza(4, 2, bytearray([0, 10, 128, 250, 255, 200, 64, 5]))


def test_brilho_positivo_satura_em_255():
    saida = operacoes.brilho(imagem_exemplo(), 30)
    assert list(saida.dados) == [30, 40, 158, 255, 255, 230, 94, 35]


def test_brilho_negativo_satura_em_0():
    saida = operacoes.brilho(imagem_exemplo(), -30)
    assert list(saida.dados) == [0, 0, 98, 220, 225, 170, 34, 0]


def test_contraste_identidade_nao_altera_a_imagem():
    saida = operacoes.contraste(imagem_exemplo(), 1.0)
    assert list(saida.dados) == list(imagem_exemplo().dados)


def test_contraste_reduzido_aproxima_de_128():
    saida = operacoes.contraste(imagem_exemplo(), 0.5)
    assert list(saida.dados) == [64, 69, 128, 189, 192, 164, 96, 67]


def test_contraste_ampliado_afasta_de_128_e_satura():
    saida = operacoes.contraste(imagem_exemplo(), 1.5)
    assert list(saida.dados) == [0, 0, 128, 255, 255, 236, 32, 0]


def test_negativo():
    saida = operacoes.negativo(imagem_exemplo())
    assert list(saida.dados) == [255, 245, 127, 5, 0, 55, 191, 250]


def test_limiarizacao_com_dois_limiares():
    assert list(operacoes.limiarizacao(imagem_exemplo(), 128).dados) == [
        0, 0, 255, 255, 255, 255, 0, 0
    ]
    assert list(operacoes.limiarizacao(imagem_exemplo(), 64).dados) == [
        0, 0, 255, 255, 255, 255, 255, 0
    ]


def test_histograma_conta_todos_os_pixels():
    contagem = operacoes.histograma(imagem_exemplo())
    assert len(contagem) == 256
    assert sum(contagem) == 8
    assert contagem[0] == 1
    assert contagem[255] == 1
    assert contagem[128] == 1
    assert contagem[1] == 0


def test_histograma_apos_limiarizacao_tem_apenas_dois_valores():
    contagem = operacoes.histograma(operacoes.limiarizacao(imagem_exemplo(), 128))
    assert contagem[0] == 4
    assert contagem[255] == 4
    assert sum(contagem) == 8


def test_arquivo_inexistente_gera_erro():
    with pytest.raises(ErroPdi):
        carregar_cinza("images/input/nao_existe.png")


def test_cli_retorna_codigo_diferente_de_zero_em_erro(tmp_path):
    codigo = main([
        "--input", "images/input/nao_existe.png",
        "--output", str(tmp_path / "saida.png"),
        "--operation", "negative",
    ])
    assert codigo == 1


def test_cli_exige_parametro_da_operacao(tmp_path):
    codigo = main([
        "--input", "images/input/sintetica.png",
        "--output", str(tmp_path / "saida.png"),
        "--operation", "brightness",
    ])
    assert codigo == 1


def test_cli_gera_imagem_e_histograma(tmp_path):
    saida = tmp_path / "brilho.png"
    assert main([
        "--input", "images/input/sintetica.png",
        "--output", str(saida),
        "--operation", "brightness",
        "--value", "30",
    ]) == 0
    assert saida.is_file()

    csv = tmp_path / "hist.csv"
    assert main([
        "--input", "images/input/sintetica.png",
        "--output", str(csv),
        "--operation", "histogram",
    ]) == 0
    linhas = csv.read_text(encoding="utf-8").strip().splitlines()
    assert linhas[0] == "intensity,count"
    assert len(linhas) == 257
