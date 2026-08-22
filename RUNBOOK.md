# Runbook de incidente e recuperação

Ao detectar vazamento, ação indevida, dependência comprometida ou deploy incorreto:

1. Pare processamento, integração e publicação afetados.
2. Contenha acesso e revogue/rotacione credenciais quando aplicável.
3. Preserve evidência sanitizada sem ampliar a exposição.
4. Notifique responsável e suplente; alto/extremo exige decisão independente.
5. Execute rollback ou roll-forward previamente testado e valide o mesmo artefato/revisão.
6. Reconcilie dados/efeitos, registre decisão e só retome após aprovação.

Ações físicas ou econômicas irreversíveis são proibidas por padrão; exigem simulação, limites, confirmação por ação e mecanismo de parada.
