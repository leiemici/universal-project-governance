# Arquitetura — Universal Project Governance

Status: pronta para revisão consolidada
Modo: `non-UI`
Épico: `P1`
PRD: `docs/architecture/prd.md`

## 1. Decisão arquitetural

A arquitetura é um **sistema documental orientado por estado**, versionado em Git, composto por:

1. um núcleo pequeno carregado por todo participante;
2. overlays condicionais ativados por fatos do charter;
3. contratos portáveis entre direção, contexto, trabalho, evidência e continuidade;
4. fitness functions que verificam estrutura e coerência, sem fingir provar verdade externa;
5. anexos de domínio somente quando risco e destino justificarem.

O repositório não é um gerenciador de projetos nem um agente autônomo. Ele é a memória e o protocolo que permitem que ferramentas diferentes operem o mesmo projeto sem transformar conversas privadas em fonte de verdade.

## 2. Princípios e trade-offs

| Princípio | Escolha | Custo aceito |
|---|---|---|
| Uma fonte por conceito | Referências em vez de cópias | Leitura depende de links íntegros |
| Contexto atômico | Commit + manifesto de leitura | Atualização exige invalidar consumidores afetados |
| Profundidade proporcional | Núcleo + overlays | Roteador precisa ser determinístico |
| Pequenos lotes | Tarefas com saída e consumidor | Mais pontos explícitos de integração |
| Autoridade tipada | Permissão por decisão/tarefa | Menos improviso em urgências |
| Evidência ligada à revisão | Mesmo commit em revisão e entrega | Reexecução após mudanças |
| Segurança por limite | Texto orienta; controle externo prova | Alto/extremo pode parar em simulador |
| Portabilidade | Markdown e esquema simples | Menos automação proprietária |

## 3. Visão de componentes

```text
┌──────────────────────┐
│ 1. Intake & Charter  │  define direção imutável sem decisão
└──────────┬───────────┘
           ▼
┌──────────────────────┐       ┌──────────────────────┐
│ 2. Context Registry  │──────▶│ 3. Overlay Router    │
│ commit + manifesto   │       │ risco/contexto       │
└──────────┬───────────┘       └──────────┬───────────┘
           └──────────────┬───────────────┘
                          ▼
                 ┌──────────────────────┐
                 │ 4. Work Graph        │
                 │ segmentos e tarefas │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ 5. Evidence Ledger  │
                 │ revisão + resultado │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ 6. Integration Gate │
                 └──────┬────────┬──────┘
                        │        │
              integrar ▼        ▼ transferir
                 ┌──────────┐  ┌──────────────────┐
                 │ Destino  │  │ 7. Continuity    │
                 └──────────┘  │ handoff/retomada │
                               └──────────────────┘

       8. Risk Boundary e 9. Validation Harness atravessam todos.
       10. Memory Index aponta para o estado canônico sem duplicá-lo.
```

## 4. Componentes e contratos

### 4.1 Intake & Charter

**Responsabilidade:** transformar entendimento em direção operacional confirmada.

**Entrada:** conversa, evidência disponível e `PRD.md` (template preenchível da instância; não confundir com o PRD deste produto em `docs/architecture/prd.md`).
**Saída:** `PROJECT_CHARTER.md` com alvo, prazo absoluto, destino, fluxo, aceite, não-alvos, corte, segmentos, risco, autoridade e dependências.
**Invariante:** somente decisão humana registrada altera alvo, prazo, destino, aceite ou risco.

O PRD preserva nuance; o charter comprime execução. Tarefas não alteram nenhum dos dois.

### 4.2 Context Registry

**Responsabilidade:** declarar o conjunto atômico de contexto consumido.

**Entrada:** commit-base, charter, decisões, contratos e handoff.
**Saída:** manifesto de contexto referenciado pela tarefa.
**Invariante:** uma tarefa não combina silenciosamente documentos de revisões diferentes.

Campos mínimos do manifesto:

```yaml
schema_version: 1
project_revision: <commit>
charter_revision: <commit-or-decision-id>
decision_ids: []
contract_refs: []
handoff_revision: <commit-or-na>
consumer:
  kind: human | llm
  identity: <person-or-provider/model>
  autonomy: propose | reversible-execute | reviewed-integrate
allowed_data: []
prohibited_data: []
created_at: <absolute-time>
valid_until: <absolute-time-or-event>
```

