# Regressão — 10 simulações após correções declaradas

Data: 2026-08-21

## Método

Foram repetidos os mesmos dez projetos, falhas humanas e níveis de LLM da bateria original. Somente regras presentes nos arquivos operacionais foram consideradas. Recomendações registradas em `docs/simulation-report-10-projects.md` não contam como correções enquanto não forem incorporadas ao charter, protocolos, templates ou perfis aplicáveis.

## Veredito

- Correções integralmente comprovadas: **0**.
- Correções parciais: **11**.
- Déficits ainda abertos: **6**.
- Regressões temporais comprovadas: **0**.
- Falha estrutural nova detectada: perfil alto/extremo e runbook não pertencem à leitura obrigatória.

As regras continuam preservando direção e contendo escopo. O resultado operacional dos cenários, porém, não mudou materialmente.

## Reexecução dos projetos

| # | Projeto | Resultado atual | Delta |
|---|---|---|---|
| 1 | Hackathon agrícola | PASS/PARCIAL | pequena melhora documental; fallback ainda não é acionado por regra obrigatória |
| 2 | Landing page | PASS/PARCIAL | pequena melhora documental; conteúdo obrigatório ausente ainda depende da interpretação |
| 3 | Estoque escolar | PASS/PARCIAL | sem mudança; caso inválido/de borda continua opcional |
| 4 | Agenda de salão | PASS/PARCIAL | sem mudança; handoff não expira nem escala automaticamente |
| 5 | Doações para ONG | PASS/PARCIAL | sem mudança material; alto/extremo continua declarativo |
| 6 | Recomendador de preços | PASS | sem mudança material; proveniência completa não é obrigatória na saída |
| 7 | Irrigação IoT simulada | PASS/PARCIAL | sem mudança; faltam estado do atuador, identidade LLM e snapshot |
| 8 | Triagem clínica | PARCIAL, somente shadow mode | zero |
| 9 | Pagamentos e limites | PARCIAL, sandbox; canário só com controles externos | zero |
| 10 | Controle industrial autônomo | FAIL físico autônomo; PASS twin/supervisão | zero |

## Estado das 17 correções

| # | Correção esperada | Estado | Evidência atual |
|---|---|---|---|
| 1 | Fallback para conteúdo/dado obrigatório | PARCIAL | há mock/cache/manual, mas sem acionamento obrigatório ou teste universal |
| 2 | Caso inválido/conflitante no aceite | PARCIAL | aceite observável existe; caso de borda não é obrigatório |
| 3 | Validade, timeout e escalonamento do handoff | ABERTO | handoff não possui prazo de validade ou gatilho |
| 4 | Recuperação verificável para projeto solo | PARCIAL | suplente existe; falta checkpoint externo/substituto |
| 5 | Gasto real de coordenação | PARCIAL | orçamento existe; gasto acumulado e limiar não são registrados |
| 6 | Fonte, coleta, cobertura e idade da saída | PARCIAL | origem/evidência são genéricas; campos não são universais na tarefa/saída |
| 7 | Identidade e autonomia da LLM por tarefa | PARCIAL | provedor/modelo devem ser aprovados, mas versão, contexto e dados permitidos não ficam na tarefa |
| 8 | Snapshot atômico do contexto | PARCIAL | commit-base ajuda, mas não fixa o conjunto de documentos lidos |
| 9 | Versão de contrato e aceite formal no handoff | ABERTO | não existem campos obrigatórios |
| 10 | Independência real de agente/evidência | PARCIAL | pessoas distintas existem no alto/extremo; modelo, fonte e incentivo podem continuar correlacionados |
| 11 | Autoridade tipada e prova de competência | PARCIAL | competência é registrada, mas decisão não exige uma classe de autoridade correspondente |
| 12 | Enforcement técnico por IAM/gateway/interlock | ABERTO | portões continuam documentais |
| 13 | Detecção de drift cumulativo | ABERTO | somente mudança “material”/release reabre risco; pequenos diffs podem se acumular |
| 14 | Recuperação específica para dados, dinheiro e físico | PARCIAL | rollback/reconciliação existem, sem protocolos distintos completos |
| 15 | Cobertura e limiar por grupos afetados no aceite | PARCIAL | grupos/indicadores existem, mas não são condição universal de liberação alto/extremo |
| 16 | Reatestado contínuo de provedor | PARCIAL | versão/licença/vulnerabilidade são revistas em mudanças explícitas; mudança silenciosa permanece |
| 17 | Anexos clínico, financeiro e industrial + escada segura | ABERTO | existe somente perfil alto/extremo genérico; escada está apenas no relatório anterior |

## Nova falha de carregamento

`AGENTS.md` e o onboarding do `README.md` não exigem a leitura de `profiles/high-extreme.md` nem de `RUNBOOK.md`. Assim, uma LLM pode cumprir a ordem oficial de leitura e nunca carregar controles de alto/extremo ou recuperação.

## Conclusão

A regressão confirma estabilidade, mas não confirma remediação. Para que a próxima bateria meça melhora real, as recomendações precisam migrar do relatório histórico para regras canônicas e templates condicionais. A prioridade é: corrigir o fluxo obrigatório de leitura, depois núcleo universal, overlay multi-LLM e overlay alto/extremo.
