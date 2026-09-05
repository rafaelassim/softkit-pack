# WI-003 Implementation

## Scope Implemented
Added --artifact-type with work-item default and change-request mode. Added standard-
library curses selection with numbered fallback, canonical CR template rendering,
IDs across change folders, exclusive output creation and origin/type separation.

## Files Changed
.softkit/scripts/create_work_item.py, README.md, orchestrator SKILL.md,
tests/test_softkit_helpers.py and cycle control artifacts.

## Requirements and Decisions Addressed
CR-002 and workflows/WI-003.md.

## Commands Executed
See specs/05_Validation/test-reports/softkit-pack/TR003-artifact-routing.md.

## Results
15 regression tests passed.

## Known Limitations
Same-executor validation; arrows tested using a simulated curses screen.

## Follow-up Work
None within the approved scope.
