# Steering — manutenção automática de rumo

Este ciclo é executado por qualquer LLM antes de propor ou realizar trabalho. Ele não avalia a capacidade moral da pessoa; compara a entrada com a diretiva vigente.

## Compasso

1. Leia ALVO, PRAZO, DESTINO, ACEITE e REGRA DE CORTE no charter.
2. Mapeie a entrada para uma palavra-chave e um resultado de segmento.
3. Calcule se a menor entrega verificável cabe no tempo restante, incluindo integração, revisão e handoff.
4. Confirme que a saída aproxima o DESTINO e pode ser aceita por evidência.
5. Escolha a ação de menor custo e maior reversibilidade.
6. Atualize tarefa ou handoff sem reescrever a história de outra pessoa.

## Classificação da entrada

| Classe | Sinal | Resposta da LLM |
|---|---|---|
| `alinhada` | Mapeia para palavra-chave, aceite e prazo | Executar dentro da autonomia autorizada |
| `ambígua` | Intenção útil, mas saída ou segmento incerto | Propor interpretação mínima e um pressuposto verificável |
| `desvio` | Não aproxima o destino ou consome reserva sem substituir trabalho | Redirecionar, estacionar como bônus ou propor troca equivalente |
| `crítica` | Altera alvo, prazo, risco, dados, custo ou ação irreversível | Parar e solicitar decisão humana registrada |

## Formato curto de redirecionamento

> Entendi `<intenção>`. Para preservar `<ALVO>` até `<PRAZO>`, vou tratar isso como `<PALAVRA-CHAVE>` e entregar `<SAÍDA MÍNIMA>`. `<PARTE FORA>` fica em bônus/decisão porque não aproxima o aceite atual.

## Orçamento de coordenação

Planejamento, conversa, leitura, revisão, integração e handoff consomem tempo do projeto. O plano reserva esse custo explicitamente. Se a coordenação crescer, reduza paralelismo ou escopo antes de reduzir validação crítica.

## Proibição de falsa autonomia

A LLM pode escolher meios reversíveis dentro de uma tarefa aceita. Ela não pode transformar silêncio em aprovação, inventar dados ausentes, ocultar incerteza, fabricar evidência ou declarar integração sem verificar o artefato compartilhado.
