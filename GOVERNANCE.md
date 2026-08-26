# Governance

## Papéis mínimos
- Integrador: protege escopo, contrato e versão executável.
- Responsável técnico: valida regras, dados e integrações da área crítica.
- Revisores: executam checklists visuais, conteúdo, dados ou fluxo.

## Decisões
Uma decisão deve registrar contexto, escolha, responsável e consequência em `docs/decisions.md`.

## Colaboração
Iniciantes recebem tarefas delimitadas com artefato esperado, exemplo de pronto, tempo limite e revisor. LLMs propõem; uma pessoa aprova decisões de produto, risco e publicação.

## Autonomia conjunta

- O proprietário confirma a diretiva e o relógio central.
- A LLM mantém o compasso, segmenta entradas, calcula aderência e recomenda corte ou fallback.
- O dono do segmento decide meios técnicos reversíveis dentro do contrato aprovado.
- O integrador aceita apenas saídas que preservem contrato, evidência e destino.
- Um iniciante pode extrair, conferir, testar ou revisar visualmente sem precisar formular toda a arquitetura; a tarefa fornece contexto, exemplo e limite.
- Senioridade não concede poder para ampliar escopo. Autoridade vem do charter e da tarefa.

Quando houver erro, registre primeiro qual defesa estrutural falhou: diretiva, segmentação, contrato, checkpoint, evidência ou integração. Evite transformar a análise em julgamento da pessoa.

## Múltiplas LLMs e segurança
Use apenas provedores e modelos aprovados em `docs/decisions.md`. Dados pessoais são bloqueados por padrão; qualquer exceção exige minimização e aprovação específica. Nunca transfira arquivos, memória ou logs entre LLMs sem registrar origem, destino e finalidade. Segredos e dados pessoais não entram em prompts, fixtures ou logs.

Código ou configuração gerada por LLM exige revisão humana do diff, dependências/licenças e testes proporcionais ao risco. Antes de commit, merge ou publicação, execute as verificações de segredos e dados proibidos definidas pelo projeto. Conflitos em código, contrato ou configuração exigem revisão do dono afetado e repetição das evidências.

Uma área crítica tem um único dono ativo. Trabalho concorrente nessa área exige decisão de integração aprovada antes do merge. Decisões não são apagadas ou reescritas: são substituídas por um novo ID.

## Propriedade, revisão e continuidade

O ciclo canônico está em `docs/work-lifecycle.md`. A branch isola trabalho, mas não concede autoridade fora da tarefa. Propriedade só muda com handoff aceito; oferta, ausência ou expiração não transferem responsabilidade automaticamente. O integrador resolve sobreposição em área crítica e decide reassumir, substituir ou cortar handoff expirado.

Uma saída só está pronta quando evidência e revisão citam o mesmo commit. A integração cita esse mesmo commit ou uma exceção humana registrada; qualquer alteração material reabre revisão e evidência.

O gate estrutural mínimo é `python tools/validate_governance.py repo`, documentado em `docs/validation.md`. Ele verifica presença, referências, overlays e registros de evidência; não substitui revisão profissional nem prova enforcement externo.

Alto/extremo acrescenta `docs/risk-boundary.md`. Autor, revisor e aprovador são distintos. Rebaixamento de destino, reabertura por drift e qualquer permissão de simulador/pacote de evidência exigem decisão humana registrada; destino operacional exige enforcement e evidência externos vigentes.
