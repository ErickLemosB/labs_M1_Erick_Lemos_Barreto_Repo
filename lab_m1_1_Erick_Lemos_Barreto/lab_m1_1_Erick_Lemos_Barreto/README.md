# Laboratório M1.1 — Representação, canais e níveis de cinza

Processamento de Imagens
Linguagem: **Python** (OpenCV) · Aluno: **Erick Lemos Barreto**

Inspecao de imagem, copia de seus pixels,
separacao dos canais de cor e convercao para níveis de cinza (média simples e
ponderada), e quantização em 16/8/4/2 níveis.

## Dependências

- Python >= 3.10
- `opencv-python` — usado apenas como infraestrutura: abrir e salvar imagens
- `numpy` — criação de matrizes e acesso a pixels
- `pytest` — testes

As cinco operações avaliadas (cópia, separação de canais, as duas conversões
para cinza e a quantização) são implementadas manualmente, com percurso
explícito dos pixels — nenhuma função pronta do OpenCV as substitui.

## Preparar o ambiente

```bash
python -m venv .venv
source .venv/bin/activate      # Windows/MSYS2: source .venv/Scripts/activate

python -m pip install -r requirements.txt
```

## Executar

```bash
PYTHONPATH=src python -m pdi_lab --help
```

Forma geral:

```bash
PYTHONPATH=src python -m pdi_lab \
  --input <arquivo> \
  --output <arquivo> \
  --operation <operacao> \
  [--levels N]
```

### Exemplos

```bash
# inspecao (grava um .txt com as estatisticas)
python -m pdi_lab --input images/input/test.png --output images/output/inspect.txt --operation inspect

# copia manual
python -m pdi_lab --input images/input/test.png --output images/output/copy.png --operation copy

# separacao de canais
python -m pdi_lab --input images/input/test.png --output images/output/channel_b.png --operation channel_b
python -m pdi_lab --input images/input/test.png --output images/output/channel_g.png --operation channel_g
python -m pdi_lab --input images/input/test.png --output images/output/channel_r.png --operation channel_r

# niveis de cinza
python -m pdi_lab --input images/input/test.png --output images/output/gray_average.png --operation grayscale_average
python -m pdi_lab --input images/input/test.png --output images/output/gray_weighted.png --operation grayscale_weighted

# quantizacao (a partir de uma imagem ja em niveis de cinza)
python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_16.png --operation quantize --levels 16
python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_8.png  --operation quantize --levels 8
python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_4.png  --operation quantize --levels 4
python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_2.png  --operation quantize --levels 2
```

`images/input/test.png` é uma imagem sintética 160×120 com quatro quadrantes
de cores bem distintas e uma faixa branca tocando a borda superior — útil
para conferir a olho os canais, os níveis de cinza e a quantização.
Substitua-a pelas imagens fornecidas pela disciplina e preserve-as na entrega.

## Argumentos


Argumento = `--input` -> Obrigatório = sim -> descricao = imagem de entrada
Argumento = `--output` -> Obrigatório = sim -> descricao = arquivo de saída (imagem, ou `.txt` para `inspect`)
Argumento = `--operation` -> Obrigatório = sim -> descricao = `inspect`, `copy`, `channel_b`, `channel_g`, `channel_r`, `grayscale_average`, `grayscale_weighted`, `quantize`
Argumento = `--levels` -> Obrigatório = `quantize` -> descricao = número de níveis de cinza, inteiro em `[2, 256]`

## Decisões de implementação

**Ordem dos canais**: o OpenCV lê e grava imagens coloridas na ordem BGR
  (azul, verde, vermelho), por isso `channel_b` corresponde ao índice `0`.
**Cinza — média simples**: `g = (R + G + B) / 3`, arredondado.
**Cinza — média ponderada**: `g = 0,299 R + 0,587 G + 0,114 B`, arredondado
  e saturado em `[0, 255]`.
**Quantização**: `passo = 256 // levels`; cada pixel é mapeado para o
  início da sua faixa (`(pixel // passo) * passo`). Com `levels` em
  `{2, 4, 8, 16}` o passo é sempre exato, o que facilita a conferência manual.
`channel_*`, `grayscale_*` e `quantize` exigem, respectivamente, imagem
  colorida (3 canais) ou em níveis de cinza (1 canal) — uma guarda recusa a
  operação com mensagem clara caso o tipo não bata.

## Códigos de saída

`0` em caso de sucesso; `1` em caso de erro (arquivo não encontrado, imagem
ilegível, número de canais incompatível com a operação, ou `--levels`
ausente/fora de `[2, 256]`).

## Testes

```bash
PYTHONPATH=src python -m pytest
```

Cobrem: cópia exata pixel a pixel (e que não é apenas uma referência), ordem
dos canais na separação, as duas fórmulas de nível de cinza (incluindo o
ponto neutro onde ambas coincidem), quantidade de níveis após a quantização,
valores nos limites `0`/`255`, as guardas de canais/parâmetros inválidos, e a
CLI de ponta a ponta.