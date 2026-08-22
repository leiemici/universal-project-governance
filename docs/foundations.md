# Fundamentos da estrutura

Este arquivo explica escolhas de desenho; não faz parte da leitura obrigatória diária.

- **Racionalidade limitada — Herbert Simon:** pessoas decidem com informação, atenção e tempo finitos. Por isso o charter comprime a direção e limita escolhas simultâneas.
- **Erro como propriedade do sistema — James Reason:** falhas atravessam várias defesas frágeis. Por isso há diretiva, contrato, checkpoint, evidência, integração e recuperação, sem depender de uma pessoa perfeita.
- **Restrições, feedback e recuperação — Don Norman:** ações corretas devem ser fáceis de perceber e erros devem aparecer cedo. Por isso tarefas têm exemplos, estados, evidência e fallback.
- **Carga cognitiva e vieses sob pressão — Daniel Kahneman:** urgência favorece atalhos e excesso de confiança. Por isso o relógio, a regra de corte e os não-alvos são explícitos antes da execução.
- **Complexidade de comunicação — Fred Brooks:** mais pessoas e handoffs aumentam coordenação. Por isso segmentos têm contratos, donos e integração frequente.
- **Contexto para agentes — Matt Pocock:** conversa e codebase são sintetizados em PRD; linguagem do domínio e decisões persistem; módulos profundos e fatias verticais reduzem interfaces frágeis. Referência: https://github.com/mattpocock/skills

O objetivo não é remover julgamento humano. É criar memória externa, feedback rápido e limites operacionais para que humanos e LLMs mantenham autonomia sem perder o resultado comum.
