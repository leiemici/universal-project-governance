# Roteador canônico de contexto

Este é o único ponto de entrada para pessoas e LLMs depois que o proprietário confirma o charter. O núcleo é sempre lido; detalhes extras entram somente quando os fatos normalizados ativam um overlay.

## Ordem obrigatória

1. Leia `PROJECT_CHARTER.md` e confirme que os fatos do roteador foram preenchidos pelo proprietário.
2. Leia `CONTEXT.md` e `docs/steering.md`.
3. Avalie todos os gatilhos de `overlays.json`; overlays simultâneos são cumulativos.
4. Leia `GOVERNANCE.md`, `docs/decisions.md`, `docs/work-lifecycle.md`, `docs/tasks.md` e `docs/handoff.md`.
5. Leia os arquivos adicionais de cada overlay ativo, na ordem declarada no manifesto.
6. Registre na tarefa quais overlays foram avaliados, quais ficaram ativos e quais fatos justificaram a decisão.

Se um fato obrigatório estiver ausente ou tiver valor fora do vocabulário, o roteamento fica `pendente`: nenhuma execução começa até o proprietário corrigir ou confirmar o charter. Nenhuma LLM pode supor o valor mais conveniente.

## Algoritmo determinístico

1. Copie os fatos confirmados do bloco `Fatos para roteamento` do charter e valide tipo/valor contra `facts` em `overlays.json`.
2. Avalie `risk_floor`. Se qualquer condição for verdadeira e o risco confirmado estiver abaixo de `alto`, mantenha `routing-pending` e peça reclassificação humana; não promova o risco silenciosamente.
3. Para cada overlay de `overlays.json`, avalie `activation.any` como OU e `activation.all` como E.
4. Ative o overlay quando sua expressão for verdadeira. Não escolha apenas o overlay de maior risco.
5. Una as leituras e saídas de todos os overlays ativos, removendo duplicatas sem mudar a ordem declarada.
6. Verifique as regras globais do manifesto.
7. Grave o resultado no cabeçalho da tarefa antes de trabalhar.

Operadores permitidos:

- `equals`: o campo é igual ao valor;
- `in`: o campo pertence à lista;
- `at_least`: o número é maior ou igual ao limite;
- `not_equals`: o campo difere do valor.

## Regra do modo rápido

Prazo de até quatro horas não ativa overlay por si só. O projeto usa apenas o núcleo, no máximo seis tarefas e nenhum épico de execução, salvo se outro fato ativar uma proteção. Um overlay ativo adiciona somente suas próprias leituras e saídas; ele não autoriza criar outros artefatos por conveniência.

## Resultado mínimo do roteamento

Registre em cada tarefa:

```text
roteador_schema: 1
fatos_confirmados_em: <data/hora e decisão ou commit>
overlays_avaliados: [multi-llm, dados-dependencias, solo, alto-extremo, dominio]
overlays_ativos: []
leituras_adicionais: []
saidas_obrigatorias: []
```

## Casos de aceite

| Caso | Fatos principais | Ativos esperados | Proteção contra excesso |
|---|---|---|---|
| baixo e rápido | 4h, risco baixo, 1 pessoa com suplente, dados públicos | nenhum | núcleo, sem épico de execução |
| médio | risco médio, equipe humana, dependência externa não crítica | nenhum | dependência comum fica no plano |
| alto | risco alto | alto-extremo | perfil e runbook obrigatórios |
| extremo | risco extremo e efeito financeiro | alto-extremo + domínio | operação sem anexo/enforcement permanece bloqueada |
| simultâneo A | 3 LLMs, dado pessoal, dependência crítica | multi-LLM + dados-dependências | somente dois overlays ativados |
| simultâneo B | 1 pessoa sem suplente, risco alto, efeito físico | solo + alto-extremo + domínio | retomada e limites operacionais acumulados |

## Limite de confiança

O roteador prova somente que o contexto documental correto foi selecionado. Aprovação humana, segurança do sistema, competência profissional e enforcement externo exigem evidência própria. Destino operacional, privilégio administrativo, ação irreversível, dado sensível/proibido ou efeito clínico, financeiro ou físico impõem piso de risco alto; contradição bloqueia o roteamento até decisão humana.
