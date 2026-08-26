# Relatório de regressão P1.06

## Veredito curto

A estrutura convergiu nos **30 testes estruturais simulados**: dez nichos combinados com três perfis comportamentais de LLM. Isso demonstra que as regras versionadas produzem a mesma decisão determinística diante dos erros injetados. Não demonstra desempenho de fornecedores reais nem de pessoas reais.

## O que foi executado

- 10 nichos: hackathon agrícola, landing page, estoque escolar, agenda, doações, preços, irrigação IoT, triagem clínica, pagamentos e controle industrial.
- 3 perfis simulados: simples, intermediário e forte.
- Equipes mistas com especialistas, intermediários e iniciantes em extração, conteúdo, checklist, teste ou revisão visual.
- 30 pares cenário/perfil, todos derivados de `validation/regression-scenarios-P1.06.json`.
- Erros injetados: aumento de escopo, atraso, entrada ambígua, evidência falsa, origem ausente, caminho canônico quebrado, handoff vencido, entrada tardia, ausência de controle, drift e conflito de integração.

## Resultado reproduzível

| Medida | Resultado | Classe de evidência |
|---|---:|---|
| Cenários | 10 | simulado |
| Perfis | 3 | simulado |
| Execuções convergentes | 30/30 | simulado |
| Chamadas reais de LLM | 0 | observado no executor local |
| Pessoas observadas | 0 | observado no executor local |
| Entrada humana em até 10 minutos | não observada | não comprovada |

O orçamento simulado de entrada ficou entre três e oito minutos, mas esse valor é parâmetro de cenário, não cronometragem humana. Por isso, o critério humano permanece como dívida de validação empírica.

## Alto e extremo

Cinco cenários alto/extremo foram exercitados. Quando faltou controle, houve drift ou conflito, a decisão calculada bloqueou operação, reabriu o risco ou interrompeu integração. O aprendizado continuou apenas em simulador, shadow, sandbox sem dinheiro real ou digital twin. Nenhum resultado desta suíte autoriza produção.

## Déficits anteriores e regra correspondente

- Ideia nova fora do prazo: redirecionar ou trocar item de custo equivalente.
- Tarefa atrasada: cortar escopo ou ativar fallback.
- Alegação sem fonte: rejeitar a alegação.
- Contexto canônico ausente: bloquear integração.
- Responsável distante ou handoff vencido: escalar e orientar reentrada.
- Alto/extremo sem controle externo: bloquear operação.
- Mudança acumulada ou de provedor: reabrir risco.
- Dois integrantes alterando o mesmo contrato: interromper integração até reconciliação.

## Limite da conclusão

A suíte valida coerência estrutural e reprodutibilidade local. Para medir facilidade real, ainda é necessário observar pessoas entrando no repositório, registrar tempo, dúvidas e retrabalho, sem generalizar além da amostra. Para comparar LLMs reais, é necessário executar provedores identificados e guardar entradas, versões, saídas e limitações como evidência separada.

## Como reproduzir

```text
python tools/run_regression.py --output validation/regression-results-P1.06.json
python -m unittest discover -s tests -v
python tools/validate_governance.py repo
```
