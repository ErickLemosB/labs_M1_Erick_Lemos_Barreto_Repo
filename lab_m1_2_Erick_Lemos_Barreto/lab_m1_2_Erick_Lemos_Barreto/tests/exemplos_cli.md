# Exemplos de execução — pdi_lab

Roteiro de comandos para exercitar manualmente a linha de comando do laboratório
M1.2. Todos os caminhos são relativos à raiz do projeto e todos os comandos
assumem o ambiente virtual já ativado:

```bash
.venv\Scripts\activate            # cmd / PowerShell
# source .venv/Scripts/activate   # Git Bash
```

Forma geral:

```bash
python -m pdi_lab --input <arquivo> --output <arquivo> --operation <operacao> [parametro]
```

Imagens disponíveis em `images/input/`: `cabana.jpg`, `cachorro.jpg`,
`estatua.jpg`, `mao.jpg` e `sintetica.png`.

---

## 1. Brilho (`brightness --value`)

Valor positivo clareia, negativo escurece.

```bash
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_mais30.png    --operation brightness --value 30
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_mais60.png    --operation brightness --value 60
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_mais120.png   --operation brightness --value 120
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_menos30.png   --operation brightness --value -30
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_menos60.png   --operation brightness --value -60
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_brilho_menos120.png  --operation brightness --value -120

python -m pdi_lab --input images/input/cachorro.jpg --output images/output/cachorro_brilho_mais50.png  --operation brightness --value 50
python -m pdi_lab --input images/input/estatua.jpg  --output images/output/estatua_brilho_menos40.png  --operation brightness --value -40
python -m pdi_lab --input images/input/mao.jpg      --output images/output/mao_brilho_mais80.png       --operation brightness --value 80
```

## 2. Contraste (`contrast --alpha`)

`alfa < 1` reduz, `alfa = 1` é identidade, `alfa > 1` amplia.

```bash
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_contraste_0_3.png   --operation contrast --alpha 0.3
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_contraste_0_5.png   --operation contrast --alpha 0.5
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_contraste_1_0.png   --operation contrast --alpha 1.0
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_contraste_1_5.png   --operation contrast --alpha 1.5
python -m pdi_lab --input images/input/cabana.jpg   --output images/output/cabana_contraste_2_5.png   --operation contrast --alpha 2.5

python -m pdi_lab --input images/input/cachorro.jpg --output images/output/cachorro_contraste_1_8.png --operation contrast --alpha 1.8
python -m pdi_lab --input images/input/estatua.jpg  --output images/output/estatua_contraste_0_6.png  --operation contrast --alpha 0.6
python -m pdi_lab --input images/input/mao.jpg      --output images/output/mao_contraste_2_0.png      --operation contrast --alpha 2.0
```

O caso `--alpha 1.0` serve de verificação: a fórmula `g = alfa * (f - 128) + 128`
deve devolver a imagem original.

## 3. Negativo (`negative`)

Não recebe parâmetro adicional.

```bash
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_negativo.png    --operation negative
python -m pdi_lab --input images/input/cachorro.jpg  --output images/output/cachorro_negativo.png  --operation negative
python -m pdi_lab --input images/input/estatua.jpg   --output images/output/estatua_negativo.png   --operation negative
python -m pdi_lab --input images/input/mao.jpg       --output images/output/mao_negativo.png       --operation negative
python -m pdi_lab --input images/input/sintetica.png --output images/output/sintetica_negativo.png --operation negative
```

## 4. Limiarização (`threshold --threshold 0-255`)

```bash
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_limiar_060.png    --operation threshold --threshold 60
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_limiar_100.png    --operation threshold --threshold 100
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_limiar_128.png    --operation threshold --threshold 128
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_limiar_160.png    --operation threshold --threshold 160
python -m pdi_lab --input images/input/cabana.jpg    --output images/output/cabana_limiar_200.png    --operation threshold --threshold 200

python -m pdi_lab --input images/input/mao.jpg       --output images/output/mao_limiar_120.png       --operation threshold --threshold 120
python -m pdi_lab --input images/input/estatua.jpg   --output images/output/estatua_limiar_140.png   --operation threshold --threshold 140
python -m pdi_lab --input images/input/sintetica.png --output images/output/sintetica_limiar_128.png --operation threshold --threshold 128
```

## 5. Histograma (`histogram`)

A saída é um CSV com cabeçalho e 256 linhas de dados, não uma imagem.

```bash
python -m pdi_lab --input images/input/cabana.jpg    --output results/hist_cabana_original.csv   --operation histogram
python -m pdi_lab --input images/input/cachorro.jpg  --output results/hist_cachorro_original.csv --operation histogram
python -m pdi_lab --input images/input/estatua.jpg   --output results/hist_estatua_original.csv  --operation histogram
python -m pdi_lab --input images/input/mao.jpg       --output results/hist_mao_original.csv      --operation histogram
python -m pdi_lab --input images/input/sintetica.png --output results/hist_sintetica.csv         --operation histogram
```

