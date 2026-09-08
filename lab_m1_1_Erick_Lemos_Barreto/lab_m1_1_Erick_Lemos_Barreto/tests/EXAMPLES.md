# Exemplos de uso — pdi_lab.main

Todos os comandos abaixo foram executados de verdade a partir da raiz do
projeto, com `PYTHONPATH=src` (ou `set PYTHONPATH=src` no `cmd.exe`).

Convenção usada no projeto:
- **Entrada**: sempre a partir de `images/input/` (aqui, `images/input/test.png`)
- **Saída**: sempre para `images/output/`

```cmd
set PYTHONPATH=src
python -m pdi_lab.main --input images\input\<arquivo> --output images\output\<arquivo> --operation <operacao>
```

> Lembrete: `inspect` gera **texto** (`--output images\output\arquivo.txt`);
> todas as outras operações geram **imagem**
> (`--output images\output\arquivo.png`, `.jpg`, etc.).

---

## inspect

Mostra dimensões, tipo e estatísticas da imagem. Funciona com imagem colorida
ou em escala de cinza.

### Imagem colorida (3 canais)

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\inspect_color.txt --operation inspect
```

Saída (impressa no terminal e salva em `images\output\inspect_color.txt`):

```
width=160
height=120
channels=3
type=uint8
pixels=19200
min_b=0
max_b=255
mean_b=86.5000
min_g=0
max_g=255
mean_g=80.1250
min_r=0
max_r=255
mean_r=80.1250
```

### Imagem em escala de cinza (1 canal)

Usando o `images\output\gray_weighted.png` gerado no exemplo de
`grayscale_weighted` abaixo:

```cmd
python -m pdi_lab.main --input images\output\gray_weighted.png --output images\output\inspect_gray.txt --operation inspect
```

Saída:

```
width=160
height=120
channels=1
type=uint8
pixels=19200
min=29
max=255
mean=80.8500
```

---

## channel_b / channel_g / channel_r

Extrai um único canal de cor (B, G ou R), zerando os demais. Exige imagem
colorida com 3 canais.

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\channel_b.png --operation channel_b
python -m pdi_lab.main --input images\input\test.png --output images\output\channel_g.png --operation channel_g
python -m pdi_lab.main --input images\input\test.png --output images\output\channel_r.png --operation channel_r
```

Saída (idêntica para os três, trocando o nome do canal):

```
ok: channel_b -> images\output\channel_b.png
ok: channel_g -> images\output\channel_g.png
ok: channel_r -> images\output\channel_r.png
```

---

## copy

Copia a imagem pixel a pixel (mesmo conteúdo, sem alterações).

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\copy.png --operation copy
```

Saída:

```
ok: copy -> images\output\copy.png
```

---

## grayscale_average

Converte para escala de cinza pela média simples `(R + G + B) / 3`. Exige
imagem colorida com 3 canais.

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\gray_avg.png --operation grayscale_average
```

Saída:

```
ok: grayscale_average -> images\output\gray_avg.png
```

---

## grayscale_weighted

Converte para escala de cinza pela média ponderada (luminância):
`0.299*R + 0.587*G + 0.114*B`. Exige imagem colorida com 3 canais.

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\gray_weighted.png --operation grayscale_weighted
```

Saída:

```
ok: grayscale_weighted -> images\output\gray_weighted.png
```

---

## quantize

Reduz a imagem em escala de cinza para um número menor de níveis de
intensidade. Exige imagem com 1 canal (gere uma com `grayscale_average` ou
`grayscale_weighted` antes) e `--levels` entre 2 e 256.

```cmd
python -m pdi_lab.main --input images\output\gray_weighted.png --output images\output\quantize_4.png --operation quantize --levels 4
python -m pdi_lab.main --input images\output\gray_weighted.png --output images\output\quantize_2.png --operation quantize --levels 2
```

Saída:

```
ok: quantize -> images\output\quantize_4.png
ok: quantize -> images\output\quantize_2.png
```

---

## Erros esperados (LabError)

O programa trata erros de uso e imprime `erro: <mensagem>` em `stderr`,
retornando código de saída `1`.

### quantize em imagem colorida

```cmd
python -m pdi_lab.main --input images\input\test.png --output images\output\erro1.png --operation quantize --levels 4
```

```
erro: a quantizacao exige uma imagem em niveis de cinza (1 canal)
```

### channel_b em imagem já em escala de cinza

```cmd
python -m pdi_lab.main --input images\output\gray_weighted.png --output images\output\erro2.png --operation channel_b
```

```
erro: esta operacao exige uma imagem colorida com 3 canais
```

### --levels fora do intervalo permitido (2 a 256)

```cmd
python -m pdi_lab.main --input images\output\gray_weighted.png --output images\output\erro3.png --operation quantize --levels 300
```

```
erro: --levels deve estar entre 2 e 256, recebi 300
```

### arquivo de entrada inexistente

```cmd
python -m pdi_lab.main --input images\input\nao_existe.png --output images\output\erro4.png --operation copy
```

```
erro: arquivo de entrada nao encontrado: images\input\nao_existe.png
```
