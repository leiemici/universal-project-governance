# Project Charter

## Diretiva operacional — preencher e confirmar antes de executar

- **ALVO:** uma frase com usuário, mudança observável e limite principal.
- **PRAZO:** data/hora absoluta, fuso e tempo total disponível.
- **DESTINO:** local e estado exato da entrega final.
- **FLUXO:** entrada → lógica essencial → resultado visível.
- **ACEITE:** evidência mínima que prova o fluxo.
- **NÃO-ALVOS:** itens sedutores que não podem consumir o prazo.
- **REGRA DE CORTE:** o que sai primeiro quando o tempo restante não comporta o plano.

Uma pessoa deve conseguir ler apenas este bloco e explicar o projeto corretamente em menos de um minuto.

## Fonte no PRD

- Versão/commit do `PRD.md`:
- Lacunas ainda abertas que podem alterar a diretiva:

## Segmentação por palavra-chave

Use de duas a seis palavras-chave canônicas. Toda tarefa possui exatamente uma palavra-chave primária.

| Palavra-chave | Resultado obrigatório | Dono | Orçamento | Ponto de integração | Estado |
|---|---|---|---|---|---|
| | | | | | |

## Contexto complementar

- Problema e usuário:
- Resultado demonstrável:
- Prazo: rápido (até 4h) | médio (dias) | longo (semanas+)
- Obrigatório:
- Bônus / fora de escopo:
- Equipe, habilidades e responsáveis:

## Classificação proposta pela LLM, confirmada por humano
- Risco: baixo | médio | alto | extremo
- Dados: públicos | pessoais | sensíveis | proibidos nesta fase
- Dependências: nenhuma | externa | crítica
- Governança: equipe fechada | stakeholder externo | comunidade aberta
- Responsável pela entrega e suplente:
- Orçamento total, reserva e limite de parada:
- Verificação pré-commit/merge/deploy e responsável:
- Branch de integração:

## Autoridade da LLM

- Autonomia autorizada: orientar | executar reversível | integrar com revisão | somente propor
- A LLM pode reduzir detalhe, recomendar fallback e redirecionar trabalho incompatível com a diretiva.
- A LLM não pode redefinir ALVO, PRAZO, DESTINO, risco ou aceite; mudança exige decisão humana registrada.
- Entrada ambígua não vira tarefa ampla: a LLM oferece a interpretação mínima alinhada e explicita o pressuposto.

## Dados e dependências
- Finalidade, origem e campos mínimos permitidos:
- Campos proibidos e retenção/exclusão:
- Dependência, dono, teste de acesso e prazo de go/no-go:
- Fallback: mock | cache | manual | nenhum

## Portões
- Escrita em produção, dinheiro, dado regulado/sensível, credenciais administrativas, efeito físico ou ação irreversível tornam o projeto automaticamente alto/extremo.
- Alto/extremo: não iniciar integração, deploy ou uso de dados reais sem aprovação humana explícita.
- Alto/extremo: autor, revisor e aprovador devem ser pessoas distintas; ausência de aprovador significa parar.
- Dependência crítica: definir dono, fallback e evidência de acesso.
- Rápido: máximo de seis tarefas de 20–30 minutos e um fluxo demonstrável antes de bônus.
- Se uma solicitação não mapear para palavra-chave, aceite ou destino, classifique como desvio e não a execute silenciosamente.
- Mudança material de escopo, dado, dependência, usuário ou ambiente reabre a classificação de risco.
- Deploy exige branch, revisão imutável, ambiente e artefato; evidência e aprovação devem referir a mesma revisão.
