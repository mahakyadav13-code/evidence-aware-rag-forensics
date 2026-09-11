Multi-Hop Reasoning Example
Question
“Who did the suspect communicate with before the incident, and where was that person located at the time?”
Why Single Retrieval Is Insufficient
Answering this question requires information from multiple evidence sources. The required information is not available in a single document; instead, each piece of information depends on the result obtained from the previous step. Therefore, a conventional single-step similarity search is insufficient because it retrieves relevant text but does not perform the dependent reasoning and evidence linking required to answer the complete question.
Required Retrieval and Reasoning Steps
Step 1: Identify the Suspect and Incident Time

* Source: Incident report / case timeline
* Identify the suspect and determine the exact timestamp of the incident.

Step 2: Identify Prior Communication

* Source: Chat logs / call records
* Retrieve communications involving the suspect that occurred before the identified incident time.
* Determine who the suspect communicated with and the corresponding communication timestamp.

Step 3: Determine the Other Person’s Location

* Source: GPS records / network logs / cell tower data
* Use the person identified in Step 2 and the communication timestamp to retrieve their location around that specific time.

Reasoning Chain
Incident → Suspect → Prior Communication → Other Person → Communication Time → Location
The final answer is obtained by connecting evidence across multiple sources through a sequence of dependent retrieval steps. This demonstrates why multi-hop reasoning is essential for complex investigation queries where the answer cannot be derived from a single retrieval operation.