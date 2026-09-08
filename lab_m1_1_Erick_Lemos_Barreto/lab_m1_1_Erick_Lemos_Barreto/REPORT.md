# Mini relatório técnico — Laboratório M1.1

## 1. Identificação

Estudante: Erick Lemos Barreto
Laboratório: M1.1 — Representação, canais e níveis de cinza
Linguagem: Python (OpenCV)

## 2. Objetivo

Compreender e implementar operações fundamentais de processamento digital de imagens: manipulação de canais de cor (RGB/BGR), conversão para escala de cinza através de diferentes métodos e quantização de níveis radiométricos, desenvolvendo algoritmos pixel-a-pixel sem utilizar funções prontas do OpenCV.

## 3. Operações implementadas

Operação = `inspect` -> O que faz = largura, altura, canais, tipo, min/max/média (por canal se colorida) -> Arquivo = `src/pdi_lab/main.py`
Operação = `copy` -> O que faz = cópia manual pixel a pixel -> Arquivo = `src/pdi_lab/main.py`
Operação = `channel_b` -> O que faz = isola o canal azul, zera os demais -> Arquivo = `src/pdi_lab/main.py`
Operação = `channel_g` -> O que faz = isola o canal verde, zera os demais -> Arquivo = `src/pdi_lab/main.py`
Operação = `channel_r` -> O que faz = isola o canal vermelho, zera os demais -> Arquivo = `src/pdi_lab/main.py`
Operação = `grayscale_average` -> O que faz = `g = (R+G+B)/3` -> Arquivo = `src/pdi_lab/main.py`
Operação = `grayscale_weighted` -> O que faz = `g = 0,299R + 0,587G + 0,114B` -> Arquivo = `src/pdi_lab/main.py`
Operação = `quantize` -> O que faz = reduz para N níveis igualmente espaçados -> Arquivo = `src/pdi_lab/main.py`

## 4. Decisões de implementação

**Percurso explícito dos pixels**: Todas as operações avaliadas (cópia, separação de canais, conversões para cinza e quantização) utilizam duplos laços `for y in range(height)` e `for x in range(width)` para varrer cada pixel individualmente, sem delegar a funções prontas do OpenCV — apenas usamos cv2 para abrir e salvar as imagens.

**Ordem dos canais (BGR)**: OpenCV carrega imagens coloridas em ordem BGR (índices 0, 1, 2), ao contrário da convenção RGB. Isso é mapeado diretamente: `channel_b` extrai o índice 0 (azul), `channel_g` o índice 1 (verde) e `channel_r` o índice 2 (vermelho). As fórmulas de cinza respeitam a ordem RGB lógica: `g = 0,299 R + 0,587 G + 0,114 B` onde R, G, B são os índices 2, 1, 0 fisicamente.

**Arredondamento e saturação**: A média simples usa `round()` para arredondar `(R+G+B)/3`. A média ponderada calcula `0,299 R + 0,587 G + 0,114 B` (que pode exceder 255 para pixels saturados) e aplica `min(255, max(0, round(valor)))` para garantir que o resultado permaneça no intervalo `[0, 255]` — a saturação é necessária porque a soma ponderada pode ultrapassar 255.

**Quantização**: O passo entre níveis é `passo = 256 // levels`. Cada pixel é mapeado para o início da sua faixa através de `(pixel // passo) * passo`, garantindo distribuição uniforme. Com `levels ∈ {2, 4, 8, 16}`, o passo é sempre exato, facilitando conferência manual.

## 5. Testes realizados

Teste = Inspeção -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/inspect.txt --operation inspect` -> Saída = `images/output/inspect.txt`
Teste = Cópia -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/copy.png --operation copy` -> Saída = `images/output/copy.png`
Teste = Canal azul -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/channel_b.png --operation channel_b` -> Saída = `images/output/channel_b.png`
Teste = Canal verde -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/channel_g.png --operation channel_g` -> Saída = `images/output/channel_g.png`
Teste = Canal vermelho -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/channel_r.png --operation channel_r` -> Saída = `images/output/channel_r.png`
Teste = Cinza (média) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/gray_average.png --operation grayscale_average` -> Saída = `images/output/gray_average.png`
Teste = Cinza (ponderada) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/input/test.png --output images/output/gray_weighted.png --operation grayscale_weighted` -> Saída = `images/output/gray_weighted.png`
Teste = Quantização (16 níveis) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_16.png --operation quantize --levels 16` -> Saída = `images/output/quant_16.png`
Teste = Quantização (8 níveis) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_8.png --operation quantize --levels 8` -> Saída = `images/output/quant_8.png`
Teste = Quantização (4 níveis) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_4.png --operation quantize --levels 4` -> Saída = `images/output/quant_4.png`
Teste = Quantização (2 níveis) -> Comando = `PYTHONPATH=src python -m pdi_lab --input images/output/gray_weighted.png --output images/output/quant_2.png --operation quantize --levels 2` -> Saída = `images/output/quant_2.png`
Teste = Suite automatizada -> Comando = `PYTHONPATH=src python -m pytest -v` -> Saída = resultado dos testes (stdout)

