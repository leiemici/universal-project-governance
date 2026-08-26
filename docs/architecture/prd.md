# PRD — Universal Project Governance

Status: arquitetura de produto para revisão
Modo: `non-UI`
Origem: síntese do repositório existente, das simulações registradas e do estágio `arch-prd` do NeoCortex

## 1. Visão

Transformar uma conversa inicial sobre qualquer projeto em uma direção compartilhada, verificável e proporcional ao prazo e ao risco, para que pessoas com diferentes níveis de experiência e LLMs de fornecedores distintos trabalhem em partes separadas e ainda convirjam para a mesma entrega.

A estrutura não tenta produzir pessoas ou agentes sem falhas. Ela reduz o espaço em que ambiguidades, excesso de confiança, perfeccionismo, contexto desatualizado e integração tardia conseguem desviar o resultado.

## 2. Discover — evidência e problema observado

### 2.1 Problema

Equipes perdem alinhamento quando objetivo, prazo, destino, autoridade, dependências, evidências e estado atual ficam espalhados entre conversas, computadores, branches e modelos. Os sintomas recorrentes são:

- cada participante entende uma versão diferente do projeto;
- especialistas ampliam a solução além do tempo disponível;
- iniciantes recebem tarefas vagas ou ficam sem uma contribuição segura;
- pesquisa, interface e núcleo técnico avançam sem contrato comum;
- decisões e handoffs não preservam revisão, validade ou responsabilidade;
- uma LLM interpreta texto convincente como aprovação ou evidência;
- controles de alto risco existem no papel, mas não são carregados ou aplicados.

### 2.2 Evidência interna

- `docs/simulation-report-10-projects.md` encontrou boa contenção de rumo em projetos baixos e médios, mas fragilidade crescente em múltiplas LLMs e alto/extremo risco.
- `docs/regression-report-10-projects.md` registrou zero correções integralmente comprovadas, onze parciais e seis déficits abertos.
- A regressão também demonstrou que `RUNBOOK.md` e `profiles/high-extreme.md` não faziam parte de toda leitura aplicável.

### 2.3 Evidência externa usada como limite de desenho

- O método `to-prd` de Matt Pocock sintetiza conversa e codebase, respeita linguagem de domínio e procura módulos profundos com interfaces pequenas e testáveis: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-prd/SKILL.md
- A configuração de domínio do mesmo projeto favorece um contexto canônico pequeno e ADRs para decisões difíceis de reverter: https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md
- O NIST AI RMF exige papéis diferenciados para configurações humano-IA, governança contínua, rastreamento e supervisão proporcional ao risco: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- O perfil de IA generativa do NIST destaca governança, testes antes da implantação, proveniência e divulgação de incidentes: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- A pesquisa DORA associa documentação de qualidade e trabalho em pequenos lotes ao desempenho de entrega: https://dora.dev/research/core/assets/dora-core-v2.1.0-detail.pdf

Essas fontes orientam princípios; não provam que este template produz desempenho real. Essa prova depende dos testes definidos neste documento.

## 3. Define — produto, atores e limites

### 3.1 Declaração do produto

Uma base clonável que conduz o proprietário da ideia da conversa inicial até uma memória compartilhada no GitHub, divide a entrega em ramificações coerentes e permite que humanos e LLMs entrem, executem, revisem, integrem e transfiram trabalho sem reconstruir o contexto em conversas privadas.

### 3.2 Atores diretos

- **Proprietário:** confirma alvo, prazo, destino, aceite, risco e cortes.
- **Integrador:** protege contrato, revisão comum e versão entregável.
- **Responsável técnico:** decide meios críticos dentro da autoridade registrada.
- **Especialista:** executa ou revisa decisões que exigem competência específica.
- **Intermediário:** implementa fatias delimitadas e integra com apoio.
- **Iniciante, extrator ou revisor:** produz artefatos pequenos com exemplo, limite e revisor.
- **LLM:** lê o mesmo snapshot, classifica entradas, propõe ações reversíveis e respeita gates humanos.

Usuários finais dos produtos criados a partir do template e stakeholders externos não são usuários diretos deste repositório.

### 3.3 Superfícies

- documentos Markdown versionados;
- Git, branches, commits e pull requests;
- issue tracker opcional;
- chats e agentes que recebem o repositório como contexto.

Não há interface gráfica, banco de dados ou API próprios.

### 3.4 Resultado principal

