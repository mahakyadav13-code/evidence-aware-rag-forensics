# Ground Truth — Synthetic Case v2 (Contradictory)

## Deliberate contradiction
Alex's phone pings place him at two different locations (Downtown Cafe 
and Riverside Warehouse) at the identical timestamp 2026-04-01T20:00:00.
This is intentionally injected to test the contradiction-detection module.

## Expected system behavior
The contradiction_detector.py module should flag EVID-C001 vs EVID-C002 
as a "location_conflict" — same entity (PERSON-Alex), same timestamp, 
different content.

## Other evidence
Sam's chat message (confidence 0.6) and file edit (confidence 0.3) are 
low-reliability, testing whether the confidence calibration module 
correctly produces a "Medium" or "Low" label when cited.