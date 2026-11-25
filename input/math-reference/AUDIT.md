# Auditoria e ampliação do ground truth matemático — caso 036

Auditoria realizada em **25/11/2026**, seguindo a metodologia do [dataset PR #12](https://github.com/A11yDevs/acessilia-dataset/pull/12): PDF como fonte primária, inspeção visual de todas as páginas, preservação dos erros impressos, IDs estáveis, distinção entre conteúdo literal e semântico e documentação das limitações do avaliador.

## Fonte, base e permissão

- Fonte: [velocidade-instantanea.pdf](velocidade-instantanea.pdf), *Cálculo 1 — O problema da velocidade instantânea*, Universidade de Brasília, Departamento de Matemática, cinco páginas.
- SHA-256 do PDF: `ab72d5c0b524c4b1d2d34e4ccbf0342b217e41394e3eb9bee7188076729c7787`.
- [PERMISSIONS.md](PERMISSIONS.md) preservado byte a byte; SHA-256 `e09ba4546b1bebc0264ff4c12dbed239393ad167067ee6dcd0051cd3f4cf13f7`.
- Commit-base: `8e51a1f599056a6eb30dcbb05491f622a4d25eb1`, `A11yDevs/acessilia-dataset:main`, já incluindo o PR #12. Branch de trabalho: `fix/case-036-math-ground-truth-audit`, no fork `marceloakira/acessilia-dataset`.

O PDF e sua permissão não foram alterados nem incluídos como novas cópias na submissão. A autorização existente é restrita ao uso como documento de teste neste repositório; não foi presumida autorização para distribuição externa. As renderizações de trabalho permaneceram em diretório temporário local e não são artefatos publicados no PR.

## Método e convenções

As cinco páginas foram renderizadas com PyMuPDF em matriz 2 (144 dpi, 1224 × 1584 px) e inspecionadas individualmente. A camada textual e suas posições foram usadas como apoio para transcrição e localização. As fórmulas foram confrontadas visualmente, incluindo índices, potências, frações, limites, agrupamentos, sinais, reticências e o rótulo (1). Nenhuma saída atual do Acessilia foi usada como verdade ou para flexibilizar o dataset.

As regiões em `semantic_reference.json` usam pontos de PDF, origem no canto superior esquerdo, página de 612 × 792 pontos. São faixas de linha ou células aproximadas, não caixas exatas de glifos nem coordenadas exigidas para uma saída transformada. Cada ID tem página, contexto, região e posição entre repetições da mesma expressão. Não se pode satisfazer cinco ocorrências originais com uma única ocorrência na saída.

Convenções adotadas:

1. Cada expressão inline impressa, inclusive variável isolada em notação matemática, constitui uma ocorrência. Subexpressões de uma fórmula maior não geram anotações inline sobrepostas. As palavras portuguesas “a” e “e” não são variáveis automaticamente.
2. Anotam-se os números de todas as fórmulas e células e as quantidades físicas completas com unidade: **60 km/h**, **2 horas** e **1 hora**. Numerais de prosa, graus de polinômio em texto corrido, rótulos de lista/equação, número da disciplina e rodapés são conteúdo textual/estrutural, não novos IDs inline isolados.
3. Repetições em contextos diferentes mantêm IDs distintos. As ocorrências novas de `a` e `h` foram registradas separadamente; não substituem expressões compostas existentes. `inline` identifica o papel na fonte: uma quantidade pode ser preservada como prosa acessível completa com unidade; `as_math` no avaliador legado mede marcação, não todas as representações acessíveis válidas.
4. `expected_latex` conserva a representação do impresso, inclusive `2^8`. Pontuação de frase não é operando; vírgula decimal integra o número. A tag (1) continua no CSV por compatibilidade, mas `math_latex` e `equations` a separam da árvore matemática.
5. São válidas representações matematicamente equivalentes que preservem o conteúdo impresso e suas relações. Isso não autoriza corrigir um erro da fonte, eliminar etapas expostas, preencher exercícios ou mesclar ocorrências distintas.
6. As cinco posições vazias da segunda tabela são intencionais. Não são zeros nem valores “faltantes” a inferir. Permanecem em JSON, pois uma linha vazia no CSV seria aceita trivialmente pela busca lexical do avaliador atual.
7. Hifenização de quebra de linha é diferente de sinal matemático: `introduzire-`/`mos` na página 4 e `ex-`/`pressão` na página 5 são palavras contínuas; sinais de menos, limites e desigualdades são preservados.

## Comparativo quantitativo

**91 → 131 linhas no CSV: 40 adições, 7 modificações de notas e nenhuma exclusão. Todos os 91 IDs anteriores e seus 91 valores `expected_latex` foram preservados.** As adições são 24 células preenchidas e 16 expressões inline. Não houve meta artificial de contagem.

| Página | Inline antes/depois | Display antes/depois | Cabeçalhos antes/depois | Células preenchidas antes/depois | Vazias em JSON |
|---|---:|---:|---:|---:|---:|
| 1 | 18 / 20 | 2 / 2 | 0 / 0 | 0 / 0 | 0 |
| 2 | 18 / 23 | 3 / 3 | 3 / 3 | 0 / 18 | 0 |
| 3 | 18 / 22 | 7 / 7 | 0 / 0 | 0 / 0 | 0 |
| 4 | 11 / 15 | 1 / 1 | 0 / 0 | 0 / 0 | 0 |
| 5 | 3 / 4 | 3 / 3 | 3 / 3 | 1 / 7 | 5 |
| **Total** | **68 / 84** | **16 / 16** | **6 / 6** | **1 / 25** | **5** |

O [AUDIT_DIFF.csv](AUDIT_DIFF.csv) compara cada ID/campo com a base: `id,page,change,field,before,after`. Novos IDs têm os sete campos registrados; alterações de notas não são confundidas com alterações de expressão. O validador reproduz esse diff a partir do commit-base. O JSON semântico é novo; alterações estruturais e de fala do expectations são explicadas abaixo.

## Evidências e decisões por página

### Página 1 — movimento, títulos e problema

Fonte: [página 1](velocidade-instantanea.pdf#page=1). Cabeçalho e logotipo no topo; duas fórmulas no corpo; enunciado azul “Problema:” no terço inferior.

As duas displays foram conferidas: posição com `s_0`, `v_0`, fração `1/2`, produto `at²` e condição `t>0`; velocidade com `v_0+at` e a mesma condição. As 18 ocorrências inline originais foram mantidas. Adicionadas `p1-i19` (**60 km/h**) e `p1-i20` (**a** isolado em “aceleração é igual a a”). O `a` dentro de `a ∈ R` já está em `p1-i07`; não é a mesma ocorrência.

O enunciado completo está em `document_structure.callouts`, associado a `p1-i16`/`p1-i17`: “Problema: se a posição do carro é dada por s(t) = t³, qual é a velocidade do carro no instante t = 2 ?”. O rótulo é destacado; a cor azul não deve ser a única indicação semântica. Preservam-se títulos de níveis 1 e 2 e a ênfase de “movimento uniformemente variado”. O logotipo é identificado como da UnB, sem repetir o cabeçalho institucional. O rodapé “1” permanece fora do fluxo principal.

Particularidades da fonte: “se o carro tendo” e “para aos casos” não são reparações automáticas da gramática. Os artefatos de acentuação do TeX são problema de extração, não novos erros ortográficos do impresso.

### Página 2 — primeira tabela e equação numerada

Fonte: [página 2](velocidade-instantanea.pdf#page=2). Três displays; tabela no centro; equação (1) abaixo; último parágrafo continua na página 3.

As 18 células da primeira tabela estão agora individualmente no CSV (`p2-t04` a `p2-t21`), com linha, coluna, cabeçalho correspondente, chave `h` e região no JSON. São seis linhas de dados, três colunas e uma linha de cabeçalhos; `rows=7` no esquema legado inclui o cabeçalho.

| h ≠ 0 | instante final, t = 2 + h | velocidade média, [s(2+h)−s(2)]/[(2+h)−2] |
|---|---|---|
| 2 | 4 | 28 |
| 1 | 3 | 19 |
| 0,5 | 2,5 | 15,25 |
| 0,1 | 2,1 | 12,61 |
| 0,01 | 2,01 | 12,0601 |
| 0,001 | 2,001 | 12,006001 |

Os três cabeçalhos matemáticos (`p2-t01`/`02`/`03`) foram conferidos, com os rótulos textuais “instante final” e “velocidade média” preservados no JSON. Não basta encontrar esses números em qualquer lugar da tabela.

Adicionadas cinco inlines: `p2-i19` (2 horas), `p2-i20` (1 hora) e `p2-i21`/`22`/`23` (três ocorrências de `h` isolado). Preservadas ênfases em “aproximar esse valor” e “distintos”.

**Erro matemático confirmado:** a segunda fração de `p2-d03` imprime `(2+h)^3−2^8`, dividido por `h`. O CSV já preservava `2^8` e continua preservando. A função `s(t)=t³`, a tabela e o desenvolvimento da página seguinte apontariam para `2^3`, mas essa interpretação é apenas uma nota: não substitui o literal. O rótulo **(1)** é registrado separadamente, com vínculo à fórmula e duas referências textuais na página 3.

A continuidade “Essa última restrição surge porque, se h < −2, então” → “2+h<0, e não faz sentido...” foi registrada. O rodapé “2” não pode ser inserido no meio desse período.

### Página 3 — domínio, cadeias de igualdades e limites

Fonte: [página 3](velocidade-instantanea.pdf#page=3). Continuação no topo; fórmula do domínio; expansão em duas linhas; quatro displays subsequentes de limites/álgebra.

As **sete displays** foram conferidas. `p3-d01` preserva domínio de `vm_2`, extremo −2 fechado, zero excluído, união, infinito positivo, pertinência aos reais, maior ou igual, diferente de zero e conjunção. A árvore distingue `Dom` de um produto de letras e subscrito de potência. A palavra “infinito” sozinha não é critério de fidelidade.

`p3-d02` tem **quatro membros de uma cadeia de igualdades em duas linhas**. Um único bloco ou vários blocos matemáticos associados e ordenados são representações válidas; todos os membros e sinais de igualdade precisam sobreviver. A representação mais simples `12+6h+h²`, sozinha, não preserva as etapas impressas. Nesta página o original imprime **2³**, em contraste com o 2⁸ da equação (1); ambas as transcrições literais são mantidas.

As duas menções a **(1)** são `p3-ref01` e `p3-ref02`, em contextos de `p3-i04` e `p3-i07`. Cada limite especifica a variável **h** e aproximação a **0**, além do operando; não basta pronunciar “limite”. Foram adicionadas quatro ocorrências isoladas de `h`: `p3-i19` a `p3-i22`.

**Ortografia preservada:** “acontence” em `p3-i11` é impresso assim e continua no contexto e nas notas. Não se confunde com ligaturas ou acentos mal extraídos.

### Página 4 — solução e lista ordenada

Fonte: [página 4](velocidade-instantanea.pdf#page=4). Explicação no topo, chamada azul com solução e lista de quatro itens; a única display está dentro do primeiro item.

O enunciado integral de **“Solução do problema:”** está no JSON: posição `s(t)=t³`, velocidade `v(t)=3t²`, condição `t>0` e a afirmação final de velocidade 12 no instante 2. Os três IDs inline da chamada permanecem associados.

A lista tem quatro itens numerados. `p4-d01` pertence ao **item 1**, com continuação “de modo a descobrir...”; sua presença não encerra o item nem reinicia a numeração. O item 2 destaca “mas diferentes”. O item 3 contém hifenização tipográfica de “introduziremos”. O item 4 contém `s(t)=s_0+v_0t+(a/2)t²`, com a fração `a/2` agrupada e multiplicação implícita. O literal `s_0, a ∈ R` não contém `v_0` nessa lista de variáveis e não foi ampliado.

Adicionadas quatro ocorrências isoladas de `h`, `p4-i12` a `p4-i15`, incluindo a introdução e os itens 1, 2 e 4. As notas de `p4-d01`, `p4-i09` e `p4-i10` explicitam vínculo, agrupamento e ausência de variável adicional.

### Página 5 — exercício e células intencionalmente vazias

Fonte: [página 5](velocidade-instantanea.pdf#page=5). Título “Tarefa”, função `s(t)=1/t`, três itens numerados e desenvolvimento final separado.

A segunda tabela tem quatro linhas de dados e três colunas. Seu cabeçalho usa `h≠0`, `t=3+h` e `[s(3+h)−s(3)]/[(3+h)−3]`. O ID existente `p5-t04` continua sendo a velocidade negativa da primeira linha, com qualificador **“(aproximadamente)”**. Seis novos IDs, `p5-t05` a `p5-t10`, completam as sete células preenchidas. As cinco posições vazias são `p5-e01` a `p5-e05`, exclusivamente no JSON.

| h ≠ 0 | instante final, t = 3 + h | velocidade média |
|---|---|---|
| 1 | 4 | −0,0833 (aproximadamente) |
| 0,1 | 3,1 | |
| 0,01 | | |
| 0,001 | | |

Coordenadas das lacunas, em linhas de dados (sem cabeçalho): **(2,3), (3,2), (3,3), (4,2), (4,3)**. No grid completo incluindo cabeçalho: **(3,3), (4,2), (4,3), (5,2), (5,3)**. Não foram calculados ou inseridos resultados para essas posições.

A tabela pertence ao **item 1**; `p5-d02` pertence ao **item 2**. Essa fórmula contém uma fração externa cujo numerador é a subtração de duas frações internas, as reticências de etapas omitidas e o resultado negativo `−1/[(3+h)3]`. O 3 final é fator multiplicativo; não é expoente nem chamada de função. O item 3 pede que h se aproxime de 0 e se determine `v(3)`, mas a auditoria não fornece a solução. `p5-i04` registra esse h isolado.

`p5-d03` preserva os dois limites, sinal negativo, agrupamento `(t+h)t` e reticências. O parágrafo iniciado por “Repetindo o argumento do item 2...” faz referência ao segundo item, depois da lista. Não foi completado com uma derivada final ausente no original. A palavra “expressão” dividida no rodapé é unida como palavra, preservando o sinal matemático de menos discutido na pergunta.

## Conferência das 16 fórmulas display

O LaTeX anterior foi confirmado no PDF; as alterações de CSV nas displays são notas, não substituições das fórmulas. A árvore de cada fórmula registra os operandos e seus agrupamentos, não só tokens estruturais.

| ID | Página / região em pontos (y) | Relações conferidas |
|---|---|---|
| `p1-d01` | 1, y=290–322 | s(t)=s₀+v₀t+(1/2)at²; subscritos, fração, quadrado e t>0. |
| `p1-d02` | 1, y=379–396 | v(t)=v₀+at e t>0; produto a·t, não aplicação de função. |
| `p2-d01` | 2, y=117–150 | Quatro membros: (s(4)−s(2))/(4−2), (4³−2³)/(4−2), (64−8)/2, 28. |
| `p2-d02` | 2, y=263–295 | Três membros: (s(3)−s(2))/(3−2), (27−8)/1, 19. |
| `p2-d03` | 2, y=628–662 | Três membros; 2⁸ preservado; número (1) fora dos operandos. |
| `p3-d01` | 3, y=111–132 | Dom(vm₂), intervalos, união e descrição por conjunto com pertinência, ≥, ≠ e conjunção. |
| `p3-d02` | 3, y=249–314 | Quatro membros em duas linhas; expansão completa, produtos com pontos e fatoração h(12+6h+h²)/h. |
| `p3-d03` | 3, y=332–350 | vm₂(h)=12+6h+h²; subscrito, produto e quadrado. |
| `p3-d04` | 3, y=478–511 | Dois limites h→0; quociente incremental em 2; resultado 12. |
| `p3-d05` | 3, y=586–620 | v(t) e dois limites h→0; denominadores (t+h)−t e h, respectivamente. |
| `p3-d06` | 3, y=650–668 | Três membros: diferença de cubos, expansão agrupada e produto h(3t²+3th+h²). |
| `p3-d07` | 3, y=698–733 | Cinco membros; dois limites h→0, cancelamento representado e etapas 3t²+0+0 e 3t². |
| `p4-d01` | 4, y=275–308 | Uma fração: s(t+h)−s(t) no numerador, h no denominador; item 1. |
| `p5-d01` | 5, y=140–173 | s(t)=1/t, com t>0; numerador 1 e denominador t. |
| `p5-d02` | 5, y=403–451 | Quatro membros com reticências; subtração de duas frações internas sob divisão por h; negativo e produto final; item 2. |
| `p5-d03` | 5, y=518–551 | Quatro membros com reticências; dois limites h→0; numerador final −1 e denominador (t+h)t. |

## Escolha do arquivo semântico e verbalização

Foi criado [semantic_reference.json](semantic_reference.json), versão de esquema **1.0.0**, para manter a semântica extensível separada do formato legado. Ele registra:

- Todas as 131 ocorrências do CSV, com contexto, região e identidade independente.
- As 16 displays com `literal_latex`, `math_latex`, árvore de operadores/operandos, contagens de nós, invariantes por caminho, segmentação e fala em pt-BR.
- As duas tabelas: seis cabeçalhos, 25 células preenchidas, cinco vazias, índices de linha/coluna, chave da linha, vínculo ao cabeçalho e qualificador de aproximação.
- Rótulo e referências da equação (1), listas, associações de fórmulas e tabela aos itens, chamadas completas, títulos, logotipo, ênfases, continuação de página e mobiliário.
- Restrições inline relevantes para unidades, subscritos, pertinência, `(a/2)t²` e a lista literal `s_0,a`.
- 17 controles semânticos negativos e 9 positivos, **especificações para um futuro avaliador**, com alvos e motivos.

A árvore é uma representação editorial da estrutura do literal, inclusive suas inconsistências. Ela **não** é o resultado de um parser simbólico, e os invariantes/contagens verificam coerência do arquivo, não uma prova automática de equivalência entre LaTeX, árvore, fala e MathML. A revisão visual é a base dessa correspondência. `domain` é um operador nomeado; `call` distingue aplicação de função de `multiply`; `divide` guarda numerador/denominador; `interval` guarda abertura/fechamento; `limit` guarda variável, alvo e operando; condições e rótulos têm escopos separados.

Cada display tem relações de fala obrigatórias e **dois exemplos de paráfrases**. Não é exigida uma única frase literal. A aceitação requer preservar todos os conceitos, relações, agrupamentos e escopos, incluindo a ordem das etapas. Os exemplos ilustram leituras e não são uma lista fechada de respostas.

Em particular, `p3-d01` exige domínio, índice 2, inclusão de −2, exclusão de zero, união, infinito positivo, pertinência aos reais, ≥, ≠ e conjunção. `p5-d02` exige as frações aninhadas, subtração interna, divisão externa por h, reticências, sinal negativo e produto no denominador final. Não se pode demonstrar isso com a presença isolada de “infinito” ou “fração”.

O `expectations.json` agora cobre **16/16** displays em `speech.formulas` (antes **8/16**). As oito regras antigas e seus `any_of` foram conservadas; outras oito foram adicionadas. O campo `any_of` permanece um **indicador lexical legado**, explicitamente insuficiente para aprovar a fala. Cada regra aponta para os critérios completos no novo arquivo. O avaliador atual ignora esses vínculos; não foi criada a aparência de suporte semântico inexistente.

## Compatibilidade, limitações do avaliador e do E2E

O CSV mantém as sete colunas e somente os tipos conhecidos: `inline`, `display`, `table-header`, `table-cell`. Células vazias e estrutura complementar ficam no JSON. `structure.tables.math_cells` agora lista todas as células preenchidas. Títulos, listas, números de equação e padrões anteriores foram preservados. O avaliador do Acessilia não foi modificado neste PR.

Código inspecionado em `develop`: [scripts/bench/math_case.py](https://github.com/A11yDevs/acessilia/blob/develop/scripts/bench/math_case.py), blob `03eb224ac0cc2fca84d5efb1565cd7cc4312b1f0`, e [tests/test_math_case_e2e.py](https://github.com/A11yDevs/acessilia/blob/develop/tests/test_math_case_e2e.py), blob `ee897e9769e47589c0372723c1f1cd54c3f60d47`. Referências de contexto: [Acessilia #850](https://github.com/A11yDevs/acessilia/pull/850), [#880](https://github.com/A11yDevs/acessilia/issues/880), [#852](https://github.com/A11yDevs/acessilia/issues/852) e [#411](https://github.com/A11yDevs/acessilia/issues/411).

| Dimensão | Suporte atual efetivamente observado | Pendência |
|---|---|---|
| Inlines | `_score_inline` escolhe maior CDM entre spans da página ou sem página; limiar 80. | Consumir ocorrências distintas com contexto/posição; uma única expressão não deve satisfazer todas as repetições. |
| Display | `_match_display` associa pares por CDM em ordem gulosa, um bloco por ocorrência, sem aceitar grupos ordenados. | Associação por objeto e segmentação válida de cadeias como `p3-d02`; evitar pareamentos globais incorretos. |
| Fórmula “encontrada” | Qualquer CDM positivo permite marcar um par como encontrado. | Limiar semanticamente confiável e verificação de operadores/operandos; presença não equivale a fidelidade. |
| Células | `_score_tables` busca em qualquer célula da página; também aceita inclusão textual como substring. | Vincular cada valor à tabela, linha e coluna; preservar as lacunas intencionais. |
| CDM e estrutura | CDM e recall de tokens estruturais são indicadores parciais. | Verificar frações, agrupamentos, sinais, índices, extremos, condições, limites e relações completas. |
| MathML | Presença é testada com `bool(metadata.mathml)`. | Validar estrutura MathML e equivalência à referência, separadamente da mera existência de string. |
| Fala | `_speech_checks` aceita qualquer palavra de `any_of`. | Avaliar relações em pt-BR e paráfrases com escopo; keywords são apenas sinais parciais. |
| Documento | Há verificações de títulos, lista, forma da tabela, número de equação e rodapé; vários campos declarados não são consumidos. | Verificar chamadas integrais, logotipo, ênfases, continuação, hierarquia e vínculo de cada fórmula/tabela ao item e de cada referência à equação. |
| TXT/PDF/UA e E2E | E2E trava cinco verificações textuais em ambos os formatos, presença de displays/MathML/fala, listas e velocidade negativa; sem floor de equivalência matemática. | Gates semânticos por formato e por objeto; separar conformidade PDF/UA da fidelidade. Consumo do novo JSON e controles precisa de implementação posterior. |

Foram reproduzidas localmente, com o código original do avaliador, quatro limitações concretas:

1. Um único span `$s(t)$` na página 1 satisfaz as **cinco ocorrências** originais de `s(t)` isolado nessa página.
2. Um bloco matemático contendo apenas `t` é marcado como encontrado para `p1-d01`, com **CDM 7,1**; uma string não vazia inválida como MathML também conta como MathML presente.
3. Trocar **28 e 19** entre as duas primeiras linhas da primeira tabela ainda aprova todas as verificações legadas de células.
4. A fala contendo apenas **“infinito”** ainda passa na regra lexical de `p3-d01`.

Essas demonstrações não são saídas aprovadas nem foram usadas para acomodar o dataset. São evidências de pendências. A issue #880 descreve atualmente a evolução semântica do caso 006; este caso 036 fornece uma referência complementar para coordenação desse trabalho, sem alegar que o escopo da issue já foi ampliado. #852 e #411 continuam como pesquisas de reconhecimento/adjudicação e verbalização. Nenhuma alteração foi feita em Core, SDK, Toolbox, Docstruct, `math_case.py` ou E2E.

## Controles semânticos especificados

Os controles negativos no JSON cobrem: `≠` trocado por `=`, `≥` por `>`, extremo fechado por aberto, inversão de fração, expoente errado, subscrito como sobrescrito, `Dom` como produto, multiplicação como chamada, perda do sinal negativo, troca de células, preenchimento indevido de lacuna, eliminação de repetição, correção silenciosa de 2⁸, referência (1) perdida, reinício da lista, perda da variável/alvo de limite e perda de fração interna.

Os positivos cobrem equivalência de macros (`mathrm`/`operatorname` para Dom, `ge`/`geq`, `ne`/`neq`, `frac`/`dfrac`), segmentação associada da cadeia em duas linhas, notação equivalente do produto no denominador, paráfrases completas, preservação de lacunas, rótulo de equação associado em bloco separado e unidade falada equivalente. Valem somente se o restante da expressão e suas associações também for preservado.

**Esses 26 controles são especificações de avaliação de saídas, não testes implementados no avaliador legado.** Diferem dos controles executados sobre o validador de integridade, descritos a seguir.

## Validação executada e reprodução

Da raiz do dataset:

```bash
python3 input/math-reference/validate.py
python3 input/math-reference/validate.py --self-test
git diff --check
```

O validador usa apenas a biblioteca padrão do Python (3.9+) e o Git para ler o commit-base. Um clone raso pode exigir buscar esse commit. São verificados: hashes e bytes originais de PDF/permissão; CSV/JSON sem IDs ou chaves duplicadas; ID/página/tipo; 91 IDs anteriores; cinco páginas; referência de todas as 131 ocorrências; seis cabeçalhos; 25 células preenchidas; cinco posições vazias exatas; linhas/colunas/cabeçalhos; rótulo (1) e suas duas referências; vínculos de listas; cobertura de 16 displays e 16 expectativas de fala; árvores, contagens e invariantes; referências cruzadas e reprodução exata de `AUDIT_DIFF.csv`.

**Resultado: aprovado.** Inventário final: 84 inline, 16 display, 6 cabeçalhos e 25 células, total 131 IDs únicos; 40 adições, 7 modificações de notas, 0 exclusões. PDF e PERMISSIONS.md inalterados.

O modo `--self-test` executou **19 controles negativos em cópias temporárias**, todos rejeitados: ID duplicado, ocorrência anterior removida, página incompatível, PDF alterado, permissão alterada, chave JSON duplicada, posição de célula duplicada, ID de lacuna duplicado, cabeçalho de célula errado, lacuna preenchida, extremo fechado alterado, fração interna removida, correção silenciosa de 2⁸, expectativa de fala ausente, rótulo ligado à fórmula errada, referência (1) removida, fórmula no item errado, tabela no item errado e diff desatualizado. Duas serializações equivalentes — JSON com outra ordenação/escapes e CSV com aspas/CRLF — foram aceitas. Esses controles verificam corrupção da referência, não qualidade de uma saída acessível.

Foi executado o código original de `math_case.py` obtido de `develop`, sem alterações, por importação e chamadas a `load_case`/`score_case`. Um documento canônico **sintético**, com os objetos da referência, foi usado apenas para verificar aceitação do esquema: **16 displays, 84 inline, 31 cabeçalhos/células e 16 proxies de fala** foram processados sem erros; as 16 primeiras paráfrases ilustrativas satisfazem seus proxies legados. A string sintética de presença MathML não é demonstração de MathML válido. Não houve processamento remoto, comparação de saídas reais nem execução do E2E.

## Limitações e próximos passos

A auditoria visual e a modelagem semântica foram feitas por um único auditor; não houve adjudicação independente nem estudo de compreensão por ouvintes. As regiões são aproximadas. A convenção de numerais de prosa é explícita, não uma alegação de transcrição matemática de todo dígito do documento.

O validador comprova integridade e coerência interna; não calcula derivadas para completar o exercício nem demonstra equivalência entre todas as representações. As árvores e leituras devem poder receber revisão editorial futura. O avaliador atual não consome a semântica complementar, por isso sua pontuação não mede integralmente a preservação agora especificada. Scores anteriores e posteriores devem ser recalculados com a mesma revisão antes de comparar cobertura.

A integração posterior deve implementar os controles de saída, reconhecer ocorrências/segmentações equivalentes, verificar associações de tabelas/listas/equações e avaliar fala/MathML por relações; então separar resultados por objeto e formato. Esta submissão entrega a referência de dados e não declara essas capacidades já implementadas.
