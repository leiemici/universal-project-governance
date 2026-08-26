# Tasks

| ID | Palavra-chave | Tarefa/saída mínima | Dono | Branch exclusiva | Aproxima qual aceite/destino | Orçamento | Checkpoint | Revisor | Estado |
|---|---|---|---|---|---|---|---|---|---|

Estados: `planejada`, `em-andamento`, `bloqueada`, `fallback-em-andamento`, `em-revisão`, `pronta`, `handoff-pendente`, `cortada`, `integrada`.

Cada tarefa inclui contexto, revisão e handoff no orçamento. Tarefa incompleta no checkpoint vira decisão de corte, ajuda ou handoff; não continua silenciosamente.

Uma pessoa atualiza somente as tarefas que possui. Mudança de dono exige handoff aceito; integração é registrada pelo integrador. O status geral é derivado das tarefas, nunca de um campo pessoal sobrescrito.

Detalhes executáveis ficam em uma ficha baseada em `docs/task-template.md`, evitando uma tabela gigante.

Toda tarefa executada por LLM referencia exatamente um manifesto válido em `contexts/<task-id>.context.json`. Sem snapshot, identidade, autonomia ou política de dados válida, a tarefa pode ser lida e discutida, mas não executada.

O contrato de campos, transições, concorrência e vínculo de commits está em `docs/work-lifecycle.md`. A tabela é apenas o índice atual; a ficha da tarefa e o Git preservam o detalhe.
