# Proposed Workflow

Superseded by the approved workflow: specs/00_Project_Control/workflows/WI-002.md.

## Objective
Centralizar helpers em .softkit/scripts/ e adicionar criação interativa de work items.

## Source Material
softkit-input/changes/inbox/CR-001-script-location-and-interactive-work-item.md;
fonte original vinculada; specs/00_Project_Control/change-impact/CR-001.md.

## Impact Summary
Quatro helpers, orchestrator, protocolo, README e testes. Preservar CLI automatizada
com wrappers mínimos de compatibilidade. Evidências históricas permanecem históricas.

## Recommended Steps
1. softkit-coder: mover implementações, atualizar referências, adicionar wrappers e modo interativo.
2. softkit-qa: testar CLI existente, entrada interativa, entradas inválidas, cancelamento,
   ausência de terminal, caminhos antigos e novos, bootstrap e validação estrutural.

## Skipped Skills
Interrogator e Philosopher: critérios concretos definidos nesta proposta.
Architect: reorganização local sem decisão arquitetural adicional.
Reviewer e DevOps: revisão independente e entrega operacional não requeridas neste ciclo.

## Approval Boundaries
Status: proposed. Aprovação por ciclo inclui mudança do caminho canônico, wrappers
e comportamento interativo descrito em CR-001. Sem nova dependência ou publicação.

## Stop Conditions
Necessidade de quebrar a CLI existente, ampliar o escopo ou adicionar dependência.

## Expected Deliverables
Scripts centralizados, CLI interativa, contratos atualizados, testes e evidências.
O work item será alocado após aprovação. QA pelo mesmo executor será identificado.

## Recommended Approval Mode
cycle.