## 6. Resultados

**Inspeção** (`images/output/inspect.txt`): Arquivo texto contendo largura, altura, número de canais, tipo de dados (uint8), total de pixels e estatísticas por canal (mín, máx, média).

**Cópia** (`images/output/copy.png`): Imagem idêntica à entrada, verificando que o percurso pixel-a-pixel não introduce artefatos ou perda de informação.

**Canais isolados** (`images/output/channel_b.png`, `channel_g.png`, `channel_r.png`): Três imagens coloridas onde apenas um canal é preservado e os demais são zerados. Visualiza a contribuição individual de cada componente de cor.

**Cinza (média simples)** (`images/output/gray_average.png`): Imagem em escala de cinza usando `(R+G+B)/3`. Produz resultado mais claro que a ponderada, pois todos os canais contribuem igualmente.

**Cinza (média ponderada)** (`images/output/gray_weighted.png`): Imagem em escala de cinza usando `0,299 R + 0,587 G + 0,114 B`. Mais escura que a média simples devido ao peso maior do canal verde (0,587), que aproxima melhor a percepção visual humana.

**Quantização (16, 8, 4, 2 níveis)** (`images/output/quant_16.png`, `quant_8.png`, `quant_4.png`, `quant_2.png`): Progressiva redução de níveis radiométricos. Com 16 níveis há pouca degradação visual; com 2 níveis obtém-se apenas preto e branco, mostrando perda significativa de informação.

## 7. Análise técnica

1. **Resolução espacial vs. resolução radiométrica**: Resolução espacial refere-se ao número de pixels na imagem (dimensões H×W), determinando o nível de detalhe geométrico. Resolução radiométrica refere-se à quantidade de níveis de intensidade por pixel (bits por canal), determinando a fidelidade das variações de brilho/cor. Uma imagem pode ter alta resolução espacial mas baixa radiométrica (muitos pixels, poucos níveis).

2. **Diferença entre média ponderada e simples**: A média simples `(R+G+B)/3` trata todos os canais igualmente, produzindo um resultado mais claro. A média ponderada `0,299 R + 0,587 G + 0,114 B` enfatiza o canal verde (57%), que é mais sensível ao olho humano, resultando em cinza mais escuro. Os pesos da ponderada aproximam melhor a luminância percebida pelo sistema visual humano.

3. **Redução de níveis radiométricos**: Quantização reduz progressivamente os níveis disponíveis. Com 16 níveis a degradação é sutilmente visível. Com 2 níveis (preto e branco), ocorre posterização acentuada, com perda drástica de gradações intermediárias, transformando a imagem em regiões sólidas de cor.

4. **Regiões com maior perda**: Gradientes suaves (transições contínuas de brilho) sofrem mais com quantização, pois múltiplos valores contínuos são mapeados para o mesmo nível discreto. Regiões de cor sólida (flat) perdem pouca informação. A perda é especialmente evidente em céus, sombras suaves e degradês.

5. **Tipo e número de canais na indexação**: Imagens coloridas (3 canais) têm shape `(H, W, 3)`, exigindo índice triplo `img[y, x, c]`. Imagens em cinza (1 canal) têm shape `(H, W)`, exigindo apenas dois índices `img[y, x]`. O acesso a um pixel depende dimensionalmente da representação: faltar ou exceder o índice de canal provoca erro.

## 8. Limitações

**Tipo de dados**: Apenas imagens uint8 (8 bits por canal) são suportadas. Imagens com 16 bits (uint16), ponto flutuante (float32/float64) ou outros tipos não são processadas.

**Número de canais**: Apenas imagens com 1 canal (escala de cinza) ou 3 canais (coloridas BGR) são válidas. Imagens RGBA (4 canais), YUV ou outras representações multi-canal não são tratadas.

**Operações específicas**: `channel_b/g/r` e `grayscale_*` exigem imagens coloridas (3 canais); `quantize` exige imagens em escala de cinza (1 canal). Não há conversão automática entre formatos.

**Performance**: O percurso pixel-a-pixel com laços Python é significativamente mais lento que operações vetorizadas do NumPy ou funções otimizadas do OpenCV, tornando o método impraticável para imagens muito grandes ou processamento em tempo real.

**Formatos de arquivo**: Apenas formatos que o OpenCV consegue abrir (`cv2.imread`) são suportados. Metadados (EXIF, gamma, espaço de cor) são ignorados.

## 9. Declaração de uso de IA

Ver `AI_USAGE.md`.

## 10. Referências

*Bibliografia, documentação e material da disciplina consultados.*
