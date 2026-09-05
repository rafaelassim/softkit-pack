# Proposed Workflow

Superseded by specs/00_Project_Control/workflows/WI-003.md.

## Objective
Criar work items e change requests nos destinos corretos e usar seleção interativa.

## Source Material
softkit-input/changes/inbox/CR-002-artifact-routing-and-selection.md e fonte original;
specs/00_Project_Control/change-impact/CR-002.md; templates existentes.

## Impact Summary
Separar tipo de artefato de origem. Dois tipos suportados neste ciclo, com templates
canônicos; preservar CLI atual. Menus por setas/Enter com alternativa numerada.

## Recommended Steps
1. softkit-coder: implementar roteamento, IDs de CR, seleção interativa e documentação.
2. softkit-qa: verificar destinos, schemas, IDs em todas as pastas, CLI antiga e nova,
   menus, fallback, cancelamento e ausência de terminal.

## Skipped Skills
Interrogator: aprovação desta proposta confirma o recorte dos dois tipos.
Philosopher e Architect: sem nova política ou arquitetura significativa.
Reviewer e DevOps: sem exigência de revisão independente ou entrega operacional.

## Approval Boundaries
Proposed. Escopo limitado a work-item e change-request, sem dependência nova.
Preservar significado de --origin-type e comportamento padrão da automação.

## Stop Conditions
Necessidade de outros schemas, nova dependência ou quebra de compatibilidade.

## Expected Deliverables
Script, documentação e testes atualizados; evidências de QA pelo mesmo executor,
explicitamente identificado. Alocar work item somente após aprovação.

## Recommended Approval Mode
cycle.
