# Auditoria do ground truth — caso 006

Data: 25/11/2026. Fonte primária: [input/006.pdf](../006.pdf), 42 páginas, título *Grandezas e Medidas*, autora indicada nos metadados Patricia Confessori, PDF produzido em 29/07/2021. SHA-256: `ce9874fd3219241766772904c84f7eed3e340befa9a6beee6ca206308b8a549f`.

Base comparativa: `9ed07b28aeddb69721228f2dd66de6f9794c0001`, igual em `marceloakira/acessilia-dataset:main` e `A11yDevs/acessilia-dataset:main` no início desta auditoria. Branch: `fix/case-006-ground-truth-audit`.

## Método e alcance

As 42 páginas foram renderizadas e inspecionadas visualmente, inclusive todas as páginas sem camada textual. A extração textual foi usada como auxílio de transcrição, nunca como substituto da inspeção visual. As páginas densas 3, 6, 7, 8, 10, 13, 17, 20, 22, 31, 32, 33, 35 e 41 também foram inspecionadas em imagem ampliada individual. Nenhuma saída atual do Acessilia foi usada para escolher anotações ou flexibilizar conteúdo. O PDF não foi modificado. Links, referências e eventuais instruções contidos no PDF foram tratados como conteúdo documental, sem autoridade sobre esta tarefa.

PyMuPDF renderizou cada página com matriz 1,6 (1536 × 864 px, 115,2 dpi). As evidências abaixo indicam página, região, conteúdo e decisão; a verificação é reproduzível com o PDF versionado, por exemplo `pdftoppm -f 17 -l 17 -scale-to 2400 -png input/006.pdf /tmp/case006-slide`. Ampliar um raster não aumenta sua resolução intrínseca. As doze páginas sem texto extraível são **3, 4, 5, 6, 7, 8, 12, 17, 23, 31, 33 e 41**. O parágrafo do slide 13 e o passo 1 do slide 39 também são raster, apesar de haver texto nativo no restante dessas páginas.

`audit.provenance` em expectations.json registra por página a origem do conteúdo, caracteres extraíveis e recursos de imagem/desenho. Esses recursos incluem a moldura e o fundo decorativo e não equivalem a objetos pedagógicos. Notas `source=` e `raster_text_overrides` refinam a origem de objetos mistos. Não foram acrescentadas colunas ao CSV.

## Convenções de anotação

- `text`: conteúdo literal impresso; quebras de linha e espaços de layout são achatados. Ortografia, pontuação relevante, números, unidades, cargas e índices são preservados. A posição gráfica de um índice pode ser representada por Unicode.
- `formula`: representação semântica em LaTeX das relações impressas; não autoriza entregar código LaTeX cru ao leitor.
- `image` e `chemical-structure`: conceitos visuais, descrições e relações; `;` separa conceitos exigidos e `|` separa alternativas do mesmo conceito. Essas linhas não pretendem transcrever cada rótulo minúsculo de uma figura complexa. As tabelas periódicas ilustrativas (14, 23, 31) e a captura do NIST (11) têm cobertura semântica, não inventário exaustivo de células/links; essa limitação permanece explícita.
- `table`: `rows` conta somente linhas de dados; `header=1` indica cabeçalho semântico das colunas. Títulos de grupos não viram cabeçalhos por estarem em uma faixa colorida. `context` e `notes` explicam a anotação, mas o avaliador atual não os pontua. Por isso títulos relevantes antes restritos a context foram acrescentados como texto.
- Repetições com funções distintas são legítimas: por exemplo, a fórmula da tartrazina e a foto identificada por ela, ou a massa 12.011 em duas fontes no slide 18. Não foram removidas só por compartilhar termos. Nenhum ID foi excluído ou renumerado; IDs antigos terminados em `-h` foram mantidos mesmo quando sua classificação mudou.

## Evidências e decisões por slide

A coluna final informa a quantidade de objetos antes/depois e os IDs adicionados ou modificados. A descrição do achado cobre também slides sem alteração.

