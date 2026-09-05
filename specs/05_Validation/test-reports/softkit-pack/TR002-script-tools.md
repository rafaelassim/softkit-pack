# TR002: Centralized scripts and interactive work items

## Scope
CR-001 / WI-002: canonical helper location, compatibility and interactive creation.

## Environment
Python 3.12, PyYAML, POSIX pseudo-terminal. Executor /root also implemented the change;
this is same-executor validation, not independent review.

## Traceability Matrix
- Six existing regressions: bootstrap, structural validation, work-item allocation.
- Five added tests: four old entry points, no-terminal/incomplete/blank CLI,
  interactive terminal with invalid inputs and defaults, EOF/interrupt cancellation,
  literal backslashes in YAML output.

## Commands Executed
- `python3 -B -m unittest discover -s tests -v`: 11 passed.
- `python3 .softkit/scripts/validate_softkit.py --mode project`: passed.
- `git diff --check`: passed.

## Results
New canonical scripts and legacy wrappers work. Interactive creation keeps proposed
status and stable IDs; invalid input is retried. EOF/interrupt cancels before writes.
Non-terminal and incomplete CLI invocations exit without prompting.

## Failures and Defects
None remaining in the approved scope.

## Coverage Gaps
PTY validation is POSIX-specific. No live Windows terminal test or independent review.

## Conclusion
Required validation passed; CR-001 is applied.