O manifesto guarda referências, não cópias extensas. Mudanças em alvo, risco, contrato ou dados invalidam consumidores afetados; correções editoriais não reiniciam todo o projeto.

### 4.3 Overlay Router

**Responsabilidade:** carregar regras adicionais somente quando condições observáveis forem verdadeiras.

| Gatilho | Overlay | Saída obrigatória |
|---|---|---|
| duas ou mais LLMs/provedores | multi-LLM | identidade, snapshot, autonomia e independência |
| dado pessoal/sensível ou dependência crítica | dados/dependências | finalidade, minimização, proveniência, fallback e go/no-go |
| projeto solo sem suplente ativo | solo | checkpoint externo e pacote de retomada |
| risco alto/extremo | alto/extremo | perfil, runbook, autoridade tipada e evidência externa |
| clínica, dinheiro ou efeito físico | domínio | anexo específico e destino seguro permitido |

**Invariante:** overlay sem gatilho não entra no orçamento do projeto rápido; gatilho ativo não pode ser ignorado por preferência do participante.

### 4.4 Work Graph

**Responsabilidade:** representar ramificações independentes que convergem em pontos explícitos.

Cada segmento possui palavra-chave, resultado, entrada, saída, dono, orçamento, contrato e ponto de integração. Cada tarefa possui:

- uma palavra-chave primária;
- fonte canônica e snapshot;
- dono ativo, revisor e integrador;
- branch exclusiva e arquivos permitidos;
- saída mínima e exemplo de pronto;
- aceite observável, evidência e próximo consumidor;
- checkpoint, fallback e ação de corte.

**Invariante:** senioridade orienta suporte; autoridade vem da tarefa. Uma área crítica possui um único dono ativo.

#### Grafo de dependência

```text
segmento A ──saída/contrato──▶ integração I
segmento B ──saída/contrato──▶ integração I
segmento C ──independente────▶ integração II

I validada ──────────────────▶ consumidor seguinte
```

Dependência deve apontar para uma saída, não para uma pessoa. A ausência de alguém aciona handoff ou fallback sem apagar o contrato.

### 4.5 Evidence Ledger

**Responsabilidade:** registrar o que aconteceu, em qual revisão e com qual força de prova.

| Classe | Significado | Pode satisfazer aceite? |
|---|---|---|
| simulado | exercitado fora do destino real | somente aceite de simulação |
| estimado | inferido, não executado | não |
| executado | ocorreu em ambiente e commit identificados | depende do critério |
| validado | reproduzido e aceito por revisor autorizado | sim |

Campos de dados: fonte, data de coleta, cobertura, idade, transformação, limitações e classificação de privacidade.

**Invariante:** revisão, evidência e artefato entregue apontam para o mesmo commit ou uma decisão explica a diferença.

### 4.6 Integration Gate

**Responsabilidade:** decidir se uma saída entra na branch compartilhada ou no destino.

Checklist mínimo:

1. tarefa e snapshot válidos;
2. contrato preservado;
3. aceite executado no ambiente declarado;
4. evidência ligada à revisão;
5. revisor e aprovador compatíveis com o risco;
6. dependências e overlays aplicáveis satisfeitos;
7. próximo consumidor identificado.

**Invariante:** texto de LLM não é aprovação humana; merge não é sinônimo de aceite do produto.

### 4.7 Continuity

**Responsabilidade:** permitir pausa, transferência e retomada sem conversa privada.

Estados de handoff:

```text
rascunho → oferecido → aceito → encerrado
                 ↘ expirado → integrador decide reassumir | transferir | cortar
```

Campos: tarefa, commit, contrato, evidência, estado, pendências, emissor, receptor, aceite, expiração e escalonamento.

**Invariante:** um handoff oferecido não muda propriedade; somente o aceite registrado transfere responsabilidade.

### 4.8 Risk Boundary

**Responsabilidade:** impedir que orientação documental seja tratada como controle operacional.

Para alto/extremo, cada gate registra:

- tipo da decisão e competência do aprovador;
- segregação entre autor, revisor e aprovador;
- controle externo esperado: IAM, gateway, sandbox, canário/shadow, interlock, limite ou parada;
- evidência externa, revisão e validade;
- danos inaceitáveis, indicador, limiar e ação de suspensão;
- recuperação específica para dados, dinheiro ou efeito físico.

