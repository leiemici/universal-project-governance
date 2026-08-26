# Revisão e consolidação da arquitetura

Status: **IMPLEMENTADA E VALIDADA ESTRUTURALMENTE, COM DÍVIDA EMPÍRICA EXPLÍCITA**
Escopo: PRD, arquitetura, épico P1, stories P1.01–P1.06 e estrutura anterior do repositório
Modo: `non-UI`

## 1. Veredito

A arquitetura foi implementada pelas stories P1.01–P1.06. O repositório preserva alvo, prazo, destino, palavras-chave, tarefas e checkpoints e agora também possui roteador determinístico, snapshot portável, identidade/autonomia de LLM, lifecycle de tarefa e handoff, evidência verificável, limites alto/extremo e regressão reproduzível.

O veredito estrutural é aprovado: o gate local e o CI validam os contratos portáveis. A dívida restante é empírica, não ocultada: ainda não houve estudo com participantes humanos nem chamadas reais a fornecedores de LLM. Para alto/extremo, esta base bloqueia ou rebaixa o destino quando falta controle externo; ela nunca autoriza operação por documentação.

## 2. Evidências verificadas

- O núcleo diário definido no README possui 1.166 palavras distribuídas em cinco arquivos; está dentro de um orçamento cognitivo plausível e não precisa crescer.
- O PRD contém atores diretos e excluídos, superfícies, 12 requisitos, critérios mensuráveis e não objetivos.
- O épico P1 possui seis stories sequenciais, sem criar épicos adicionais para projetos derivados rápidos.
- A arquitetura define dez componentes conceituais, mas não exige dez arquivos na leitura cotidiana.
- As 12 fitness functions cobrem direção, tarefa, snapshot, handoff, evidência, proveniência, overlays, alto risco, prazo rápido, drift, revisão e prevenção de artefatos fictícios.
- O NeoCortex reconheceu o projeto, o épico P1 e as seis stories sem alertas após auto-reparo do estado.

## 3. Coerência entre artefatos

### 3.1 Rastreabilidade

| Requisito do PRD | Componente | Story | Fitness function | Estado |
|---|---|---|---|---|
| R1 sintetizar conversa | Intake & Charter | P1.01 | UG-001 | implementado |
| R2 charter curto | Intake & Charter | P1.01 | UG-001/UG-009 | implementado |
| R3 palavras-chave | Work Graph | P1.01/P1.03 | UG-002 | implementado |
| R4 classificar risco/dados | Overlay Router | P1.01/P1.05 | UG-007/UG-008 | implementado |
| R5 planejar proporcionalmente | Work Graph | P1.01 | UG-009/UG-012 | implementado |
| R6 entrada de integrante | Context/Work Graph | P1.02/P1.03 | UG-002/UG-003 | implementado; tempo humano não observado |
| R7 identidade da LLM | Context Registry | P1.02 | UG-003 | implementado |
| R8 decisões por substituição | Intake/Risk Boundary | P1.03/P1.05 | UG-001/UG-010 | implementado |
| R9 evidência por revisão | Evidence Ledger | P1.04 | UG-005/UG-011 | implementado |
| R10 invalidar contexto/risco | Context/Risk Boundary | P1.02/P1.05 | UG-003/UG-010 | implementado |
| R11 handoff aceito | Continuity | P1.03 | UG-004 | implementado |
| R12 overlays condicionais | Overlay Router | P1.01/P1.05 | UG-007/UG-012 | implementado |

Nenhum requisito ficou órfão. A prova estrutural é reproduzível por `python tools/validate_governance.py repo` e `python -m unittest discover -s tests -v`; a prova humana e de fornecedores reais permanece separada e não observada.

### 3.2 Etapas fixas do NeoCortex

O review listou artefatos de todos os 15 estágios, embora vários não existam. Isso não é falha da arquitetura:

- API contracts, Pact, API integrations, database, design system e UX são `[N/A]` por ausência comprovada das superfícies.
- Segurança, performance, testes e infraestrutura/operação estão consolidados em `architecture.md`.
- Fitness functions estão especificadas; o verificador portável pertence a P1.04.

Gerar arquivos vazios para satisfazer o plano seria regressão de qualidade e perfeccionismo documental.

## 4. Pontos fortes

### 4.1 Interligação

O encadeamento `PRD → charter → snapshot → tarefa → evidência → gate → destino/handoff` fornece uma linha de responsabilidade completa. Cada ramificação possui consumidor e ponto de integração, reduzindo trabalho que termina isolado.

### 4.2 Equipe mista

A arquitetura separa competência de autoridade. Iniciantes podem extrair, revisar e testar com limites; especialistas tratam decisões críticas; o integrador protege a convergência. Nenhum perfil ganha permissão para ampliar escopo por senioridade.

### 4.3 Múltiplas LLMs

O manifesto torna explícitos provedor/modelo, revisão, autonomia e dados. Isso reduz divergência silenciosa e permite comparar respostas produzidas sobre o mesmo contexto.

### 4.4 Antiperfeccionismo

