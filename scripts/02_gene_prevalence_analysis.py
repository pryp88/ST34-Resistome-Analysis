# =========================================================
# AMR Gene Prevalence Analysis in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script calculates prevalence of antimicrobial
# resistance genes among Salmonella enterica ST34 genomes.
# =========================================================

import pandas as pd

# =========================================================
# INPUT FILE
# =========================================================

resistome_file = "output/ST34_Resistome_Matrix.xlsx"

# =========================================================
# LOAD RESISTOME MATRIX
# =========================================================

df = pd.read_excel(resistome_file)

print("Matrix shape:", df.shape)

# =========================================================
# EXTRACT GENE COLUMNS
# =========================================================

gene_columns = df.columns[1:]  # Exclude accession column

total_genomes = df.shape[0]

print("Total ST34 genomes:", total_genomes)
print("Total AMR genes:", len(gene_columns))

# =========================================================
# CALCULATE GENE PREVALENCE
# =========================================================

gene_counts = df[gene_columns].sum()

gene_prevalence = (gene_counts / total_genomes) * 100

prevalence_df = pd.DataFrame({
    "Gene": gene_prevalence.index,
    "Genomes_with_gene": gene_counts.values,
    "Prevalence_percent": gene_prevalence.values
})

# =========================================================
# SORT BY PREVALENCE
# =========================================================

prevalence_df = prevalence_df.sort_values(
    by="Prevalence_percent",
    ascending=False
)

# =========================================================
# SAVE OUTPUT
# =========================================================

output_path = "output/ST34_Gene_Prevalence.xlsx"

prevalence_df.to_excel(output_path, index=False)

print("Gene prevalence table saved successfully.")
print("Output:", output_path)

# =========================================================
# DISPLAY TOP GENES
# =========================================================

print("\nTop 20 AMR genes:")
print(prevalence_df.head(20))