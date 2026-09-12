# Knowledge Graph Schema Specification — Week 6 Day 3

## Node types
- **Person**: an individual referenced in evidence (e.g. PERSON-John)
- **Device**: a phone, laptop, or other hardware (e.g. DEVICE-JohnLaptop)
- **IP**: a network address (e.g. IP-192.168.1.5)
- **Location**: a physical place referenced in evidence (e.g. LOCATION-Warehouse)
- **Event**: an evidence item itself (a call, file creation, upload, ping) — 
  carries the evidence_id, timestamp, and source_type as attributes

## Edge types
| Edge | From → To | Meaning |
|---|---|---|
| COMMUNICATED_WITH | Person → Person | Call/chat contact occurred |
| OWNS | Person → Device | Device ownership/association |
| USED | Person/Device → IP | Network activity attribution |
| LOCATED_AT | Person/Device → Location | Physical presence evidence |
| PARTICIPATED_IN | Person/Device → Event | Links an entity to a specific evidence event |
| FOLLOWED_BY | Event → Event | Temporal ordering between events |

## Example (from synthetic_case_v0)
PERSON-John --COMMUNICATED_WITH--> PERSON-Mike
PERSON-John --OWNS--> DEVICE-JohnLaptop
DEVICE-JohnLaptop --PARTICIPATED_IN--> EVID-0002
PERSON-John --USED--> IP-192.168.1.5
EVID-0002 --FOLLOWED_BY--> EVID-0003
PERSON-Mike --LOCATED_AT--> LOCATION-Warehouse

## Why this matters
This schema is what the correlation engine (Week 8) will actually build 
from extracted entities/relations, and what the evidence-aware retriever 
(Week 9) will traverse for graph-guided expansion — e.g. "find all events 
connected to PERSON-Mike within 2 hops."