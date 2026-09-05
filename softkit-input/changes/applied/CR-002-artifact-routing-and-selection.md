---
id: CR-002
document_type: change-request
title: Destinos por tipo de artefato e seleção interativa
status: applied
priority: medium
submitted: 2026-09-05
authority: normative
supersedes: []
---

# Requested Change
Gerar itens no diretório correspondente ao tipo de requisição e preferir seleção
a digitação livre quando as opções forem conhecidas.

# Motivation
Evitar confusão entre work items e change requests e facilitar o modo interativo.

# Expected Behavior
Aprovada pelo usuário e implementada em WI-003:
- Selecionar o tipo de artefato: work-item ou change-request.
- Work item: specs/00_Project_Control/work-items/WI-NNN.yaml, template de work item.
- Change request: softkit-input/changes/inbox/CR-NNN.md, template de change request.
- Preservar origin.type como metadado do work item; defect, roadmap e user-request
  continuam sendo origens, sem novos diretórios ou schemas presumidos.
- Seleção por setas e Enter para tipo, origem e prioridade em terminais compatíveis;
  menu numerado como alternativa em terminais sem suporte. Texto livre só para
  campos descritivos. Sem biblioteca externa nova.
- Preservar CLI existente; adicionar seleção explícita de artefato na automação,
  mantendo work-item como padrão. IDs estáveis sem colisões; CR considera todas
  as pastas de ciclo de vida. Cancelamento não gera arquivos.

# Constraints
A expressão “demais” não identifica outros artefatos. Este ciclo propõe somente os
dois tipos com templates existentes. Criar arquivo proposto não significa aprová-lo.

# Examples or References
Fonte original preservada: softkit-input/changes/inbox/change-request.template.md.

# Known Risks
Confundir origem com tipo; reutilizar ID de CR já aplicada; incompatibilidade de
terminal; regressão na CLI automatizada.
