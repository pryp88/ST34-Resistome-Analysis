# =========================================================
# Figure 5: AMR Gene Co-occurrence Heatmap in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script identifies highly prevalent AMR genes
# in Salmonella enterica ST34 genomes and generates
# a co-occurrence heatmap showing relationships
# among major resistance determinants.
# =========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# LOAD RESISTOME MATRIX
# =========================================================

matrix_file = "output/ST34_Resistome_Matrix.xlsx"

df = pd.read_excel(matrix_file)

gene_cols = df.columns[1:]  # Exclude accession column

total_genomes = df.shape[0]

print("Total genomes:", total_genomes)

# =========================================================
# CALCULATE GENE PREVALENCE
# =========================================================

prevalence = (
    df[gene_cols]
    .sum()
    .sort_values(ascending=False)
)

# =========================================================
# SELECT TOP GENES
# =========================================================

top_genes = prevalence.head(30).index.tolist()

print("Top 30 genes:")
print(top_genes)

# Remove intrinsic gene
filtered_genes = [
    gene for gene in top_genes
    if gene != "aac(6')-Iaa_1"
]

# Select top 15 genes
top15 = filtered_genes[:15]

print("\nTop 15 genes used for co-occurrence:")
print(top15)

# =========================================================
# COMPUTE CO-OCCURRENCE MATRIX
# =========================================================

co_matrix = pd.DataFrame(
    index=top15,
    columns=top15
)

for g1 in top15:

    for g2 in top15:

        both_present = (
            (df[g1] == 1) &
            (df[g2] == 1)
        ).sum()

        co_occurrence = (
            both_present / total_genomes
        ) * 100

        co_matrix.loc[g1, g2] = co_occurrence

co_matrix = co_matrix.astype(float)

# =========================================================
# SAVE CO-OCCURRENCE TABLE
# =========================================================

output_table = "output/ST34_Cooccurrence_Matrix.xlsx"

co_matrix.to_excel(output_table)

print("Co-occurrence matrix saved.")
print("Output:", output_table)

# =========================================================
# GENERATE HEATMAP
# =========================================================

plt.figure(figsize=(10, 8))

heatmap = plt.imshow(
    co_matrix,
    aspect="auto",
    cmap="RdYlGn_r"
)

# Color scale
cbar = plt.colorbar(heatmap)

cbar.set_label("Co-occurrence (%)")

# Axis labels
plt.xticks(
    range(len(top15)),
    top15,
    rotation=90
)

plt.yticks(
    range(len(top15)),
    top15
)

plt.title(
    "Co-occurrence of Major AMR Genes in Salmonella enterica ST34"
)

plt.tight_layout()

# =========================================================
# SAVE FIGURE
# =========================================================

output_figure = (
    "figures/Figure5_AMR_Gene_Cooccurrence_Heatmap.png"
)

plt.savefig(
    output_figure,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Figure 5 saved successfully.")
print("Output:", output_figure)