# Mini relatório técnico — Laboratório M1.2

## 1. Identificação

**Estudante:** Erick Lemos Barreto
**Disciplina:** Processamento de Imagens — 2026-02
**Laboratório:** M1.2 — Transformações de intensidade
**Linguagem:** Python 3.12

## 2. Objetivo

Implementar manualmente transformações pontuais sobre imagens em níveis de
cinza e analisar como elas alteram os valores dos pixels e a distribuição das
intensidades.

## 3. Operações implementadas


Brilho = `g = f + b` dentro de `src/pdi_lab/operacoes.py`
Contraste = `g = α (f − 128) + 128` dentro de `src/pdi_lab/operacoes.py`
Negativo = `g = 255 − f` dentro de `src/pdi_lab/operacoes.py`
Limiarização = `g = 0` se `f < T`, senão `255` dentro de `src/pdi_lab/operacoes.py`
Histograma = contagem de 256 intensidades dentro de `src/pdi_lab/operacoes.py`

Todas percorrem a imagem linha a linha e coluna por coluna, nenhuma funcao ou biblioteca protas foram usadas.

## 4. Decisões de implementação

A imagem é considerado um dado 2D, mas está sendo guardada em um bytearray linear (`imagem cinza`)

Sobre a saturacao, ela é feita na funcao `_limitar` que se aplica DEPOIS do cálculo, pra n perder informacao no meio do caminho

No contraste, o cáculo é feito sim em ponto flutuante mas é arredondado com `math.floor(valor + 0.5)` (inteiro mais prxm, meio para cima) antes da saturacao (`_limitar`)

Caso as fotos estejam em RGB ou RGBA, tem uma funcao que converte para niveis de cinza, que é feita na leitura manualmente com 0,299 vermelho (R) + 0,587 verde (G) + 0,114 azul (blue). Usando do Pillow para abrir e salvar os arquvios.

O histograma é gravado como `intensity,count` com 256 linhas de dados,

Erros previstos são sinalizados por `ErroPdi` e resultam em código de saída
`1`; erros de linha de comando resultam em `2`.

## 5. Testes realizados

Suíte automatizada em `tests/test_operacoes.py` — **13 testes, todos aprovados**
(`python -m pytest`). Baseiam-se em uma imagem `4 × 2` com os valores
`[0, 10, 128, 250, 255, 200, 64, 5]`, cujos resultados foram conferidos à mão:

brilho positivo (`b = +30`) e negativo (`b = −30`), incluindo saturação nos
dois extremos;
contraste reduzido (`α = 0,5`), identidade (`α = 1,0`) e ampliado (`α = 1,5`);
negativo;
limiarização com `T = 128` e `T = 64`;
histograma da imagem original e de uma imagem limiarizada;
guardas: arquivo inexistente, parâmetro obrigatório ausente e códigos de saída.

Guardas verificadas na execução, todas com código de saída diferente de zero:


comando = arquivo inexistente -> cod erro = 1 -> mensagem = arquivo de entrada não encontrado
comando = arquivo que não é imagem -> cod erro = 1 -> mensagem = falha ao abrir a imagem

e etc...

## 6. Resultados

Medidas obtidas dos CSVs em `results/` (imagem `cabana.jpg`, 24.000.000 pixels):

| Imagem | Média | Pixels em 0 | Pixels em 255 | Níveis ocupados |
|---|---:|---:|---:|---:|
| original | 110,01 | 43.166 | 7 | 256 |
| brilho `b = +60` | 169,81 | 0 | 526.531 | 196 |
| contraste `α = 1,5` | 104,62 | 3.113.187 | 92.154 | 172 |
| limiar `T = 100` | 168,41 | 8.149.944 | 15.850.056 | 2 |

Saídas geradas em `images/output/` (8 imagens) e `results/` (5 histogramas).

## 7. Análise técnica (tirada dos testes gerados pelo CLAUDE e dos .CSV)