## 6. Encadeamento — histograma das imagens transformadas

A saída de um comando vira a entrada do seguinte. **Requer que os comandos das
seções 1 a 4 já tenham sido executados.**

```bash
python -m pdi_lab --input images/output/cabana_brilho_mais60.png   --output results/hist_cabana_brilho_mais60.csv   --operation histogram
python -m pdi_lab --input images/output/cabana_brilho_menos60.png  --output results/hist_cabana_brilho_menos60.csv  --operation histogram
python -m pdi_lab --input images/output/cabana_contraste_0_5.png   --output results/hist_cabana_contraste_0_5.csv   --operation histogram
python -m pdi_lab --input images/output/cabana_contraste_1_5.png   --output results/hist_cabana_contraste_1_5.csv   --operation histogram
python -m pdi_lab --input images/output/cabana_negativo.png        --output results/hist_cabana_negativo.csv        --operation histogram
python -m pdi_lab --input images/output/cabana_limiar_100.png      --output results/hist_cabana_limiar_100.csv      --operation histogram
python -m pdi_lab --input images/output/sintetica_negativo.png     --output results/hist_sintetica_negativo.csv     --operation histogram
```

O histograma da imagem limiarizada é o mais ilustrativo: todas as 256 linhas
ficam em zero, exceto as intensidades `0` e `255`, porque a limiarização só
produz esses dois valores.

## 7. Casos de erro e códigos de saída

| Código | Situação |
|--------|----------|
| `0`    | operação concluída e arquivo gravado |
| `1`    | erro previsto (arquivo inexistente, formato não suportado, parâmetro inválido) |
| `2`    | erro de linha de comando (argumento ausente ou operação desconhecida) |

```bash
# codigo 1 - arquivo inexistente
python -m pdi_lab --input images/input/nao_existe.jpg --output images/output/x.png --operation negative

# codigo 1 - brightness sem --value
python -m pdi_lab --input images/input/cabana.jpg --output images/output/x.png --operation brightness

# codigo 1 - limiar fora de 0-255
python -m pdi_lab --input images/input/cabana.jpg --output images/output/x.png --operation threshold --threshold 300

# codigo 1 - alfa negativo
python -m pdi_lab --input images/input/cabana.jpg --output images/output/x.png --operation contrast --alpha -1

# codigo 2 - operacao inexistente (rejeitada pelo argparse)
python -m pdi_lab --input images/input/cabana.jpg --output images/output/x.png --operation blur

# codigo 2 - argumento obrigatorio ausente
python -m pdi_lab --input images/input/cabana.jpg --operation negative
```

Para inspecionar o código de saída após a execução:

```bash
echo $?              # Git Bash
echo %errorlevel%    # cmd
```

## 8. Verificação manual com a imagem sintética

`images/input/sintetica.png` é uma imagem `8 x 8` em modo `L` cujas linhas
repetem os valores `0, 32, 64, 96, 128, 160, 192, 255`. Por ser pequena, os
resultados podem ser conferidos pixel a pixel.

```bash
python -m pdi_lab --input images/input/sintetica.png --output images/output/sintetica_brilho_mais10.png --operation brightness --value 10
python -m pdi_lab --input images/input/sintetica.png --output images/output/sintetica_contraste_2_0.png --operation contrast --alpha 2.0
```

Valores esperados sobre uma linha da imagem sintética:

| Operação | Entrada | Saída esperada |
|---|---|---|
| `brightness --value 10` | `0, 32, 64, 96, 128, 160, 192, 255` | `10, 42, 74, 106, 138, 170, 202, 255` |
| `negative` | `0, 32, 64, 96, 128, 160, 192, 255` | `255, 223, 191, 159, 127, 95, 63, 0` |
| `threshold --threshold 128` | `0, 32, 64, 96, 128, 160, 192, 255` | `0, 0, 0, 0, 255, 255, 255, 255` |

Note a saturação em `brightness --value 10`: o pixel `255` permanece `255` em vez
de virar `265`, por causa de `_limitar` em `src/pdi_lab/operacoes.py`.

## Observações de desempenho

As transformações percorrem os pixels em Python puro, sem NumPy, conforme a
exigência do laboratório. Numa imagem de `6000 x 4000` (24 milhões de pixels)
cada operação leva cerca de 6 a 7 segundos. A imagem sintética é instantânea.

## Testes automatizados

Este arquivo cobre a verificação manual pela linha de comando. Os testes
automatizados das operações estão em `tests/test_operacoes.py` e são executados
com:

```bash
python -m pytest
```