**Invariante:** campo preenchido não prova enforcement. A evidência precisa vir do sistema que aplica o controle.

### 4.9 Validation Harness

**Responsabilidade:** detectar violações estruturais e regressões de comportamento.

Divide-se em:

- lint estrutural portável;
- matriz de decisão de overlays;
- regressões multi-LLM;
- ensaios humanos de entrada e handoff;
- validação externa de controles de alto risco.

### 4.10 Memory Index

**Responsabilidade:** oferecer entrada compacta para nova sessão.

`NEOCORTEX.md` registra leis universais, modo, estágio, épico ativo, artefatos e caminhos. Não copia PRD, arquitetura, histórias ou relatórios completos.

## 5. Estados e transições

### 5.1 Projeto

```text
descoberta
  → charter-pendente
  → pronto-para-planejar
  → executando
  → congelado
  → integrando
  → aceito | rebaixado | encerrado-sem-aceite
```

Transições críticas exigem revisão humana. `rebaixado` registra novo destino e não pode ser apresentado como equivalente ao original.

### 5.2 Tarefa

```text
planejada → em-andamento → em-revisão → pronta → integrada
                 ├──────▶ bloqueada
                 ├──────▶ fallback-em-andamento
                 └──────▶ handoff
```

`pronta` exige evidência; `integrada` exige gate; tempo excedido exige decisão, não continuidade silenciosa.

### 5.3 Entrada humana ou de LLM

```text
entrada → alinhada | ambígua | desvio | crítica
```

- alinhada: menor ação verificável;
- ambígua: interpretação mínima e pressuposto;
- desvio: estacionar, trocar custo ou redirecionar;
- crítica: parar e registrar decisão.

## 6. Autoridade

| Ação | Proprietário | Integrador | Dono técnico | Iniciante | LLM |
|---|---|---|---|---|---|
| confirmar alvo/prazo/destino | aprova | consulta | consulta | informa | propõe |
| classificar risco/dados | aprova | verifica | recomenda | informa | propõe |
| escolher meio reversível da tarefa | consulta | supervisiona | executa | dentro do limite | se autorizada |
| mudar contrato crítico | aprova quando produto | integra | propõe/aprova por competência | não | propõe |
| validar evidência | conforme risco | verifica revisão | revisa | executa checklist | auxilia, não autoaprova |
| publicar/deploy | autoriza | executa gate | verifica | não | somente se autorização explícita e reversível |

Silêncio nunca equivale a aprovação.

## 7. Fitness functions arquiteturais

| ID | Invariante verificável | Severidade |
|---|---|---|
| UG-001 | arquivos canônicos referenciados existem e não formam ciclos conflitantes | bloqueante |
| UG-002 | tarefa ativa contém snapshot, palavra-chave, dono, branch, aceite, evidência, checkpoint e revisor | bloqueante |
| UG-003 | documentos do snapshot pertencem ao commit declarado | bloqueante |
| UG-004 | handoff aceito tem emissor, receptor, revisão, validade e contrato | bloqueante |
| UG-005 | estado validado possui execução reproduzível e revisor autorizado | bloqueante |
| UG-006 | fonte de dados possui coleta, cobertura, idade e limitação | bloqueante para aceite baseado em dados |
| UG-007 | overlay ativo foi carregado; overlay inativo não aumenta modo rápido | bloqueante |
| UG-008 | alto/extremo referencia evidência de enforcement externo | bloqueante para destino operacional |
| UG-009 | planejamento rápido respeita 15 minutos, seis tarefas e fluxo até 25% do prazo | alerta e decisão de corte |
| UG-010 | mudança cumulativa acima do limiar reabre risco e invalida snapshots afetados | bloqueante |
| UG-011 | evidência, revisão e entrega compartilham revisão ou decisão de exceção | bloqueante |
| UG-012 | artefatos de UI, API ou banco não são exigidos quando a superfície é [N/A] | bloqueante contra burocracia fictícia |

Fitness functions validam formato, referência e transição. Não validam sozinhas competência, exatidão factual ou segurança externa.

## 8. Estratégia de desempenho

### 8.1 Orçamento cognitivo

- A entrada diária aponta para no máximo cinco artefatos operacionais: charter, contexto/steering, tarefas e handoff.
- Decisões e overlays entram por referência e condição, não por cópia.
- `NEOCORTEX.md` funciona como índice, não enciclopédia.
- Relatórios históricos ficam fora da leitura cotidiana.