Um integrante novo consegue descobrir, sem conversa privada, o que está sendo construído, quando precisa terminar, onde será entregue, como provar que funciona, qual trabalho pode assumir e qual é o próximo ponto de integração.

### 3.5 Não objetivos

- substituir julgamento, responsabilidade ou aprovação humana;
- garantir segurança operacional apenas com documentos;
- impor épicos e stories a projetos curtos;
- gerar wrappers para todas as ferramentas de IA;
- criar documentação específica para UI, banco ou API inexistentes;
- transformar toda sugestão em regra obrigatória;
- prometer universalidade regulatória para saúde, finanças ou controle físico.

## 4. Develop — modelo operacional

### 4.1 Arquitetura em camadas

#### Núcleo universal

O menor conjunto necessário para orientar qualquer projeto:

1. PRD — contexto e decisões de produto.
2. Charter — diretiva operacional confirmada.
3. Contexto e steering — vocabulário e manutenção de rumo.
4. Plano e tarefas — decomposição proporcional e propriedade.
5. Handoff e decisões — continuidade e alterações autorizadas.

#### Overlays condicionais

Carregados somente quando o charter ativar a condição:

- múltiplas LLMs;
- dependências externas;
- dados pessoais ou sensíveis;
- risco alto ou extremo;
- projeto solo sem substituto;
- duração longa e múltiplos fluxos dependentes.

#### Anexos de domínio

Saúde, finanças e sistemas físicos exigem anexos próprios. O núcleo pode identificar e bloquear risco, mas não substitui controles técnicos, jurídicos ou profissionais do domínio.

### 4.2 Encadeamento canônico

```text
conversa
  → PRD aprovado
  → charter confirmado
  → snapshot de contexto
  → plano proporcional
  → tarefas por palavra-chave
  → branches e evidências
  → revisão e integração
  → aceite no destino
  → handoff ou encerramento
```

Cada transição registra uma revisão Git ou decisão. Nenhuma camada posterior redefine silenciosamente a anterior.

### 4.3 Snapshot de contexto

Antes de assumir uma tarefa, pessoa ou LLM registra:

- commit-base;
- versão do charter e decisões aplicáveis;
- versão do contrato consumido;
- provedor, modelo e autonomia quando houver LLM;
- dados permitidos e proibidos;
- horário e validade do snapshot.

Mudança em charter, decisão, contrato ou risco invalida o snapshot afetado e exige releitura seletiva.

### 4.4 Ramificações de trabalho

Toda tarefa possui exatamente uma palavra-chave primária, um dono ativo, uma branch exclusiva, arquivos permitidos, saída mínima, consumidor seguinte e revisor. Uma palavra-chave representa resultado, não cargo.

Trabalho concorrente na mesma área crítica exige uma decisão prévia de integração. Autoridade vem do charter e da tarefa, não da senioridade ou do modelo utilizado.

### 4.5 Handoff verificável

Uma transferência só é válida quando registra:

- tarefa e revisão exata;
- contrato e evidências aplicáveis;
- estado real e próximo passo;
- pendências e riscos;
- emissor, receptor e aceite do receptor;
- expiração e escalonamento se não for aceita.

Sem aceite, a tarefa continua pertencendo ao emissor ou retorna ao integrador.

### 4.6 Evidência

Todo resultado recebe uma classe:

- `simulado` — comportamento exercitado sem ambiente real;
- `estimado` — inferência ainda não executada;
- `executado` — ocorreu em ambiente e revisão identificados;
- `validado` — execução reproduzida e aceita pelo revisor autorizado.

Saídas baseadas em dados também registram fonte, coleta, cobertura, idade, transformação e limitações.

### 4.7 Tempo e perfeccionismo

O relógio pertence ao projeto. Cada tarefa inclui leitura, execução, revisão, integração e handoff. Quando o checkpoint estoura, as opções são integrar parte útil, simplificar, ativar fallback, transferir ou cortar.

Para projetos de até quatro horas:

- planejamento inicial limitado a 15 minutos;
- máximo de seis tarefas;
- primeiro fluxo demonstrável até 25% do prazo;
- extras congelados antes da integração final;
- nenhuma ferramenta nova entra se não substituir trabalho de custo equivalente.

### 4.8 Alto e extremo risco

Documentação define obrigação, mas não prova enforcement. Projetos altos/extremos devem demonstrar controles externos adequados, como identidade e acesso, gateway, segregação de funções, sandbox, canário, interlock independente, limites e mecanismo de parada.

