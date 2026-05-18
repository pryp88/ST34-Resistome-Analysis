# =========================================================
# Figure 4: AMR Gene Burden Analysis in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script calculates antimicrobial resistance
# gene burden among Salmonella enterica ST34 genomes
# and visualizes the distribution using violin and
# box plot analysis.
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# LOAD RESISTOME MATRIX
# =========================================================

matrix_file = "output/ST34_Resistome_Matrix.xlsx"

df = pd.read_excel(matrix_file)

gene_cols = df.columns[1:]  # Exclude accession column

# =========================================================
# CALCULATE TOTAL AMR GENES PER GENOME
# =========================================================

df["Total_AMR_Genes"] = df[gene_cols].sum(axis=1)

# =========================================================
# SUMMARY STATISTICS
# =========================================================

mean_genes = df["Total_AMR_Genes"].mean()

median_genes = df["Total_AMR_Genes"].median()

min_genes = df["Total_AMR_Genes"].min()

max_genes = df["Total_AMR_Genes"].max()

print("Mean AMR genes per genome:",
      round(mean_genes, 2))

print("Median AMR genes per genome:",
      median_genes)

print("Minimum AMR genes:",
      min_genes)

print("Maximum AMR genes:",
      max_genes)

# =========================================================
# SAVE SUMMARY TABLE
# =========================================================

summary_df = pd.DataFrame({
    "Statistic": [
        "Mean",
        "Median",
        "Minimum",
        "Maximum"
    ],
    "Value": [
        round(mean_genes, 2),
        median_genes,
        min_genes,
        max_genes
    ]
})

output_table = "output/ST34_AMR_Gene_Burden_Summary.xlsx"

summary_df.to_excel(output_table, index=False)

print("Gene burden summary saved.")
print("Output:", output_table)

# =========================================================
# GENERATE VIOLIN + BOXPLOT
# =========================================================

plt.figure(figsize=(8, 4))

# Violin plot
parts = plt.violinplot(
    df["Total_AMR_Genes"],
    vert=False,
    showmedians=False,
    showextrema=False
)

# Boxplot overlay
plt.boxplot(
    df["Total_AMR_Genes"],
    vert=False,
    widths=0.15
)

# Remove meaningless y-axis labels
plt.yticks([])

plt.xlabel("Number of AMR Genes per Genome")

plt.title(
    "Distribution of AMR Gene Burden in Salmonella enterica ST34"
)

plt.tight_layout()

# =========================================================
# SAVE FIGURE
# =========================================================

output_figure = (
    "figures/Figure4_AMR_Gene_Burden_Violin_Boxplot.png"
)

plt.savefig(
    output_figure,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Figure 4 saved successfully.")
print("Output:", output_figure)