# Proposed Workflow

Superseded by specs/00_Project_Control/workflows/WI-004.md.

## Objective
Instalar e inicializar SoftKit em um diretório de destino, criando-o se necessário.

## Source Material
softkit-input/changes/inbox/CR-003.md;
specs/00_Project_Control/change-impact/CR-003.md;
bootstrap_softkit.py, README, protocolo e templates.

## Impact Summary
Bootstrap passa a instalar arquivos do pacote e gerar controle próprio no destino.
Diretório posicional ou --root identifica destino exato; pacote vem da localização
do script. Preservar arquivos existentes e compatibilidade da inicialização local.

## Recommended Steps
1. softkit-coder: implementar instalação e preflight de conflitos, atualizar
   README e contratos de bootstrap, preservar wrapper e CLI existentes.
2. softkit-qa: testar cenários da análise de impacto em diretórios temporários e
   executar validação do pacote/projeto instalado e regressões existentes.

## Skipped Skills
Interrogator: comportamento e limites definidos nesta proposta.
Philosopher e Architect: sem política ou arquitetura adicional necessária.
DevOps: instalação local e documentação cobertas pelo coder, sem release/deploy.
Reviewer: revisão independente não exigida; QA do mesmo executor será identificada.

## Approval Boundaries
Proposed. Instalação de agentes/ferramentas e inicialização por templates, sem
sobrescrita de conflitos, dependências novas, publicação ou cópia do histórico.
Testes em diretórios temporários; nenhum projeto externo real escolhido nesta etapa.

## Stop Conditions
Necessidade de sobrescrever customizações, migrar estado ou ampliar dependências.

## Expected Deliverables
Bootstrap instalador, instruções atualizadas, testes e evidências. Work item será
alocado após aprovação. Exemplo previsto:
python3 .softkit/scripts/bootstrap_softkit.py /caminho/novo-projeto --project-name "Novo projeto"

## Recommended Approval Mode
cycle.
