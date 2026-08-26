# Registro canônico de contexto

Cada tarefa executada por uma LLM usa um manifesto em `contexts/<task-id>.context.json`, validável por `docs/context-manifest.schema.json`. O manifesto identifica a revisão exata, o subconjunto de contexto consumido, a identidade do consumidor, sua autonomia e os dados permitidos.

## Criar um snapshot

1. Parta de uma branch sincronizada e obtenha o commit completo com `git rev-parse --verify HEAD^{commit}`.
2. Leia a ordem de `docs/overlay-router.md` e registre somente os documentos realmente consumidos, sempre com caminho e revisão completa.
3. Registre decisões, contratos e handoff aplicáveis; ausência conhecida usa lista vazia ou `null`, nunca texto inventado.
4. Para LLM, registre fornecedor, modelo, situação da versão, fontes do contexto, autonomia e autorização quando necessária.
5. Registre dados permitidos, proibidos, classificação e finalidade.
6. Liste em `invalidation.watched_refs` cada referência material e as classes de mudança que afetam esta tarefa.
7. Defina validade por horário absoluto ou evento verificável e grave o manifesto antes da execução.

O snapshot contém referências, não cópias extensas. Conversas privadas podem ser sintetizadas em decisão ou confirmação pública; o conteúdo integral não entra no repositório.

## Gate de execução

Leitura do repositório nunca depende de manifesto válido. Execução por LLM exige, ao mesmo tempo:

- JSON compatível com o schema;
- `status: valid`;
- `project_revision` resolvendo para commit Git;
- tarefa apontando para este arquivo;
- identidade e fontes do consumidor presentes;
- autonomia declarada e autorização quando ela permite execução;
- política de dados preenchida;
- validade ainda vigente;
- nenhuma referência observada alterada materialmente.

Se qualquer item falhar, a autonomia efetiva é `read-only`. A LLM pode explicar o bloqueio e propor correção; não pode executar, integrar ou publicar.

## Invalidação seletiva

Compare o snapshot com a revisão nova:

1. Identifique arquivos e decisões alterados.
2. Classifique cada mudança como `target`, `deadline`, `destination`, `acceptance`, `risk`, `data`, `contract`, `decision`, `handoff`, `task` ou `editorial`.
3. Para cada manifesto, procure a mesma referência em `invalidation.watched_refs`.
4. Invalide somente quando caminho e classe de mudança coincidirem. Registre motivo, horário e substituto, se existir.
5. Mudança de charter em alvo, prazo, destino, aceite, risco ou dados é material para toda tarefa que consome o charter.
6. Mudança de contrato, decisão ou handoff afeta apenas manifestos que referenciam esse item.
7. Alteração não observada não invalida. Correção `editorial` só preserva validade quando a classificação foi registrada por revisor autorizado e o conteúdo operacional não mudou.

Um snapshot invalidado é imutável como histórico. Crie outro arquivo ou revisão com novo `snapshot_id`; não reescreva o passado para parecer válido.

## Validade e eventos

`valid_until` aceita horário absoluto ou evento. Exemplos de evento: novo commit na branch de integração, decisão substituída, contrato versionado ou fim do checkpoint. Um evento precisa de referência verificável; frases como “até ficar velho” são inválidas.

## Interpretação por ferramentas diferentes

Toda ferramenta deve produzir a mesma visão mínima:

```text
snapshot_id
task_id
project_revision
consumer.kind + consumer.identity
consumer.provider/model quando LLM
consumer.autonomy
data_policy.allowed + prohibited
status + valid_until
watched_refs
next_consumer
```

Campos extras proprietários são proibidos no núcleo (`additionalProperties: false`). Metadados opcionais ficam somente em `extensions`, sob namespace estável; todo consumidor pode ignorá-los. Extensão não altera identidade, autonomia, dados, validade ou invalidação e nunca contém segredo, prompt integral ou dado pessoal. Mudança no núcleo exige nova versão do schema e migração explícita.

## Limite de confiança

O manifesto prova quais referências e limites foram declarados. Ele não prova que o modelo realmente internalizou o conteúdo, que fornecedores distintos são independentes, nem que um controle externo foi aplicado.
