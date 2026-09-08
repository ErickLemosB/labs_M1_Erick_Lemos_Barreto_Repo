# Laboratório M1.2 — Transformações de intensidade

**Disciplina:** Processamento de Imagens — 2026-02
**Laboratório:** M1.2
**Estudante:** Erick Lemos Barreto
**Linguagem:** Python

Aplicação que implementa manualmente ajuste de brilho,
ajuste de contraste, negativo, limiarização binária e histograma através de linha de comando.

## Dependências

Python 3.10 ou superior
Pillow (apenas para abrir e salvar arquivos de imagem)
pytest (testes)

As versões estão em `requirements.txt`.

## Preparação do ambiente

```bash
python -m venv .venv
source .venv/Scripts/activate      # MSYS2 UCRT64 / Git Bash
# .venv\Scripts\activate           # PowerShell
# source .venv/bin/activate        # Linux / macOS
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` instala o projeto em modo editável (`-e .`), o que
torna o pacote `pdi_lab` importável. Depois disso:

```bash
python -m pdi_lab --help
```

## Testes

```bash
python -m pytest
```

## Execução

Forma geral:

```bash
python -m pdi_lab --input <arquivo> --output <arquivo> --operation <operacao> [opcoes]
```
Operacao = brightness -> parâmetro obrigatório = --value <int> -> saída = imagem
Operacao = contrast -> parâmetro obrigatório = --alpha float -> saída = imagem
Operacao = negative -> saída = imagem
Operacao = threshold -> parâmetro obrigatório = --threshold <0-255> -> saída = imagem
Operacao = histogram -> saída = CSV

Todos os caminhos são relativos à raiz do projeto.

### Exemplos (gerados por IA como descrito no AI usage e também como em tests/exemplos_cli.md)

```bash
# brilho (b > 0 e b < 0)
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_brilho_mais60.png  --operation brightness --value 60
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_brilho_menos60.png --operation brightness --value -60

# contraste (reduzido, identidade e ampliado)
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_contraste_0_5.png --operation contrast --alpha 0.5
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_contraste_1_0.png --operation contrast --alpha 1.0
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_contraste_1_5.png --operation contrast --alpha 1.5

# negativo
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_negativo.png --operation negative

# limiarização (dois limiares)
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_limiar_100.png --operation threshold --threshold 100
python -m pdi_lab --input images/input/cabana.jpg --output images/output/cabana_limiar_160.png --operation threshold --threshold 160

# histograma da imagem original e de imagens transformadas
python -m pdi_lab --input images/input/cabana.jpg                --output results/hist_cabana_original.csv     --operation histogram
python -m pdi_lab --input images/output/cabana_brilho_mais60.png --output results/hist_cabana_brilho_mais60.csv --operation histogram
python -m pdi_lab --input images/output/cabana_contraste_1_5.png --output results/hist_cabana_contraste_1_5.csv --operation histogram
python -m pdi_lab --input images/output/cabana_limiar_100.png    --output results/hist_cabana_limiar_100.csv    --operation histogram
```


## Códigos de saída

0 = deu certo e arquivo foi gravado
1 = erro tratado (previsto) algo como arquivo n existe, não suportado ou algum parâmetro inválido
2 = erro de linha de comando, erro em um pedido por linha de comando como: python -m pdi_lab --input images/output/cabana_limiar_100.png    --output results/hist_cabana_limiar_100.csv    --operation histograme <-