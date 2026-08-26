# Universal Project Governance

Base portátil para uma pessoa iniciar um projeto com uma LLM, transformar a conversa em direção executável e publicar o mesmo contexto para toda a equipe e outras LLMs.

## Princípio central

A estrutura não tenta eliminar falhas humanas. Ela torna **alvo, prazo, destino e limites** explícitos o bastante para que a LLM detecte ruído, reduza ambiguidade e reconduza o trabalho ao resultado comprometido.

## Ordem de início

1. Conversem livremente e sintetizem o entendimento no `PRD.md`, que é o template preenchível da instância criada a partir deste repositório.
2. A LLM converte o PRD em `PROJECT_CHARTER.md`: uma diretiva curta, verificável e aprovada pelo proprietário.
3. O proprietário confirma os fatos de roteamento no charter; a equipe executa a ordem única de `docs/overlay-router.md`.
4. Definam de duas a seis palavras-chave de segmentação no charter; cada uma aponta para um resultado, dono, orçamento e ponto de integração.
5. Gerem `docs/execution-plan.md` e `docs/tasks.md` de acordo com prazo, risco e equipe. Projeto rápido não recebe épicos automaticamente.
6. Publiquem no GitHub somente após confirmar a diretiva e o primeiro fluxo demonstrável.
7. Quem entrar depois começa por `docs/overlay-router.md`; não existe uma segunda ordem de leitura neste README.

## Fonte de verdade

- `PRD.md` é o template de entendimento preenchido por cada projeto derivado.
- `docs/architecture/prd.md` é o PRD deste repositório-produto e não deve ser preenchido por projetos derivados.
- `PROJECT_CHARTER.md` é a diretiva operacional vigente.
- `docs/decisions.md` altera a diretiva sem apagar a história.
- `docs/tasks.md` mostra execução e responsabilidade por unidade de trabalho.
- `docs/context-registry.md` e `contexts/` mostram qual revisão, autoridade e dados cada consumidor utilizou.
- `docs/handoff.md` mostra onde retomar agora.

Se houver conflito, prevalece a decisão aprovada mais recente. Nenhuma LLM muda alvo, prazo, destino, escopo ou risco silenciosamente.

## Regra de leveza

O volume de planejamento é proporcional ao projeto: até 4 horas usa diretiva, segmentos e no máximo seis tarefas; projetos de dias usam funcionalidades ou fatias verticais; épicos e stories só entram quando duração e dependências justificarem o custo de coordenação.

Mudanças na estrutura são verificadas contra `docs/validation-matrix.md`, que simula entradas vagas, excesso de confiança, escopo tardio, conflito entre LLMs, evidência falsa e mudança de risco.

A bateria comparativa mais recente está em `docs/simulation-report-10-projects.md`. Ela registra dez projetos, três níveis de LLM, déficits observados e o limite atual da estrutura para riscos altos e extremos.

A repetição após as correções declaradas está em `docs/regression-report-10-projects.md`. Ela diferencia recomendações históricas de regras realmente incorporadas e mostra quais déficits continuam abertos.