Valores tirados dos CSVs em `results/` (`cabana.jpg`, 24.000.000 de pixels).

1. **Diferença entre brilho e contraste:** o brilho demonstra uma somatória (g = f + b) e preserva a distância entre os pixels, enquanto o contraste é multiplicativo (g = α (f - 128)  + 128) e também multiploca essa distância por α
Nos dados: o brilho mudou a média de `110,01` para `169,81` mantendo o desvio-padrão
(`50,47 → 50,07`), enquanto o contraste quase não mexeu na média e subiu o
desvio para `69,74`. Brilho translada a distribuição, contraste a espalha.
No contexto visual, parece que o contraste "estoura" os pixels em branco enquanto o brilho aumenta o brilho dos pretos e brancos sem "estourar".

2. **Onde ocorreu saturação e qual foi o efeito:** no brilho `b = +60`, os
pixels com `f ≥ 195` foram grampeados em `255` — 526.531 pixels (2,19 %). No
contraste `α = 1,5`, `f ≤ 42` virou `0` (3.113.187 pixels, 12,97 %) e `f ≥ 213`
virou `255` (92.154 pixels, 0,38 %). O efeito é perda irreversível de detalhe
nos extremos, mais severa nas sombras porque a `cabana.jpg` já era escura
(média 110, abaixo do ponto neutro 128).

3. **Deslocamento do histograma após alterar o brilho:** o histograma desliza 60
posições para a direita preservando a forma — verifiquei que
`hist_brilho[k + 60] == hist_original[k]` para todo `k < 195`. Os níveis `0` a
`59` ficam vazios e forma-se um pico em `255` com os pixels saturados, o que
reduz os níveis ocupados de 256 para 196. Não há buracos internos.

4. **Mudança da distribuição após alterar o contraste:** a distribuição é
esticada em torno de 128, único ponto fixo. Os níveis ocupados caem para 172,
por dois motivos: os picos de grampeamento nas pontas e 84 buracos internos nos
múltiplos de 3 — o efeito pente, causado por `α = 1,5 = 3/2` espalhar 2 níveis
de entrada sobre 3 de saída. Ampliar o contraste não cria informação: a entropia
cai de `7,452` para `6,743` bits/pixel.

5. **Informação perdida após a limiarização:** é a operação mais destrutiva —
256 níveis viram 2 e a entropia cai de `7,452` para `0,924` bits/pixel, cerca de
87,6 % da informação descartada. Com `T = 100`, 33,96 % dos pixels ficaram
pretos e 66,04 % brancos. Perde-se todo o gradiente (textura, sombreamento) e
resta apenas a forma, que é o que interessa para segmentação. A perda é
irreversível: um pixel `255` na saída pode ter vindo de qualquer valor entre 100
e 255. Comparando as quatro operações, só o negativo é totalmente reversível
(`255 − (255 − f) = f`); brilho e contraste são reversíveis apenas fora da
saturação; a limiarização não é.

## 8. Limitações

O percurso pixel a pixel em Python é lento: cerca de 10 segundos por operação
em uma imagem de 24 milhões de pixels.
Apenas imagens de 8 bits são tratadas;
A conversão para nível de cinza usa coeficientes fixos, sem correção de gama.
O contraste usa o ponto neutro fixo em 128, como pede o enunciado, e não a
média da imagem.

## 9. Declaração de uso de IA

Ver `AI_USAGE.md`.

## 10. Referências

Enunciado do Laboratório M1.2 — Processamento de Imagens, 2026-02.
Contrato técnico dos Laboratórios da M1 — versão para estudantes.
Rubrica geral dos Laboratórios da M1.
Documentação da Pillow — abertura e gravação de imagens.
https://stackoverflow.com/search?q=Pillow+python
https://stackoverflow.com/search?q=Image+processing+Python&s=319600de-8383-4d08-bc10-73830a5dbe1f