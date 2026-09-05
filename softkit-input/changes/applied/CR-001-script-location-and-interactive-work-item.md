---
id: CR-001
document_type: change-request
title: Centralizar scripts e criar work items interativamente
status: applied
priority: medium
submitted: 2026-09-05
authority: normative
supersedes: []
---

# Requested Change
Mover os quatro helpers do orchestrator para .softkit/scripts/ e tornar
create_work_item.py interativo quando chamado sem argumentos.

# Motivation
Facilitar o acesso aos scripts e a criação manual de work items.

# Expected Behavior
Critérios aprovados e implementados em WI-002:
- Scripts executáveis no novo caminho e referências operacionais atualizadas.
- Sem argumentos, em terminal interativo, solicitar título, objetivo, origem e
  prioridade; manter os defaults atuais para campos opcionais.
- Preservar a CLI com argumentos para automação; argumentos incompletos geram erro.
- Sem argumentos e sem terminal, sair com orientação e código não zero, sem aguardar entrada.
- Cancelamento ou EOF não cria work item; título e objetivo não podem ser vazios.
- Preservar IDs estáveis, template completo e status proposed.

# Constraints
Sem dependências novas. Não alterar evidências históricas do WI-001.
Proposta de compatibilidade: wrappers mínimos nos caminhos anteriores delegam aos
scripts canônicos, sem duplicar a implementação.

# Examples or References
Fonte original preservada: softkit-input/changes/inbox/change-request.template.md.

# Known Risks
Referências antigas quebradas; prompts bloqueando automações; criação parcial ao cancelar.
