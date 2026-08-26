# Validação portátil

O verificador transforma invariantes estruturais em mensagens acionáveis sem afirmar verdade externa. Ele usa somente a biblioteca padrão do Python 3 e não depende do runtime, stack ou gerenciador de pacotes do projeto derivado.

## Comandos

```text
python tools/validate_governance.py repo
python tools/validate_governance.py evidence evidence/EV-exemplo.json
python tools/validate_governance.py route validation/fixtures/routing/valid.json
python -m unittest discover -s tests -v
```

`repo` verifica caminhos canônicos, leituras de overlays, contratos JSON e evidências publicadas. `evidence` valida presença, proveniência e força da conclusão. `route` valida fatos, calcula overlays aplicáveis e compara o resultado esperado quando informado.

## Semântica das classes

- `simulado`: fixture ou ensaio fora do destino real; nunca satisfaz aceite operacional.
- `estimado`: inferência não executada; nunca satisfaz aceite.
- `executado`: ocorreu em ambiente e commit identificados, mas ainda não possui revisão reproduzível aceita.
- `validado`: execução reproduzível, revisão aceita e entrega apontam para o mesmo commit.

Fixture marcada como `executado` ou `validado` falha. Evidência diferente da revisão ou entrega falha. Exceções humanas continuam em `docs/decisions.md`; o registro não deve mentir para contornar o verificador.

## Proveniência mínima

Toda evidência registra fonte, coleta, cobertura, idade na validação, transformações e limitações. Campo presente não prova exatidão: o revisor ainda precisa reproduzir o caso e avaliar se a fonte é adequada.

## Portabilidade

`governance.validation.json` define somente caminhos e globs da instância. `docs/evidence-record.schema.json` é o contrato interoperável; `tools/validate_governance.py` implementa o subconjunto operacional com mensagens estáveis. Projetos sem Python podem implementar o mesmo esquema em outra linguagem sem alterar a semântica.

Referências: [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) e [Python Standard Library](https://docs.python.org/3/library/).
