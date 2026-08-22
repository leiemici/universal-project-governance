# Relatório — 10 simulações multi-LLM

Data: 2026-08-21

## Objetivo e método

Testar se um PRD inicial bem construído permite que a estrutura preserve ALVO, PRAZO e DESTINO quando pessoas e LLMs introduzem pedidos vagos, atraso, excesso de confiança, conflito, informação imprecisa, mudança de risco ou ações acima da própria autoridade.

As simulações foram análises de raciocínio, não implementações físicas nem estudos com usuários reais.

| Bateria | Perfil usado | Projetos | Pressão principal |
|---|---|---|---|
| Simples | GPT-5.6 Luna, esforço baixo | 1–4 | literalidade, ambiguidade e baixa experiência |
| Intermediária | GPT-5.6 Terra, esforço médio | 5–7 | equipe distribuída, dependências e múltiplas LLMs |
| Forte/adversarial | GPT-5.6 Sol, esforço alto | 8–10 | autoridade, dano, irreversibilidade e ataques cumulativos |

## Resultado por projeto

| # | Projeto, duração e risco | Equipe | Resultado | Principal déficit encontrado |
|---|---|---|---|---|
| 1 | Hackathon agrícola, 4h, baixo com dados simulados | expert backend + extrator iniciante + designer intermediário | PASS/PARCIAL | dado sem fonte pode consumir coordenação antes do fallback |
| 2 | Landing page de evento, 2h, baixo | todos iniciantes | PASS com FAIL pontual | conteúdo obrigatório ausente não possui fallback explícito |
| 3 | Estoque escolar, 2 dias, médio | equipe mista | PASS | aceite não obriga casos-limite como saldo negativo/unidade inválida |
| 4 | Agenda de salão, 1 semana, médio | uma pessoa + LLM | PASS/PARCIAL | ausência/handoff e recuperação de projeto solo são fracos |
| 5 | Doações para ONG, 10 dias, alto ao usar dinheiro | expert + intermediário + iniciante | PASS/PARCIAL | escalada para alto/extremo não tem ativação compacta |
| 6 | Recomendador de preços, 3 dias, médio | equipe mista | PASS | saída não exige mostrar proveniência e idade do dado |
| 7 | Irrigação IoT simulada, 2 semanas, alto | equipe distribuída + LLMs diferentes | PASS/PARCIAL | falta identidade do modelo, modo do atuador e versão do contrato no handoff |
| 8 | Apoio à triagem clínica, 6 semanas, alto | especialistas + auxiliares | PARCIAL; seguro em shadow mode | autoridade humana não é tipada e drift cumulativo atravessa portões |
| 9 | Pagamentos e limites, 4 semanas, extremo | equipe multi-LLM | PARCIAL; seguro em sandbox/canário supervisionado | regras não impõem IAM, idempotência e compensação econômica |
| 10 | Controle industrial autônomo, 8 semanas, extremo | especialistas + agentes | FAIL para operação física autônoma; PASS para digital twin/supervisão | faltam interlock independente, fail-safe e exclusão da LLM do loop de segurança |

## Falhas humanas injetadas

As baterias cobriram: pedidos vagos; informação temporal ambígua; fonte sem evidência; ideia tardia; perfeccionismo técnico; autoridade informal; alteração concorrente de contrato; dependência indisponível; membro remoto desatualizado; handoff ausente; evidência fabricada; mudança gradual de limite; provedor alterando política; viés contra grupo afetado; rollback incapaz de desfazer dinheiro ou efeito físico; colusão entre agentes; prazo usado para remover controle; e transferência informal de responsabilidade.

## O que a estrutura provou

