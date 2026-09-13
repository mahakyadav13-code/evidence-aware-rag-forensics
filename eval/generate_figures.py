import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import csv
import matplotlib.pyplot as plt

def plot_baseline_comparison():
    cases, hybrid_pct, naive_pct = [], [], []
    with open("eval/results.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    case_names = sorted(set(r["case"] for r in rows))
    for case in case_names:
        h = next(r for r in rows if r["case"] == case and r["system"] == "hybrid")
        n = next(r for r in rows if r["case"] == case and r["system"] == "naive_baseline")
        cases.append(case)
        hybrid_pct.append(float(h["coverage_pct"]))
        naive_pct.append(float(n["coverage_pct"]))
    
    x = range(len(cases))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar([i - width/2 for i in x], hybrid_pct, width, label="Hybrid (ours)", color="#2E7D32")
    ax.bar([i + width/2 for i in x], naive_pct, width, label="Naive Baseline", color="#C62828")
    ax.set_ylabel("Evidence Coverage (%)")
    ax.set_title("Evidence Coverage: Hybrid vs Naive Baseline")
    ax.set_xticks(list(x))
    ax.set_xticklabels(cases)
    ax.set_ylim(0, 110)
    ax.legend()
    plt.tight_layout()
    plt.savefig("docs/figure1_baseline_comparison.png")
    plt.close()
    print("Saved figure1_baseline_comparison.png")

def plot_ablation():
    with open("eval/ablation_results.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    configs = [r["config"] for r in rows]
    pcts = [float(r["pct"]) for r in rows]
    
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#2E7D32", "#F57C00", "#F57C00"]
    ax.bar(configs, pcts, color=colors)
    ax.set_ylabel("Evidence Coverage (%)")
    ax.set_title("Ablation Study: Component Contribution")
    ax.set_ylim(0, 110)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig("docs/figure2_ablation.png")
    plt.close()
    print("Saved figure2_ablation.png")

if __name__ == "__main__":
    plot_baseline_comparison()
    plot_ablation()