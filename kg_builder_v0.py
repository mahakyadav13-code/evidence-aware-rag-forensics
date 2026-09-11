import spacy
import networkx as nx
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")

text = """On Jan 5th, Alice called Bob at 10 PM. Bob then drove to 
Carol's house using his car registered as DL-01-AB-1234. Carol's 
phone pinged near City Mall at 10:30 PM."""

doc = nlp(text)

print("Entities found:")
for ent in doc.ents:
    print(f"  {ent.text} -> {ent.label_}")

# Manually link relations (basic NER doesn't extract relations automatically)
G = nx.DiGraph()
G.add_edge("Alice", "Bob", relation="called")
G.add_edge("Bob", "Carol's house", relation="traveled_to")
G.add_edge("Bob", "Car DL-01-AB-1234", relation="drove_in")
G.add_edge("Carol", "City Mall", relation="located_at")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=2000, font_size=8)
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.savefig("docs/kg_code_generated.png")
plt.show()