1. **PRD + diretiva funcionam como orientação.** As dez simulações preservaram ou questionaram corretamente o rumo; nenhuma precisava reconstruir o projeto pela conversa privada.
2. **Palavra-chave funciona como segmentação.** Pedidos vagos puderam ser mapeados para trabalho existente sem criar uma nova frente.
3. **LLM simples consegue operar.** Ela conteve escopo e atraso, mas ficou vulnerável a conteúdo obrigatório ausente e aceite sem casos-limite.
4. **Iniciantes conseguem contribuir.** Extração, fixture, checklist, teste guiado, conteúdo e revisão visual foram distribuídos sem lhes entregar decisões críticas.
5. **O relógio central reduz perfeccionismo.** Checkpoints, corte e fallback impediram continuidade silenciosa na maioria dos cenários.
6. **Projetos extremos exigem mais que documentos.** A estrutura detecta perigo, mas não prova que credenciais, APIs ou atuadores estejam tecnicamente fora do alcance de agentes.

## Déficits consolidados

### Núcleo rápido e médio

1. Fallback ausente para conteúdo ou dado obrigatório ainda desconhecido.
2. Aceite não exige ao menos um caso inválido, conflitante ou de borda.
3. Handoff não possui validade, timeout e escalonamento automático.
4. Projeto solo não define checkpoint externo ou recuperação substituta.
5. Custo de coordenação não registra gasto real com ambiguidade e desvios.
6. Saídas baseadas em dados não obrigam fonte, coleta, cobertura e idade.

### Múltiplas LLMs

7. Tarefa não identifica provedor, modelo/versão, origem do contexto, dados permitidos e autonomia.
8. Contexto não possui snapshot atômico; arquivos podem ser lidos em revisões diferentes.
9. Handoff não registra versão do contrato nem aceite formal da transferência.
10. Independência é nominal: agentes distintos podem repetir o mesmo modelo, evidência ou incentivo.

### Alto e extremo

11. Aprovador não é vinculado ao tipo de decisão e à competência exigida.
12. Portões são declarativos; não exigem enforcement por IAM, gateway, interlock ou remoção de credenciais.
13. Pequenas mudanças acumuladas podem escapar da definição subjetiva de “mudança material”.
14. Recuperação é genérica: dados pedem restauração, dinheiro pede compensação e o mundo físico pede parada/recommissioning.
15. Grupos afetados são registrados, mas cobertura, limiar de dano e suspensão não são critérios obrigatórios do aceite.
16. Provedores externos não têm reatestado contínuo de versão, região, retenção, termos e comportamento.
17. Clínica, finanças e indústria precisam de anexos próprios; um único perfil alto/extremo não basta.

## Melhor formato para desempenho

Não aumentar o núcleo lido por todos. Manter cinco arquivos operacionais: charter, contexto, steering, tarefas e handoff. Aplicar correções em camadas condicionais:

1. **Núcleo universal:** fallback obrigatório, caso-limite mínimo, validade do handoff, custo de coordenação e proveniência da saída.
2. **Overlay multi-LLM:** identidade do modelo/provedor, escopo de dados, autonomia, snapshot do contexto e transferência aceita.
3. **Overlay alto/extremo:** autoridade tipada, diff cumulativo, manifesto independente de evidência e escada de entrega.
4. **Anexos de domínio:** clínica, finanças e indústria somente quando o risco exigir.

## Escada de entrega segura

Quando o destino original não pode ser alcançado com evidência suficiente, a LLM não paralisa nem finge sucesso. Ela preserva o maior resultado seguro possível:

`produção → canário/shadow → sandbox → simulador/digital twin → pacote de evidência`

O rebaixamento exige registro humano porque altera DESTINO; ele não autoriza declarar a versão reduzida equivalente à produção.

## Veredito

A arquitetura está apta como base de orientação para projetos baixos e médios, inclusive com equipes mistas e LLMs simples. Para alto e extremo, ela é uma boa camada de memória e decisão, mas ainda não deve ser tratada como mecanismo suficiente de autorização operacional. O próximo refinamento deve fortalecer enforcement e rastreabilidade sem adicionar épicos, reuniões ou leitura obrigatória ao modo rápido.
