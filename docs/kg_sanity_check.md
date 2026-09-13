# KG Sanity Check — Week 8 Day 5

## Matches with ground truth
- John—Mike communication captured (call: EVID-0001, message: EVID-0004) ✓
- File creation on John's laptop correctly linked via BELONGS_TO ✓
- Mike's phone pinging near a warehouse location captured (EVID-0005) ✓

## Discrepancies found

**1. Entity resolution gap: "warehouse" vs "old warehouse"**
The message (EVID-0004) mentions "warehouse" while the location ping 
(EVID-0005) mentions "old warehouse". The LLM extracted these as two 
separate nodes instead of resolving them to the same location. Ground 
truth requires these be treated as one entity to correctly conclude 
"Mike physically went to the meeting location after messaging John."

**2. Missing link: IP address not connected to John**
Ground truth states "the file creation and upload are linked by the 
same device/IP (John)". Our graph has:
- John's laptop → John (BELONGS_TO)
- 192.168.1.5 → external server (uploaded to)
But there is no edge connecting 192.168.1.5 to John or John's laptop. 
The LLM extracted each evidence item's relations in isolation and did 
not infer that the IP address belongs to John, since that link isn't 
stated explicitly in the evidence text — it requires cross-evidence 
reasoning.

**3. Timestamps dropped during extraction**
The original evidence has timestamps (22:30, 22:35, etc.), but the 
extraction prompt did not ask the LLM to preserve them, so the graph 
has no temporal ordering. Without this, the "before the file activity" 
ordering from ground truth cannot be verified from the graph alone.

## Notes for future weeks
- Week 9-10 (correlation engine): entity resolution and cross-evidence 
  linking (like IP-to-person) need dedicated logic, not just per-item 
  LLM extraction — this is the core "evidence-aware" contribution.
- Timestamps must be carried through into the KG edges for timeline 
  reconstruction (Week 10 Day 4).