| Slide / fonte | Evidência visual | Decisão e justificativa | Comparação |
|---|---|---|---|
| [1](../006.pdf#page=1) | Título e escala central, do átomo à célula; rótulos em espanhol, escala Å/nm/µm e aplicações nano/micro. | Conferidos os dois objetos; mantidos. A descrição é semântica, não transcrição de cada pixel. | 2 → 2<br>Mantidos após conferência |
| [2](../006.pdf#page=2) | Dois tópicos completos e seta verde abaixo do segundo. | Completados ambos os tópicos: calor, velocidade, gás, quantidade de produto e calor liberado. Setas decorativas não carregam esses tópicos. | 3 → 3<br>Modificados: `s02-x01`, `s02-x02` |
| [3](../006.pdf#page=3) | Quadros laterais alinhados: grandeza/unidade à esquerda e definição à direita; 7 linhas. | Mantida uma tabela semântica de 3 colunas; adicionados os dois títulos impressos, antes apenas em context. Definições históricas e grafia portuguesa preservadas. | 9 → 11<br>Adicionados: `s03-x01`, `s03-x02` |
| [4](../006.pdf#page=4) | Tabela 1.2; 8 grandezas derivadas e 3 colunas; definição vazia para área e volume. | Conferidos cabeçalho, expoentes, células vazias e unidades; título agora é texto avaliado. | 10 → 11<br>Adicionados: `s04-x01` |
| [5](../006.pdf#page=5) | Dois quadros, 10 prefixos cada; títulos e subtítulos acima. | Adicionados título, subtítulo e legendas Múltiplos/Submúltiplos; mantidas grafias yota, zeta, fento, ato e expoentes impressos. | 24 → 28<br>Adicionados: `s05-x01`, `s05-x02`, `s05-x03`, `s05-x04` |
| [6](../006.pdf#page=6) | Ordens de grandeza: 12 pares, de 10⁻¹⁵ m a 10²⁶ m, cabeçalho Ordem de Grandeza (m)/Facto. | Conferidos expoentes e fatos; adicionados três títulos. Valores astronômicos impressos não foram recalculados nem atualizados. | 14 → 17<br>Adicionados: `s06-x01`, `s06-x02`, `s06-x03` |
| [7](../006.pdf#page=7) | Gráfico Metals : Density; eixo Density (gram/cm3); 20 barras e 20 números impressos. | Todos os metais, valores e unidade entraram em expected e em audit.chart_data, em pares ordenados. Não foi inventada uma tabela na origem. A tabela acessível derivada é representação válida. | 1 → 1<br>Modificados: `s07-i01` |
| [8](../006.pdf#page=8) | Table 12-9, Experimental Bond Lengths (in nanometers); 14 linhas visuais de dados. | Adicionados título/número e unidade; mantida a célula de molécula vazia na segunda ligação de CH₃I, com associação por célula vertical compartilhada. Mantidos H₂SAlBr₃ e (H₃Si)₂NN(SiH₃)₂ exatamente como impressos. | 16 → 18<br>Adicionados: `s08-x01`, `s08-x02` |
| [9](../006.pdf#page=9) | Cinco tópicos sob O que é importante. | Adicionados SI, interconversão e notação científica; completado o tópico de algarismos significativos nas medidas experimentais e operações. | 3 → 6<br>Adicionados: `s09-x04`, `s09-x05`, `s09-x06`<br>Modificados: `s09-x03` |
| [10](../006.pdf#page=10) | Título, tópico azul Átomo, tabela de 3 partículas × 6 colunas, duas notas, fonte e duas linhas verdes. | Adicionados tópico, título da tabela, nota † e fonte; expandida nota *. Mantidos Kg, Shiver, massas, cargas e spins do original. | 9 → 13<br>Adicionados: `s10-x05`, `s10-x06`, `s10-x07`, `s10-x08`<br>Modificados: `s10-x02` |
| [11](../006.pdf#page=11) | URL no alto e captura do NIST mostrando busca por mass. | URL adicionada como texto literal; mantida descrição semântica da captura, sem transformar links do PDF em instruções de navegação. | 1 → 2<br>Adicionados: `s11-x01` |
| [12](../006.pdf#page=12) | Recordando, lâmpada, notação A/Z à esquerda de E e duas definições. | Conferida posição: A superior esquerdo, Z inferior esquerdo; mantidos objetos e definições. A imagem raster não contém camada textual nativa. | 5 → 5<br>Mantidos após conferência |
| [13](../006.pdf#page=13) | Título Massa atômica; parágrafo raster de três frases. | Adicionadas as duas frases de definição e completada a frase do enxofre de 32 u. Não confundir o título nativo com a proveniência raster do parágrafo. | 2 → 4<br>Adicionados: `s13-x03`, `s13-x04`<br>Modificados: `s13-x02` |
| [14](../006.pdf#page=14) | Tabela periódica sobre pergaminho, modelos de água e texto vermelho Há isótopos...... | Texto vermelho separado em anotação literal; descrição da imagem mantém tabela, H/O e água, sem duplicar a exigência da legenda. | 1 → 2<br>Adicionados: `s14-x01`<br>Modificados: `s14-i01` |
| [15](../006.pdf#page=15) | Parágrafo de elemento/isótopos, ficha 17/Cl/35.453 e tabela com 2 isótopos. | Completadas definição e explicação dos isótopos, exemplo 35/37 e título da tabela. Conferidos 34.97/75.76 e 36.97/24.24 e legenda 35,5u. | 7 → 10<br>Adicionados: `s15-x03`, `s15-x04`, `s15-x05`<br>Modificados: `s15-x01` |
| [16](../006.pdf#page=16) | Diagrama do espectrômetro com injetor, aquecedor, feixe, magneto, partículas e detector. | Removida a alternativa recíproca massa/carga: o diagrama imprime carga/massa. O resto da descrição foi conferido. | 2 → 2<br>Modificados: `s16-i01` |
| [17](../006.pdf#page=17) | Espectro de Cl₂ com cinco picos, quadro amarelo e explicação central. | Adicionados os textos impressos e distinção explícita entre íons atômicos 35/37 e moleculares 70/72/74. Preservado o erro Relative molecular mass 35.45; nota científica abaixo. | 1 → 4<br>Adicionados: `s17-x01`, `s17-x02`, `s17-x03`<br>Modificados: `s17-i01` |
| [18](../006.pdf#page=18) | Parágrafo superior e quatro fichas de carbono com fontes e valores distintos. | Completado parágrafo literal; registrado erro ± 8 e historicidade. Fontes e valores associados em audit.object_associations, incluindo repetição legítima de 12.011 em duas fontes. | 2 → 2<br>Modificados: `s18-x01` |
| [19](../006.pdf#page=19) | Três tópicos do conceito de mol. | Adicionadas definição com carbono-12 e constância do número de entidades; mantido presentem. O texto de Avogadro já existente foi conferido. | 2 → 4<br>Adicionados: `s19-x03`, `s19-x04` |
| [20](../006.pdf#page=20) | Definição/recomendação IUPAC, relação n(B)/N(B), constante e duas referências no rodapé. | Adicionados cabeçalho bibliográfico, periódico, frase explicativa e as duas referências completas. Mantidos fórmula e ponto médio visual na constante; camada textual extrai × nesse lugar. | 3 → 8<br>Adicionados: `s20-x03`, `s20-x04`, `s20-x05`, `s20-x06`, `s20-x07` |
| [21](../006.pdf#page=21) | Dois tópicos e duas formas equivalentes de n = massa/massa molar. | Adicionados os dois tópicos completos; mantidas fórmulas e nota sobre a distinção dimensional entre massas. | 3 → 5<br>Adicionados: `s21-x02`, `s21-x03` |
| [22](../006.pdf#page=22) | Definições de mᵤ/Mᵤ, três equações, igualdade 1 Mᵤ = 1 g mol⁻¹, Aᵣ(B) e seta. | Adicionadas definições, igualdade, título e explicação de Aᵣ(B). Mantida igualdade histórica como impressa, com nota sobre o SI revisado. | 4 → 9<br>Adicionados: `s22-x02`, `s22-x03`, `s22-f04`, `s22-x04`, `s22-x05` |
| [23](../006.pdf#page=23) | Tabela periódica azul com classes representativos/transição/lantanídeos/actinídeos. | Imagem e legenda de massas relativas a ¹²C conferidas; mantida anotação semântica. Não é uma transcrição célula a célula de toda a tabela periódica. | 1 → 1<br>Mantidos após conferência |
| [24](../006.pdf#page=24) | Seis fotos com rótulos de substância e estado físico; fórmula da tartrazina abaixo. | Alternativas reorganizadas por conceito; adicionados seis rótulos literais com (l)/(s). Substância, forma e cor não substituem umas às outras. Notas e seção abaixo explicam os limites lexicais. | 8 → 14<br>Adicionados: `s24-x03`, `s24-x04`, `s24-x05`, `s24-x06`, `s24-x07`, `s24-x08`<br>Modificados: `s24-i01`, `s24-i02`, `s24-i03`, `s24-i04`, `s24-i05`, `s24-i06` |
| [25](../006.pdf#page=25) | Estrutura de H₂SO₄, modelos de bolas/bastões e preenchimento, legendas Fórmulas estrutural e Molécula. | Conferida estrutura; separados forma e cores dos dois modelos. Mantida a discordância Fórmulas estrutural. | 5 → 5<br>Modificados: `s25-i01`, `s25-i02` |
| [26](../006.pdf#page=26) | Tartrazina à esquerda, PET entre colchetes com n à direita; duas legendas inferiores. | Adicionado Molécula sob tartrazina; separados os conceitos de grupo sulfonato, repetição, colchetes e anel aromático nas estruturas descritivas. | 5 → 6<br>Adicionados: `s26-x04`<br>Modificados: `s26-c01`, `s26-c02` |
| [27](../006.pdf#page=27) | Balão com vapor violeta e amostra escura em placa; I₂ (s), molecular. | Conferidos quatro objetos; removida a alternativa pó para a forma dos cristais. I₂ (s) identifica o sólido, não o vapor no balão. | 4 → 4<br>Modificados: `s27-i02` |
| [28](../006.pdf#page=28) | Quatro painéis do pentaceno, legenda inglesa e citação portuguesa com DOI. | Completada citação em português; número de painéis separado do conceito painéis nas alternativas semânticas. | 3 → 3<br>Modificados: `s28-i01`, `s28-x02` |
| [29](../006.pdf#page=29) | Dois arranjos de NaCl; primeiro Cl⁻ azul/Na⁺ vermelho, segundo cloreto verde/sódio roxo. | Conceitos de identidade, geometria e ambas as cores separados; relações de legenda preservadas em metadados. Mantido Cela unitária. | 4 → 4<br>Modificados: `s29-i01`, `s29-i02` |
| [30](../006.pdf#page=30) | Rede de sulfato de cobre, legenda Iônico, Cu²⁺ e estrutura do sulfato com textos. | Adicionada legenda Iônico; SO₄⁻ preservado com nota de erro de carga, pois a espécie sulfato é SO₄²⁻. | 7 → 8<br>Adicionados: `s30-x06` |
| [31](../006.pdf#page=31) | Tabela periódica raster de íons; grupos 1–18 e Gases Nobres. | Conferida descrição e exemplos de cargas existentes. Mantida como figura semântica, não convertida artificialmente em centenas de fragmentos de texto. | 1 → 1<br>Mantidos após conferência |
| [32](../006.pdf#page=32) | Halogênios: 13 pares, começando F⁻/Fluoreto; fósforo: título e 7 pares. | F⁻ reclassificado para table-row mantendo s32-t01-h; HALOGÊNIOS acrescentado como legenda textual. FÓSFORO reclassificado como legenda; ambas tabelas header=0, com contagens de dados corrigidas. | 23 → 24<br>Adicionados: `s32-x01`<br>Modificados: `s32-t01`, `s32-t01-h`, `s32-t02`, `s32-t02-h` |
| [33](../006.pdf#page=33) | Enxofre: título e 6 pares; nitrogênio: título e 4 pares; sem nomes de colunas. | ENXOFRE e NITROGÊNIO reclassificados para legendas textuais; header=0. Mantido S²⁻/Sulfito, erro científico do original. | 14 → 14<br>Modificados: `s33-t01`, `s33-t01-h`, `s33-t02`, `s33-t02-h` |
| [34](../006.pdf#page=34) | Célula de SiC com legenda Si/C, ferro cinza e duas representações cúbicas. | Conferidos desenhos e legendas; separados conceitos de cubo, esferas, centro e cor nas alternativas. Mantidos os seis IDs e as legendas REDE Covalente estendida e metálico. | 6 → 6<br>Modificados: `s34-i01`, `s34-i03`, `s34-i04` |
| [35](../006.pdf#page=35) | Definições de fórmulas empíricas e moleculares e sequência de exemplos. | Completada definição empírica, adicionada molecular e exemplos NaCl, C, Na, Fe; preservados Al₂O₃, Fe₃O₄, CaCO₃ e H₂O₂/HO. A justaposição Fe₃O₄CaCO₃ do original é documentada, sem inserir pontuação fictícia. | 6 → 11<br>Adicionados: `s35-x07`, `s35-x08`, `s35-x09`, `s35-x10`, `s35-x11`<br>Modificados: `s35-x02`, `s35-x04`, `s35-x05` |
| [36](../006.pdf#page=36) | Fração percentual, definição de n e exemplo de 1 mol de CaCO₃. | Conferidos três mols de O, numerador/denominador e ×100%; mantidos quatro objetos. | 4 → 4<br>Mantidos após conferência |
| [37](../006.pdf#page=37) | Enunciado de vitamina C, três itens a/b/c e estrutura do ácido ascórbico. | Conferidos enunciado, itens e legenda; mantidos seis objetos e representação descritiva da estrutura. | 6 → 6<br>Mantidos após conferência |
| [38](../006.pdf#page=38) | Explicação inicial, fração de massa percentual, amostra de 8 g e três massas. | Adicionada explicação inicial e completado enunciado da amostra; mantidos 3,270 g C, 0,366 g H e 4,360 g O, sem ajustar arredondamentos. | 5 → 6<br>Adicionados: `s38-x05`<br>Modificados: `s38-x01` |
| [39](../006.pdf#page=39) | Passo 1 raster, passo 2 nativo e fórmula n = massa em 100 g/massa molar. | Adicionado passo 2; preservado de cada em elemento no passo 1. Proveniência mista registrada. | 2 → 3<br>Adicionados: `s39-x02` |
| [40](../006.pdf#page=40) | Explicação superior, três quantidades unidas por chave Em 100 gramas, razão e duas fórmulas tentativas. | Adicionados O = 3,41 mol, chave, explicações e fórmula de índices fracionários C₃,₄₁H₄,₅₄O₃,₄₁ como LaTeX. Mantidos somos capaz e os ??? do original. | 4 → 9<br>Adicionados: `s40-x05`, `s40-x06`, `s40-x07`, `s40-x08`, `s40-f01` |
| [41](../006.pdf#page=41) | Parágrafo inteiramente raster sobre fórmula empírica e múltiplos. | Completada segunda frase, incluindo C₆H₈O₆/C₉H₁₂O₉/C₁₂H₁₆O₁₂ e qualquer outro múltiplo; primeira frase mantida. | 2 → 2<br>Modificados: `s41-x02` |
| [42](../006.pdf#page=42) | Introdução, comparação 176,14/88,06 g mol⁻¹, quociente e conclusão C₆H₈O₆. | Adicionadas introdução, massa empírica e explicação do fator dois; valores e 2,000 impressos preservados. | 3 → 6<br>Adicionados: `s42-x03`, `s42-x04`, `s42-x05`<br>Modificados: `s42-f01` |

## Pontos que exigem interpretação explícita

**Slide 7 — associação dos 20 pares.** `audit.chart_data` mantém cada metal em inglês, equivalente em português, valor com duas casas impressas e unidade comum `gram/cm3` (semanticamente `g/cm³`). A ordem segue o eixo, de Aluminum a Zinc. O gráfico tem barras verticais; não é originalmente uma tabela. Uma descrição por objeto ou uma tabela acessível derivada pode representar esses dados. A lista de termos no CSV foi completada; sua mera presença no slide não prova a associação, que ainda depende da integração do avaliador.

**Slide 17 — massa atômica e molecular.** O quadro amarelo imprime *Relative molecular mass 35.45* junto de Cl₂. O número 35.45 é compatível com massa atômica relativa do cloro; a massa molecular relativa de Cl₂ é aproximadamente 70.90 (inferência pela soma de dois átomos). O literal incorreto foi anotado em `s17-x02`, sem substituir 35.45 por 70.90. As associações de picos são [³⁵Cl]⁺/35, [³⁷Cl]⁺/37, [³⁵Cl³⁵Cl]⁺/70, [³⁵Cl³⁷Cl]⁺/72 e [³⁷Cl³⁷Cl]⁺/74. O eixo vertical tem escala de intensidade relativa, mas as barras não têm números de intensidade impressos: não foram inventadas intensidades exatas. Referência científica auxiliar para a nota, sem substituir a fonte primária: [CIAAW, cloro](https://www.ciaaw.org/chlorine.htm).

**Slide 24 — alternativas semânticas.** `SiC|carbeto de silício;pó;preto|negro|escuro` exige identificação, forma e cor separadamente; “pó” não é sinônimo de SiC. Tartrazina é separada de pó e amarelo; Cu/cobre é separado da forma das partículas e da cor acobreada; NaCl/sal é separado da forma cristalina; silício é separado do lingote/cilindro. Rótulos com (s)/(l) são texto literal à parte, para não tratar estado físico como nome da substância. A descrição de cada foto deve pertencer àquela foto. O avaliador ainda usa substrings e recall de 0,6, podendo aceitar descrição incompleta ou termos emprestados de outra foto; o dataset não declara essa aceitação suficiente.

**Slides 32–33 — títulos e cabeçalhos.** Nenhuma das quatro tabelas imprime nomes de coluna equivalentes a “íon” e “nome”; esses são papéis semânticos inferidos, registrados apenas como metadados. HALOGÊNIOS fica acima da tabela; FÓSFORO, ENXOFRE e NITROGÊNIO ficam na faixa superior interna. Todos são legendas/títulos. As contagens corretas de dados são 13/7/6/4, duas colunas, zero cabeçalhos semânticos. `s32-t01-h` é a primeira linha de dados F⁻/Fluoreto; `s32-t02-h`, `s33-t01-h` e `s33-t02-h` são textos de legenda. Não foram inventados cabeçalhos ausentes no PDF.

## Erros e particularidades da fonte preservados

| Slide | Impresso / particularidade | Tratamento |
|---|---|---|
| 3, 19 | Definições de unidades anteriores ao SI revisado, inclusive mol por 12 g de carbono-12. | Preservar como conteúdo histórico, sem atualizar o documento. |
| 5 | yota, zeta, fento, ato. | Preservar grafias impressas. |
| 6 | Ordens astronômicas impressas, inclusive Terra–Sol 10¹² m. | Preservar valores da tabela, sem recalcular distâncias. |
| 8 | H₂SAlBr₃ na linha S—Al e (H₃Si)₂NN(SiH₃)₂ na linha Si—N. | Preservar o agrupamento literal, sem tentar reparar quimicamente a fonte. |
| 10 | Kg e Shiver na fonte bibliográfica. | Preservar, embora kg seja o símbolo SI e o sobrenome usual seja Shriver. |
| 13 | “vezes maior” na comparação de massas. | Preservar a expressão, sem reescrever como uma definição científica nova. |
| 17 | Massa molecular relativa de Cl₂ rotulada 35.45. | Preservar literal; distinguir em nota da massa atômica e dos picos moleculares. |
| 18 | 12,0107 ± 8, “ultimo” e afirmação “mais recente”. | Preservar; a notação 12.0107(8) na ficha indica incerteza 0.0008, não 8; não atualizar a alegação histórica. |
| 19 | “átomos presentem”. | Preservar a grafia. |
| 21–22 | Igualdade numérica simplificada de massas e 1 Mᵤ = 1 g mol⁻¹. | Preservar. Massa molar tem dimensão distinta da massa de uma entidade; no SI revisado Mᵤ não é exatamente 1 g mol⁻¹. |
| 25 | “Fórmulas estrutural”. | Preservar a discordância. |
| 30 | SO₄⁻ sob a estrutura de sulfato. | Preservar a carga única impressa; nota distingue SO₄²⁻. |
| 33 | S²⁻ / Sulfito. | Preservar o nome incorreto; o íon é sulfeto, enquanto sulfito corresponde a SO₃²⁻ em outra linha da própria tabela. |
| 35 | “fórmulas moleculares: descreve”; Fe₃O₄CaCO₃ sem separador. | Preservar a concordância e registrar a justaposição; manter ambos os exemplos sem inventar sinal. |
| 38 | Massas da amostra somam 7,996 g para o enunciado 8 g. | Preservar a precisão e o arredondamento; não ajustar os dados para fechar a soma. |
| 39–40 | “de cada em elemento”, “somos capaz”, índices fracionários e ???. | Preservar texto e etapa intermediária da exposição. |
| 42 | 176,14/88,06 = 2,000. | Preservar; o quociente calculado é aproximadamente 2,000227, compatível com o arredondamento mostrado. |

Referência auxiliar para a nota histórica sobre mol e Mᵤ: [BIPM, realização do mol no SI revisado](https://www.bipm.org/documents/20126/41489679/SI-App2-mole.pdf/be4dea74-a526-e49b-f497-11b393665401). Essas referências fundamentam notas científicas; somente o PDF determina o conteúdo esperado.

## Compatibilidade e pendências de integração com Acessilia PR #850

O CSV mantém as sete colunas e todos os tipos já reconhecidos por `scripts/bench/slide_case.py`. O bloco JSON `audit` é metadado descritivo adicional: **o avaliador atual o ignora**. Os padrões proibidos, títulos e contagem de slides foram mantidos; a descrição de tabelas e de execução degradada foi esclarecida. Novas linhas de texto raster também estão sob a exigência de preservação: `kind=text` não significa “texto extraível nativo”.

Código de referência inspecionado: [PR #850](https://github.com/A11yDevs/acessilia/pull/850), head `a9c12cc9c27e94879e010b0cdfce9544eb6b3d57`, especialmente `scripts/bench/slide_case.py` e `tests/test_slide_case_e2e.py`. Pendências abaixo devem ser integradas ao avaliador, sem afrouxar o dataset:

| Pendência | Evidência no avaliador / impacto | Integração necessária |
|---|---|---|
| Símbolos científicos | `normalize` usa NFKC e casefold: subscrito/sobrescrito e maiúsculas/minúsculas podem colapsar (CO/Co, índices e cargas). | Normalização ciente do domínio; preservar a diferença semântica de símbolos, índices e cargas. |
| Fórmulas | `_latex_words` e recall de 0,8 verificam palavras/números no slide, sem demonstrar numerador, denominador, expoentes ou igualdade. | Comparação estrutural/semântica e representações acessíveis equivalentes, por objeto. |
| Descrições de imagens | `_terms_recall` busca termos no slide inteiro; recall de 0,6 não exige todos os conceitos. | Vincular descrição a cada objeto; validar conceitos e relações de cada foto, inclusive o slide 24. |
| Tabelas | `table` é ignorado em `score_text`; linhas e cabeçalhos são buscados lexicalmente com tolerância de distância. | Verificar contagens, células vazias, spans, títulos, papéis de cabeçalho e associação entre cada fórmula e nome. Não depender do sufixo -h do ID. |
| Valores de gráficos | Recall de termos não liga um metal ao seu número; trocar valores pode manter todos os termos. | Consumir `audit.chart_data` ou esquema equivalente; exigir os 20 pares, a unidade e os vínculos corretos. Aplicar o mesmo princípio aos picos e legendas registrados em `audit.object_associations`. |
| Aprovação TXT/PDF/UA | `DeckOutputs.passed_by_kind()` une IDs aprovados em qualquer saída; um formato pode compensar falha do outro. | Gates separados por formato, inclusive texto, imagens, tabelas, fórmulas e conformidade PDF/UA. |

Casos negativos recomendados para essa integração: trocar Gold/Platinum sem mudar o conjunto de números; remover somente amarelo da foto da tartrazina; colocar “cobre” apenas em outra foto; trocar subscrito por sobrescrito numa carga; inverter a fração de massa; apresentar as duas colunas de tabela sem pares; remover um objeto só no TXT e outro só no PDF/UA. Esses casos devem reprovar onde há perda semântica.

As falhas [#868](https://github.com/A11yDevs/acessilia/issues/868) (glifo .notdef/PDF/UA) e [#869](https://github.com/A11yDevs/acessilia/issues/869) (`Row N:` em TXT pt-BR) continuam sendo problemas do produto. Nenhum padrão foi removido, nenhuma não conformidade foi tornada esperada. [#615](https://github.com/A11yDevs/acessilia/issues/615) continua exigindo validação de staging; esta auditoria não executa processamento remoto nem comprova a qualidade das saídas entregues.

## Comparativo antes/depois

**237 → 304 anotações; 67 adicionadas, 43 modificadas e 0 removidas. Todos os 237 IDs anteriores foram preservados; 304 IDs únicos no resultado.** As 43 modificações incluem notas/contexto, sem necessariamente alterar expected. O comparativo completo, campo a campo, está em [AUDIT_DIFF.csv](AUDIT_DIFF.csv), com as colunas id, page, change, field, before e after; adições incluem todos os sete campos para permitir reconstrução.

| Tipo | Antes | Depois |
|---|---:|---:|
| chemical-structure | 5 | 5 |
| formula | 10 | 12 |
| image | 31 | 31 |
| table | 12 | 12 |
| table-header | 12 | 8 |
| table-row | 95 | 96 |
| text | 72 | 140 |

A queda de cabeçalhos de 12 para 8 é uma correção de papel semântico: três títulos viraram texto e uma linha virou dado. A quantidade de imagens (31) e estruturas químicas (5) foi mantida. O slide 7 é um único gráfico, mesmo com 20 pares de dados. Contagens e scorecards antigos não são diretamente comparáveis à cobertura ampliada: reavaliar ambos os resultados com a mesma revisão do dataset.

## Validação e limites

Executar `python3 input/presentation-reference/validate.py` na raiz do dataset. O validador usa apenas a biblioteca padrão e verifica UTF-8/CSV, largura das linhas, JSON sem chaves duplicadas, regexes, tipos aceitos, IDs únicos, correspondência ID/página, cobertura de 42 páginas, duplicidades literais, quantidade de células/linhas/cabeçalhos de cada tabela, referências de metadados, categorias e valores do gráfico, títulos e SHA-256 do PDF. Também reconstrói as diferenças contra o commit-base por `git show` e exige igualdade exata com AUDIT_DIFF.csv. O clone precisa conter o commit-base (um clone raso pode exigir fetch).

A compatibilidade é verificada por carregamento e pontuação pelo código real de `slide_case.py` do PR #850, sem modificar o avaliador. Essa execução verifica a aceitação do formato, não a correção semântica dos algoritmos. Controles negativos temporários verificam rejeição de ID duplicado, tabela com contagem incorreta, divergência entre gráfico e metadados e diff desatualizado. Resultados executados: validador aprovado (42 páginas, 304 IDs únicos, 12 tabelas consistentes, PDF inalterado e diff reproduzido); código original do avaliador do PR #850 carregou as 304 linhas e pontuou os 292 objetos não estruturais sem erro de parser/tipo em uma entrada sintética contendo 42 cabeçalhos. Essa entrada testa formato e não é evidência de uma saída acessível aprovada. Os quatro controles negativos foram rejeitados pelos motivos esperados: ID duplicado, contagem de linhas, divergência dos valores do gráfico e diff desatualizado. `git diff --check` também passou.

Foram reproduzidos dois falsos positivos do avaliador original: `normalize("CO") == normalize("Co")` e `normalize("SO₄⁻") == normalize("SO⁴⁻")`; uma descrição sintética com todos os valores do slide 7 deslocados para o metal seguinte ainda foi aprovada pelo recall de termos. Esses resultados confirmam as pendências e não foram usados para reduzir exigências do dataset.

Limites: a inspeção foi realizada por um único auditor, sem adjudicação independente. Não há transcrição exaustiva das figuras periódicas ou da captura do navegador. Descrições semânticas aceitam variações linguísticas; a gramática lexical atual não expressa todas as paráfrases válidas nem garante associações espaciais. Não foi rodado E2E remoto ou veraPDF sobre uma saída nova. Os metadados adicionais documentam vínculos corretos, mas exigem implementação no avaliador para virarem gates automáticos. A completude avaliada aqui é a dos tópicos, exemplos, tabelas explícitas, relações e objetos descritos neste relatório, não uma garantia de inventário de todo texto microscópico nas figuras.