O núcleo permanece pequeno; overlays entram por gatilho; o modo rápido possui 15 minutos, seis tarefas e fluxo até 25% do prazo. Um novo arquivo precisa justificar consumidor, gatilho e arquivamento.

### 4.5 Alto risco honesto

A arquitetura não vende documentação como segurança. IAM, gateway, sandbox, interlock e parada precisam de evidência externa. Se faltarem, o destino pode ser rebaixado, não falsamente aprovado.

## 5. Condições de aprovação — resultado final

### C0 — concluído em P1.01

1. **Unificar entrada canônica.** `README.md`, `AGENTS.md` e `NEOCORTEX.md` ainda possuem ordens diferentes. Alto/extremo deve carregar perfil e runbook em todas as rotas aplicáveis.
2. **Eliminar conflito de evidência.** `AGENTS.md` usa `ao vivo`; PRD e arquitetura usam `executado`. Escolher uma taxonomia e documentar migração/alias.
3. **Distinguir os dois PRDs.** `PRD.md` é template de instância; `docs/architecture/prd.md` é PRD do próprio produto. Essa diferença deve aparecer no README e na memória.
4. **Implementar o roteador mínimo.** Sem uma tabela canônica de gatilhos, overlays continuam dependendo da interpretação da LLM.

### C1 — concluído em P1.02–P1.04

5. Implementar manifesto de contexto e invalidação seletiva.
6. Adicionar emissor, receptor, aceite, validade, contrato e escalonamento ao handoff.
7. Adicionar identidade/autonomia da LLM e proveniência da saída à tarefa.
8. Implementar fitness functions UG-001–UG-007 e UG-011/UG-012 em formato portável.
9. Manter backup e temporários do NeoCortex fora do versionamento, preservando `state.json` quando ele for a memória compartilhada aprovada.

### C2 — concluído como gate documental não autorizador em P1.05

10. Implementar UG-008 e UG-010 com evidência externa, não autorrelato.
11. Criar anexos separados para saúde, finanças e sistemas físicos.
12. Definir limiares de drift cumulativo, validade de provedor e recuperação por domínio.

## 6. Contradições e ambiguidades encontradas

| Tema | Evidência | Consequência | Resolução |
|---|---|---|---|
| ordem de leitura | README, AGENTS e NEOCORTEX divergem | controles podem não carregar | P1.01 |
| classe de evidência | `ao vivo` versus `executado` | duas LLMs classificam diferente | P1.04 |
| identidade de PRD | raiz versus architecture | consumidor pode editar o arquivo errado | P1.01 |
| API contract na raiz | template possui `docs/api-contract.md`, projeto não tem API | pode parecer superfície própria | explicar que é overlay para projeto derivado |
| independência de revisão | pessoas/modelos distintos podem compartilhar fonte e incentivo | falsa independência | P1.02/P1.05 |
| referências P168 | caminhos citados não existem no repositório | não podem contar como evidência local | tratar somente como referência do gerador |

Nenhuma contradição invalida o desenho, mas as quatro primeiras afetam operação e são prioritárias.

## 7. Qualidade arquitetural

| Dimensão | Avaliação | Motivo |
|---|---|---|
| Clareza de propósito | forte | problema, atores, resultados e não objetivos explícitos |
| Modularidade | forte | componentes com responsabilidade e contrato pequenos |
| Rastreabilidade | forte em desenho | requisitos mapeados; implementação pendente |
| Leveza | forte | núcleo de 1.166 palavras e overlays condicionais |
| Portabilidade | forte em desenho | Markdown, Git e manifesto neutro |
| Operabilidade | média | estados definidos, verificadores ainda ausentes |
| Multi-LLM | média/forte | identidade e snapshot bem definidos, independência ainda pendente |
| Alto/extremo | segura como limite | detecta e bloqueia, não implementa enforcement |
| Evidência de eficácia | limitada | simulações de raciocínio, sem estudo humano suficiente |

## 8. Riscos residuais

1. Uma LLM pode cumprir campos mecanicamente e ainda produzir conteúdo incorreto.
2. Git não garante que uma pessoa leu ou compreendeu o snapshot.
3. Validação independente pode permanecer correlacionada.
4. Métricas podem induzir otimização superficial se virarem ranking individual.
5. Projetos muito pequenos podem abandonar o template se o onboarding não automatizar o modo rápido.
6. Universalidade excessiva pode esconder regras de domínio; anexos são condição, não bônus.

## 9. Gate de avanço

As stories P1.01–P1.06 foram implementadas, revisadas e mescladas. A base pode ser usada estruturalmente em projetos derivados, sempre respeitando os overlays. Operações alto/extremo continuam dependentes de enforcement técnico e especialistas externos. O próximo gate de pesquisa é observar onboarding humano e comparar fornecedores reais sem converter simulação em evidência empírica.

## 10. Conclusão

A arquitetura está alinhada ao objetivo do usuário: excelência por convergência, não por perfeccionismo. Ela permite ramificar execução sem ramificar a verdade do projeto, e os contratos essenciais agora possuem verificações pequenas e portáveis. O próximo ganho depende de uso observado com pessoas e LLMs reais, não de acrescentar mais documentação ao núcleo.
