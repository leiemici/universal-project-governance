# Context snapshots

Armazene aqui um manifesto por tarefa: `<task-id>.context.json`.

- Valide pelo contrato `../docs/context-manifest.schema.json`.
- Siga criação e invalidação em `../docs/context-registry.md`.
- Nunca salve prompts integrais, transcrições privadas, segredos ou dados pessoais.
- Não use um exemplo como evidência de execução.
- Snapshot antigo permanece como histórico; o sucessor recebe outro `snapshot_id` e referencia o anterior em `invalidation.superseded_by`.

Esta pasta começa sem manifesto de exemplo para impedir que placeholders sejam confundidos com contexto válido.
