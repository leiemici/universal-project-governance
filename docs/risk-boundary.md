# Limite alto/extremo

Este contrato **não autoriza operação**. Ele só demonstra que o pacote documental está completo o bastante para uma pessoa competente avaliar uma decisão. Produção, canário/shadow e sandbox permanecem bloqueados sem controle externo verificado no sistema que realmente aplica o limite.

## Escada de destino

```text
produção → canário/shadow → sandbox → simulador → pacote-de-evidência
```

Descer a escada é permitido apenas por decisão humana registrada; não é aprovação automática do novo destino. Sem enforcement externo, somente `simulador` ou `pacote-de-evidência` podem avançar, ainda com aprovador e limites documentados.

## Gate

Um registro em `risk/*.json` segue `docs/risk-control-record.schema.json` e precisa provar:

1. `profiles/high-extreme.md`, `RUNBOOK.md` e anexo do domínio aplicável;
2. autor, revisor e aprovador distintos, com competência do aprovador;
3. drift cumulativo comparado a limiar objetivo e risco reaberto quando excedido;
4. controles externos com sistema aplicador, evidência externa, revisão e validade;
5. reatestado do provedor quando um controle depende dele;
6. estado seguro, parada, rollback e reconciliação;
7. decisão humana para destino e para qualquer rebaixamento.

Texto, checklist, prompt, Markdown, branch ou aprovação de LLM nunca são `enforcement_system`. O verificador aceita evidência externa somente por referência `external://...`; segredos e dados pessoais não entram no registro.

## Drift e reatestado

Cada release soma mudança na unidade definida pelo projeto: requisitos, regras, permissões, esquema, dependências ou superfície afetada. Ao atingir o limiar, `threshold_exceeded=true` e `risk_reopened=true`; aprovação anterior perde validade até reavaliação. Controle ligado a provedor exige atestado vigente e evidência externa do mesmo provedor.

## Anexos

- clínico: população, uso pretendido, dano, supervisão profissional e contestação;
- financeiro: fluxo de valor, autorização, idempotência, reconciliação e compensação;
- físico: envelope operacional, interlock, parada independente, estado seguro e recommissioning.

Os esqueletos em `domain-annexes/` começam como `template-not-approved`. Preencher o arquivo não altera esse status; um aprovador competente registra a aprovação separadamente.

Referências de orientação: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST SP 800-37 Rev. 2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) e [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final). Essas referências não certificam o projeto.
