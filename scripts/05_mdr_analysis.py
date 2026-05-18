# =========================================================
# Figure 3: Multidrug Resistance Analysis in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script calculates multidrug resistance (MDR)
# prevalence among Salmonella enterica ST34 genomes
# and generates an MDR distribution pie chart.
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
# MAP GENES TO CLASSES
# =========================================================

class_map = {}

for gene in gene_cols:

    cls = assign_amr_class(gene)

    class_map.setdefault(cls, []).append(gene)

# =========================================================
# COUNT RESISTANCE CLASSES PER GENOME
# =========================================================

class_counts = pd.DataFrame()

for cls, genes in class_map.items():

    class_counts[cls] = (
        df[genes].sum(axis=1) > 0
    ).astype(int)

# Total resistance classes per genome
class_counts["Total_Classes"] = class_counts.sum(axis=1)

# MDR definition:
# Resistance to 3 or more antimicrobial classes

class_counts["MDR_Status"] = (
    class_counts["Total_Classes"] >= 3
)

# =========================================================
# CALCULATE MDR STATISTICS
# =========================================================

mdr_count = class_counts["MDR_Status"].sum()

non_mdr_count = total_genomes - mdr_count

mdr_percent = (
    mdr_count / total_genomes
) * 100

print("MDR genomes:", mdr_count)
print("Non-MDR genomes:", non_mdr_count)
print("MDR percentage:", round(mdr_percent, 2))

# =========================================================
# SAVE SUMMARY TABLE
# =========================================================

summary_df = pd.DataFrame({
    "Category": ["MDR", "Non-MDR"],
    "Genome_Count": [mdr_count, non_mdr_count]
})

output_table = "output/ST34_MDR_Summary.xlsx"

summary_df.to_excel(output_table, index=False)

print("MDR summary table saved.")
print("Output:", output_table)

# =========================================================
# GENERATE PIE CHART
# =========================================================

labels = [
    "MDR (≥3 classes)",
    "Non-MDR (<3 classes)"
]

sizes = [mdr_count, non_mdr_count]

plt.figure(figsize=(6, 6))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title(
    "Multidrug Resistance in Salmonella enterica ST34"
)

plt.tight_layout()

# =========================================================
# SAVE FIGURE
# =========================================================

output_figure = "figures/Figure3_MDR_PieChart.png"

plt.savefig(
    output_figure,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Figure 3 saved successfully.")
print("Output:", output_figure)