Quando o destino original não é seguro, a equipe pode propor a escada:

`produção → canário ou shadow → sandbox → simulador → pacote de evidência`

O rebaixamento altera o destino e exige decisão humana registrada.

## 5. Requisitos funcionais

1. Sintetizar conversa e evidência em PRD sem repetir perguntas respondidas.
2. Gerar charter curto com alvo, prazo absoluto, destino, aceite, não-alvos e corte.
3. Selecionar de duas a seis palavras-chave e vincular cada tarefa a uma delas.
4. Classificar prazo, risco, dados, dependências e governança com confirmação humana.
5. Gerar planejamento proporcional à duração e complexidade de coordenação.
6. Guiar entrada de integrantes com tarefas existentes, sem criar novo PRD.
7. Registrar identidade, contexto e autonomia de cada LLM envolvida.
8. Preservar decisões por substituição, nunca por reescrita silenciosa.
9. Exigir evidência vinculada à revisão entregue.
10. Invalidar contexto e reabrir risco quando uma mudança atingir os campos canônicos.
11. Transferir trabalho somente com handoff aceito e dentro da validade.
12. Carregar overlays e anexos apenas quando a condição correspondente estiver ativa.

## 6. Critérios de aceite

- Um novo integrante localiza alvo, prazo, destino, aceite, tarefa própria e próximo passo em até 10 minutos, sem conversa privada.
- 100% das tarefas ativas contêm palavra-chave, dono, branch, arquivos permitidos, aceite, evidência, checkpoint, revisor e próximo consumidor.
- 100% dos trabalhos de LLM registram provedor, modelo ou versão disponível, snapshot, dados permitidos e autonomia.
- Mudança em alvo, prazo, destino, aceite, risco ou dado não avança sem decisão humana registrada.
- Projetos rápidos respeitam 15 minutos de planejamento, seis tarefas e fluxo demonstrável até 25% do prazo.
- Handoff vencido ou não aceito produz escalonamento visível, não transferência presumida.
- Saída baseada em dados não pode ser validada sem proveniência e idade.
- Risco alto/extremo carrega perfil, runbook e anexo de domínio aplicável antes da execução.
- Os dez cenários da matriz de regressão preservam direção e bloqueiam falsa evidência.
- O repositório não exige artefatos de UI, banco ou API quando essas superfícies não existem.

## 7. Estratégia de validação

### 7.1 Testes estruturais

- verificador de links e arquivos obrigatórios;
- lint de campos mínimos em charter, tarefa, decisão e handoff;
- teste de carregamento condicional dos overlays;
- verificação de que evidência e entrega apontam para a mesma revisão;
- detecção de snapshot vencido e handoff expirado.

### 7.2 Simulações comportamentais

Reexecutar os dez projetos existentes com LLM simples, intermediária e forte, além de variações humanas: entrada vaga, fonte imprecisa, atraso, conflito, escopo tardio, falsa evidência, drift cumulativo, dependência indisponível e troca de responsável.

### 7.3 Validação humana

Executar pelo menos um projeto solo, um hackathon curto e um projeto de dias com equipe mista. Medir tempo de entrada, retrabalho, divergências de interpretação, tarefas reabertas e tempo de integração.

## 8. Métricas

- tempo para um novo integrante iniciar contribuição segura;
- percentual de tarefas com contexto completo;
- quantidade de desvios redirecionados antes de execução;
- tempo gasto em coordenação versus orçamento;
- handoffs vencidos ou rejeitados;
- evidências inválidas detectadas antes da integração;
- frequência de cortes e fallbacks acionados no checkpoint;
- divergências entre LLMs sobre classe, autoridade ou estado;
- regressões por cenário e nível de risco.

Métricas servem para ajustar a estrutura, não para ranquear pessoas.

## 9. Decisões pendentes para a arquitetura

- formato do manifesto de contexto sem amarrar o template a uma linguagem;
- mecanismo mínimo de lint estrutural portável;
- taxonomia dos overlays e seus gatilhos;
- formato dos anexos de saúde, finanças e sistemas físicos;
- política de expiração proporcional para snapshot, evidência e handoff;
- separação entre regra documental e prova externa de enforcement.

## 10. Definição de entrega desta fase

O PRD está pronto quando arquitetura e épico conseguirem derivar componentes, dependências, fitness functions e tarefas sem reabrir o problema ou incluir estágios incompatíveis com o modo non-UI.
