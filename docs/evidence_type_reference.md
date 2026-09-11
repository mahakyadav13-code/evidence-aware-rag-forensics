# Evidence-Type Reference Sheet

Evidence types this system is designed to support, with their raw data
formats and what they reveal.

| Evidence Type | Raw Data Format | What it Reveals |
|---|---|---|
| Chat/messaging logs | JSON, XML, SQLite DB dumps, plain text exports | Sender, receiver, message content, timestamps |
| Call logs | CSV, CDR files, JSON | Caller, callee, call duration, timestamp |
| File metadata | EXIF (images), filesystem timestamps, PDF/Office metadata | Device used, creation/modification time, sometimes authorship or GPS |
| Network traffic | PCAP files | Source/destination IP, ports, protocol, timestamp |
| Mobile app data | SQLite DBs, plist (iOS), shared_prefs XML (Android) | App-specific cached data, in-app location/message history |
| Location/GPS pings | GPX, JSON, cell-tower logs | Timestamped device coordinates |
| Disk images | Raw (.dd/.img), E01 | Full device snapshot; source for most other evidence types once parsed |
| Browser history | SQLite (Chrome/Firefox history DB), CSV | URLs visited, timestamps, search queries |

## Scope for our synthetic case (Week 5)

We will realistically model 5 of these types, matching our existing
`basic_rag_demo.py` sample documents:

1. Chat/messaging logs
2. Call logs
3. File metadata
4. Network logs
5. Location/GPS pings

Disk images, mobile app data, and browser history are out of scope for
the synthetic dataset (too complex to fake convincingly) but will be
mentioned in the paper as supported evidence types the schema is
designed to extend to.