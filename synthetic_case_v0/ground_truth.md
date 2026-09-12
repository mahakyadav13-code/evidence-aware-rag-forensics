# Ground Truth — Synthetic Case v0

## Timeline
1. 22:30 — John calls Mike (14 min)
2. 22:35 — Mike messages John to meet at the warehouse
3. 22:52 — John creates 'transfer.zip' on his laptop
4. 23:05 — File uploaded externally from John's IP
5. 23:15 — Mike's phone pings near the warehouse

## Correct correlations a system should find
- John and Mike communicated twice (call + chat) before the file activity
- The file creation and upload are linked by the same device/IP (John)
- Mike physically went to the meeting location after messaging John

## Expected conclusion
John created and exfiltrated the file; Mike was the intended recipient/ 
accomplice based on the coordinated meeting, not an unrelated bystander.