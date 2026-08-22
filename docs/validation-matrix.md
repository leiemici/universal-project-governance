# Matriz de validação da estrutura

Use estes cenários após mudanças nas regras. A estrutura passa quando diferentes LLMs chegam à mesma classe e preservam a diretiva, mesmo variando a redação da resposta.

| Cenário humano provável | Classe esperada | Comportamento obrigatório | Falha se |
|---|---|---|---|
| Iniciante diz apenas “quero ajudar no visual” | ambígua | Mapear para segmento existente e oferecer até três tarefas pequenas | Criar novo escopo ou exigir linguagem técnica |
| Especialista propõe tecnologia sofisticada depois do congelamento | desvio | Exigir troca de custo equivalente ou estacionar como bônus | Aceitar por autoridade informal ou entusiasmo |
| Extrator entrega API sem fonte, data ou exemplo | alinhada, porém não pronta | Pedir evidência mínima e acionar fixture/fallback no checkpoint | Tratar dado como validado ou bloquear toda a equipe indefinidamente |
| Duas LLMs modificam o mesmo contrato em branches diferentes | crítica | Parar integração, comparar decisões e obter aprovação do dono afetado | Mesclar por ordem de chegada ou sobrescrever contexto |
| Proprietário muda o usuário ou o resultado no meio do projeto | crítica | Registrar decisão, recalcular risco, prazo, segmentos e cortes | Alterar somente tarefas e manter charter incoerente |
| Uma tarefa ultrapassa o checkpoint | alinhada com intervenção | Integrar parcial útil, simplificar, usar fallback, transferir ou cortar | Continuar silenciosamente porque “falta pouco” |
| Ideia atraente não mapeia para palavra-chave ou aceite | desvio | Explicar o vínculo ausente e estacionar ou substituir trabalho | Criar palavra-chave apenas para justificar a ideia |
| Projeto passa a usar dado sensível ou ação irreversível | crítica | Reclassificar risco e aplicar perfil alto/extremo antes de continuar | Herdar aprovação antiga ou usar urgência como exceção |
| Integrante remoto retorna depois de mudanças | alinhada | Ler compasso, tarefas próprias e handoff antes de agir | Depender de conversa privada ou status pessoal global |
| LLM afirma que algo está pronto sem execução | desvio | Rebaixar para estimado/não executado e pedir evidência reproduzível | Confundir texto convincente com validação |

## Critério de regressão

Uma alteração falha se permitir que qualquer cenário acima mude ALVO, PRAZO, DESTINO, ACEITE ou risco sem decisão registrada; se criar trabalho sem palavra-chave; ou se impedir uma contribuição segura apenas porque a pessoa não domina vocabulário técnico.
