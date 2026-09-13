import json
import networkx as nx
import matplotlib.pyplot as plt

def build_kg(extraction_file):
    with open(extraction_file) as f:
        extractions = json.load(f)
    
    G = nx.DiGraph()
    
    for item in extractions:
        evidence_id = item["evidence_id"]
        # Add entity nodes with type attribute
        for entity in item["entities"]:
            G.add_node(entity["name"], type=entity["type"])
        # Add relation edges, tagged with source evidence_id
        for rel in item["relations"]:
            G.add_edge(rel["subject"], rel["object"], 
                       relation=rel["relation"], 
                       evidence_id=evidence_id)
    
    return G

def visualize_kg(G, output_path):
    pos = nx.spring_layout(G, k=1.5, seed=42)
    plt.figure(figsize=(12, 8))
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=2500, font_size=8, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'relation')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title("Case Knowledge Graph (from LLM extraction)")
    plt.savefig(output_path)
    plt.show()

if __name__ == "__main__":
    G = build_kg("ingestion/extracted_entities.json")
    
    print(f"Total nodes (entities): {G.number_of_nodes()}")
    print(f"Total edges (relations): {G.number_of_edges()}")
    print("\nNodes:", list(G.nodes(data=True)))
    print("\nEdges:", list(G.edges(data=True)))
    
    visualize_kg(G, "docs/full_case_kg.png")