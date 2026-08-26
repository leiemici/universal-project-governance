# Epic P1 — Arquitetura universal convergente

Status: generated
Fonte: `docs/architecture/prd.md`

## Feature Spec Summary

### Intenção

Consolidar a base existente em um núcleo pequeno e overlays condicionais que preservem direção, contexto, autoridade, evidência e continuidade entre pessoas e LLMs diferentes.

### Objetivos

- tornar toda contribuição rastreável do PRD ao aceite;
- permitir entrada segura de especialistas, intermediários e iniciantes;
- versionar o contexto consumido por humanos e LLMs;
- tornar handoffs aceitos, expiráveis e escaláveis;
- transformar regras importantes em validações estruturais;
- separar claramente orientação documental de enforcement externo.

### Não objetivos

- criar interface, banco ou API;
- adicionar épicos a projetos rápidos que usem o template;
- gerar wrappers para cada fornecedor de LLM;
- declarar documentação suficiente para operações clínicas, financeiras ou físicas.

### Evidência de aceite

- testes estruturais dos campos e referências canônicas;
- dez cenários de regressão executados em três níveis de LLM;
- ensaio humano de entrada em projeto medido em até 10 minutos;
- relatório que distingue regra documental de controle técnico externo.

### Suposições

- Git é a memória compartilhada e os participantes conseguem ler o repositório;
- o proprietário identifica prazo e destino antes da execução;
- integrações de alto risco são implementadas fora deste template e apenas referenciadas como evidência.

## Architecture Spec Summary

### Superfícies afetadas

- núcleo: charter, contexto, steering, tarefas, decisões e handoff;
- overlays: multi-LLM, dependência/dados e alto/extremo;
- validação: manifesto, lint estrutural e regressões;
- memória: `NEOCORTEX.md` e referências canônicas.

### Pontos de integração

`PRD → charter → snapshot → plano → tarefa → branch → evidência → revisão → integração → handoff ou encerramento`

### Riscos

- núcleo crescer até virar burocracia;
- overlays serem ignorados por ordem de leitura incompleta;
- lint validar presença sem validar verdade;
- múltiplos agentes usarem contexto correlacionado e parecerem independentes;
- documentação ser confundida com enforcement.

### Referências P168

- `core/standards/spec-driven-development.md`
- `core/templates/specs/feature-spec-template.md`
- `core/templates/specs/architecture-spec-template.md`

## Contract Inventory

| Contrato | Estado | Observação |
|---|---|---|
| API | [N/A] | O repositório não expõe API própria |
| Banco | [N/A] | O repositório não possui banco próprio |
| UI | [N/A] | O produto é documental e non-UI |
| Eventos | [N/A] | Não há runtime de eventos próprio |
| Configuração | Necessário | Manifesto de contexto e gatilhos de overlay devem possuir formato portável |
| Git | Necessário | Commit-base, branch, revisão e evidência formam o contrato de integração |

## ADR / NFR Notes

- **ADR candidato 1:** núcleo universal pequeno mais overlays ativados por risco e contexto.
- **ADR candidato 2:** Git revisionado como unidade atômica de contexto e evidência.
- **ADR candidato 3:** regras documentais nunca contam como prova de enforcement externo.
- **NFR:** portabilidade entre fornecedores de LLM.
- **NFR:** entrada compreensível por iniciantes sem reduzir gates críticos.
- **NFR:** projetos de até quatro horas mantêm planejamento inicial em até 15 minutos.
- **NFR:** nenhuma duplicação deliberada de fonte canônica.

## Stories

| ID | Resultado |
|---|---|
| P1.01 | Núcleo e ativação determinística dos overlays |
| P1.02 | Snapshot de contexto e identidade de LLM |
| P1.03 | Ciclo de tarefa, branch e handoff aceito |
| P1.04 | Evidência, proveniência e fitness functions portáveis |
| P1.05 | Limites alto/extremo e anexos de domínio |
| P1.06 | Regressão multi-LLM e validação humana de entrada |

## Traceability

| Requisito | Contrato | Story | Aceite/validação | Dívida aberta |
|---|---|---|---|---|
| R1–R4 direção e segmentação | Git/config | P1.01 | AC-P1.01-01..04 | nenhuma |
| R6–R7 entrada e múltiplas LLMs | manifesto | P1.02 | AC-P1.02-01..05 | independência correlacionada |
| R8–R11 decisão, evidência e handoff | Git | P1.03 | AC-P1.03-01..05 | expiração proporcional |
| R9 e critérios de evidência | lint/config | P1.04 | AC-P1.04-01..05 | semântica além de presença |
| R12 risco e overlays | evidência externa | P1.05 | AC-P1.05-01..05 | anexos regulatórios |
| todos os critérios mensuráveis | matriz de validação | P1.06 | AC-P1.06-01..05 | amostra humana inicial |

### Cobertura pública

- Requisitos órfãos: nenhum identificado nesta versão.
- Contratos órfãos: nenhum; contratos técnicos inexistentes estão marcados [N/A].
- Exemplos não validados: os dez cenários existentes precisam de nova execução após implementação.
- Exclusões: segredos, dados pessoais, prompts privados e logs brutos.
