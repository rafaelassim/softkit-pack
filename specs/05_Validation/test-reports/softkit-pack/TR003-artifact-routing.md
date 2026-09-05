# TR003: Artifact routing and selection

## Scope
CR-002 / WI-003. Work-item and change-request creation with canonical destinations.

## Environment
Python 3.12, POSIX. Same executor /root implemented and validated the change.

## Traceability Matrix
CLI routing and metadata: test_change_request_routing_and_lifecycle_ids and
 test_origin_does_not_change_artifact_type. Arrow selection/cancellation: mocked
curses screen. Numbered fallback: input simulation and existing PTY integration.
Existing compatibility, bootstrap, YAML, cancellation and validation tests retained.

## Commands Executed
`python3 -B -m unittest discover -s tests -v`: 15 passed.

## Results
Change requests preserve proposed authority/inbox status and allocate IDs across
lifecycle folders. Work-item CLI and legacy paths remain compatible. Selection and
cancellation tests passed. Exclusive file creation prevents overwriting a collision.

## Failures and Defects
None remaining in approved scope.

## Coverage Gaps
Arrow behavior tested with a simulated curses screen, not a real full-screen terminal.
PTY integration covers numbered fallback. No Windows terminal or independent review.
Concurrent allocation may fail safely and require retry; no parallel allocator added.

## Conclusion
Required checks passed for the approved cycle.
