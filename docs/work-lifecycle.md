# Ciclo de trabalho e continuidade

Este é o contrato canônico para tarefa, branch, revisão, integração e handoff. Git continua sendo o histórico técnico; estes registros explicam autoridade e intenção sem copiar o histórico do Git.

## Identidade de uma tarefa

Toda tarefa ativa possui:

- `task_id`, palavra-chave, fonte canônica e requisito;
- vínculo explícito com ALVO, ACEITE e DESTINO;
- `context_snapshot`, `base_commit` e prazo de validade;
- um `owner` ativo, um `reviewer` e um `integrator` identificáveis;
- uma branch exclusiva e os caminhos que o dono pode alterar;
- entrada, saída mínima, critério observável de aceite e próximo consumidor;
- orçamento, checkpoint, fallback e ação de corte;
- `evidence_commit`, `review_commit` e `delivery_commit` quando aplicáveis.

O dono é exclusivo por tarefa e por área crítica. Revisor e integrador podem coincidir em risco baixo ou médio quando o charter permitir; em risco alto ou extremo, vale a segregação definida pelo overlay.

## Estados da tarefa

```text
planejada → em-andamento → em-revisão → pronta → integrada
                 ├──────▶ bloqueada
                 ├──────▶ fallback-em-andamento
                 └──────▶ handoff-pendente

bloqueada ──────────────▶ em-andamento | fallback-em-andamento | handoff-pendente | cortada
fallback-em-andamento ──▶ em-revisão | bloqueada | handoff-pendente | cortada
handoff-pendente ───────▶ em-andamento | bloqueada | cortada
```

Regras de transição:

1. `planejada → em-andamento`: dono, branch, caminhos permitidos e snapshot válido estão registrados.
2. `em-andamento → em-revisão`: saída está no `evidence_commit` e o revisor foi avisado.
3. `em-revisão → pronta`: critério foi executado; evidência e revisão apontam para o mesmo commit.
4. `pronta → integrada`: integrador aprovou o gate e o `delivery_commit` é o commit revisado ou há exceção humana registrada.
5. `→ bloqueada`: bloqueio, impacto e próxima decisão possuem responsável e checkpoint.
6. `→ fallback-em-andamento`: fallback já previsto foi ativado sem alterar ALVO, ACEITE ou DESTINO.
7. `→ handoff-pendente`: existe um handoff `oferecido`; o dono atual ainda mantém a responsabilidade.
8. `→ cortada`: integrador ou proprietário registrou a decisão de corte.

Tempo excedido nunca muda o estado sozinho. No checkpoint, o integrador escolhe integrar, simplificar, usar fallback, transferir ou cortar.

## Regra da branch

- Uma tarefa possui uma branch ativa. A branch isola o lote de trabalho; ela não concede autoridade fora dos caminhos permitidos.
- Duas tarefas não alteram simultaneamente o mesmo contrato ou área crítica. O integrador pausa uma delas ou registra ordem e ponto de integração.
- Antes de editar, o dono confirma o `base_commit`. Mudança material no contexto invalida o snapshot afetado.
- Merge, revisão e validação sempre citam o commit exato. Alteração posterior invalida o aceite daquele commit e exige nova evidência proporcional.

## Estados do handoff

```text
rascunho → oferecido → aceito → encerrado
                    ↘ expirado → escalado → reassumido | substituído | cortado
```

Campos obrigatórios:

- `handoff_id`, `task_id`, estado e última atualização;
- emissor, receptor proposto e integrador;
- dono atual e dono proposto;
- commit, snapshot, contrato e arquivos permitidos;
- saída existente, evidência, pendências e próximo passo;
- critério de aceite, validade absoluta e regra de escalonamento;
- aceite do receptor com identidade, data e commit lido.

Regras:

1. `rascunho` e `oferecido` não transferem propriedade.
2. Somente `aceito`, com receptor e integrador confirmados, troca o dono da tarefa.
3. Se o receptor não responder até `valid_until`, o handoff vira `expirado`; o integrador registra `escalado` e decide reassumir, substituir ou cortar.
4. Aceite após expiração exige nova oferta com snapshot e contrato atuais.
5. `encerrado` só ocorre quando o novo dono confirma retomada ou a tarefa termina.

## Evidência de uma única revisão

Para uma tarefa pronta ou integrada:

```text
evidence_commit == review_commit == delivery_commit
```

Se os commits diferirem, a tarefa volta a `em-revisão` até repetir a evidência. A única exceção é uma decisão humana registrada que prove que a diferença é não material e identifique os três commits.

## Reentrada remota

Quem retorna lê o roteador, o snapshot da tarefa e o handoff vigente. A pessoa não cria outro PRD e não reassume por memória ou mensagem privada. Se o contrato mudou, o integrador oferece uma tarefa atualizada; se nada mudou, registra a retomada no handoff existente.