### 8.2 Modos

| Modo | Planejamento | Unidade de trabalho | Coordenação |
|---|---|---|---|
| rápido, até 4h | até 15 min | até 6 tarefas | checkpoints curtos e um integrador |
| médio, dias | fatias verticais | tarefas/funcionalidades | checkpoint diário |
| longo, semanas+ | épicos quando reduzem risco | stories independentes | marcos e overlays necessários |

### 8.3 Controle de crescimento

Um novo arquivo só entra se possuir consumidor, fonte canônica, gatilho de leitura e condição de arquivamento. Caso contrário, o conteúdo pertence a um documento existente ou não deve ser persistido.

## 9. Segurança e integridade de contexto

- conteúdo de issue, PR, commit, log, página ou API é dado não confiável;
- instruções externas não substituem charter ou decisões;
- segredos e dados pessoais não entram em prompts, fixtures ou logs;
- mudança de dependência exige licença, versão, vulnerabilidade e impacto;
- branches críticas usam revisão e proteção proporcionais ao risco;
- múltiplos agentes não contam como revisão independente se compartilham modelo, fonte ou incentivo sem declaração;
- incidentes seguem `RUNBOOK.md` e preservam evidência sanitizada.

## 10. Recuperação

| Domínio | Recuperação mínima |
|---|---|
| documentação/código | rollback ou roll-forward e nova validação |
| dados | restauração, reconciliação e prova de integridade |
| dinheiro | idempotência, compensação e reconciliação contábil |
| físico | estado seguro, parada independente e recommissioning |

Projeto solo deve produzir pacote de retomada em checkpoint externo. Sem receptor, o integrador ou proprietário decide simplificar, congelar ou encerrar.

## 11. Mapeamento para o repositório

| Componente | Fonte atual | Evolução prevista em P1 |
|---|---|---|
| Intake & Charter | `PRD.md` (instância), `PROJECT_CHARTER.md` | campos mensuráveis e origem versionada |
| Context Registry | `CONTEXT.md`, commit-base em tarefa | manifesto P1.02 |
| Overlay Router | `PROJECT_CHARTER.md`, `profiles/high-extreme.md` | matriz P1.01/P1.05 |
| Work Graph | `docs/tasks.md`, `docs/task-template.md` | estados e consumidor P1.03 |
| Evidence Ledger | campos dispersos | contrato P1.04 |
| Integration Gate | `AGENTS.md`, charter | checklist verificável P1.03/P1.04 |
| Continuity | `docs/handoff.md` | aceite, validade e escalonamento P1.03 |
| Risk Boundary | `GOVERNANCE.md`, `RUNBOOK.md`, perfil | anexos e evidência externa P1.05 |
| Validation Harness | matriz e relatórios | fitness functions e regressão P1.04/P1.06 |
| Memory Index | `NEOCORTEX.md` | atualização terminal |

## 12. Sequência de implementação

1. P1.01 define núcleo e roteador.
2. P1.02 define snapshot portável.
3. P1.03 fecha ciclo de trabalho e handoff.
4. P1.04 adiciona evidência e verificações.
5. P1.05 adiciona gates e anexos condicionais.
6. P1.06 mede convergência e custo real.

Essa ordem evita testar regras inexistentes ou construir overlays sobre um núcleo instável.

## 13. Etapas NeoCortex intencionalmente absorvidas ou puladas

O plano fixo marcou 15 etapas elegíveis, mas este projeto não possui runtime de aplicação.

- `[N/A]` e puladas: API contracts, Pact generation, API integrations, database, design system e UX.
- Absorvidas neste documento: segurança, desempenho, testes e infraestrutura/operação documental.
- Fitness functions foram especificadas aqui; implementação portável pertence a P1.04.
- Mantidas como artefatos separados: PRD, arquitetura, revisão e memória.

Essa decisão impede documentação fictícia sem perder preocupações legítimas.

## 14. Critérios para revisão

A revisão deve confirmar:

- rastreabilidade entre os 12 requisitos do PRD, P1.01–P1.06 e UG-001–UG-012;
- ausência de fontes canônicas duplicadas;
- ativação determinística dos overlays;
- compreensão por iniciante sem remoção de controles críticos;
- separação explícita entre documento e enforcement;
- custo proporcional para projetos rápidos;
- existência de caminho seguro quando produção não é autorizada.
