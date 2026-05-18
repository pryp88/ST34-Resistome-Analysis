# =========================================================
# Figure 2: AMR Class Distribution in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script calculates and visualizes prevalence
# of antimicrobial resistance classes among
# Salmonella enterica ST34 genomes.
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt
import re

# =========================================================
# LOAD RESISTOME MATRIX
# =========================================================

matrix_file = "output/ST34_Resistome_Matrix.xlsx"

df = pd.read_excel(matrix_file)

gene_cols = df.columns[1:]  # Exclude accession column

total_genomes = df.shape[0]

print("Total genomes:", total_genomes)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_gene(gene):
    """
    Remove allele suffix from gene names.
    Example:
    tet(B)_2 -> tet(B)
    """
    return re.sub(r"_\\d+$", "", gene)

def assign_amr_class(gene):

    g = clean_gene(gene)

    if re.match(r"^(aac|aad|aph|armA|rmt|ant)", g):
        return "Aminoglycoside"

    elif g.startswith("bla"):
        return "β-lactamase"

    elif g.startswith("tet"):
        return "Tetracycline"

    elif re.match(r"^(sul|dfr)", g):
        return "Sulfonamide / Trimethoprim"

    elif re.match(r"^(floR|cat|cml)", g):
        return "Phenicol"

    elif g.startswith("qnr"):
        return "Quinolone"

    elif g.startswith("mcr"):
        return "Colistin"

    elif re.match(r"^(mdt|emr|oqx|acr)", g):
        return "Efflux / Intrinsic"

    else:
        return "Other AMR"

# =========================================================
# MAP GENES TO AMR CLASSES
# =========================================================

class_map = {}

for gene in gene_cols:

    cls = assign_amr_class(gene)

    class_map.setdefault(cls, []).append(gene)

# =========================================================
# CALCULATE CLASS PREVALENCE
# =========================================================

class_results = []

for cls, genes in class_map.items():

    # Genome considered positive if
    # any gene from class is present

    class_presence = df[genes].sum(axis=1) > 0

    prevalence = (
        class_presence.sum() / total_genomes
    ) * 100

    class_results.append({
        "AMR_Class": cls,
        "Genomes_with_class": class_presence.sum(),
        "Prevalence_percent": prevalence
    })

class_df = pd.DataFrame(class_results)

# =========================================================
# SORT RESULTS
# =========================================================

class_df = class_df.sort_values(
    "Prevalence_percent",
    ascending=False
)

# =========================================================
# SAVE TABLE
# =========================================================

output_table = "output/ST34_AMR_Class_Distribution.xlsx"

class_df.to_excel(output_table, index=False)

print("AMR class distribution table saved.")
print("Output:", output_table)

# =========================================================
# GENERATE FIGURE
# =========================================================

plot_df = class_df.sort_values(
    "Prevalence_percent",
    ascending=True
)

plt.figure(figsize=(8, 6))

plt.barh(
    plot_df["AMR_Class"],
    plot_df["Prevalence_percent"]
)

plt.xlabel("Prevalence (%)")

plt.title(
    "Resistance Class Distribution in Salmonella enterica ST34"
)

plt.tight_layout()

# =========================================================
# SAVE FIGURE
# =========================================================

output_figure = "figures/Figure2_AMR_Class_Distribution.png"

plt.savefig(
    output_figure,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Figure 2 saved successfully.")
print("Output:", output_figure)