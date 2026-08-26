# Team

| Pessoa | Função | Habilidade relevante | Disponibilidade | Autoridade | Área ativa | Suplente |
|---|---|---|---|---|---|---|

Uma pessoa só recebe tarefa após confirmar este perfil e ler o handoff. Integrantes tardios passam por reentrada guiada e confirmação do integrador.

O vínculo entre pessoa e trabalho vive na tarefa, não em um status pessoal. Cada tarefa possui um dono ativo; a transferência segue `docs/work-lifecycle.md`. Ausência, mensagem privada ou handoff apenas oferecido não autorizam outro integrante a assumir.

## Entrada de integrante

Não gere outro PRD. A LLM lê charter, tarefas e handoff e faz perguntas simples:

1. O que você consegue fazer ou revisar com segurança?
2. Quanto tempo do relógio central ainda estará disponível para você?
3. Você prefere produzir, conferir, testar, pesquisar ou revisar visualmente?

Se a resposta for vaga, a LLM apresenta até três tarefas abertas já delimitadas, com exemplo, orçamento e revisor. A pessoa escolhe; o integrador confirma o vínculo. Dizer “quero ajudar no visual”, por exemplo, não cria uma nova frente: a LLM procura o segmento correspondente e oferece uma saída mínima existente.

## Distribuição

- Especialista: contratos, decisões irreversíveis, arquitetura crítica e revisão de risco.
- Intermediário: implementação delimitada, integração assistida e testes de comportamento.
- Iniciante ou auxiliar: extração estruturada, fixtures, checklist, conteúdo, teste guiado e revisão visual.

Esses perfis orientam suporte, não valor ou autoridade. A tarefa determina o que pode ser alterado.

## Identidade de LLM

Cada LLM ativa possui identidade no snapshot da tarefa: fornecedor, modelo, versão quando exposta, fontes de contexto, autonomia, autorização e grupo de independência. Apelidos como “a IA do backend” não bastam. Fornecedores diferentes não provam independência se compartilham modelo, fontes ou incentivo; registre a limitação sem fabricar certeza.
