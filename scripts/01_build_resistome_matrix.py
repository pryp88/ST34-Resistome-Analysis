# =========================================================
# ST34 Resistome Matrix Construction
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script filters ResFinder output for
# Salmonella enterica ST34 genomes and generates
# a binary resistome presence–absence matrix.
# =========================================================

import pandas as pd

# =========================================================
# INPUT FILES
# =========================================================

resfinder_file = "input/summary_resfinder.tsv"
st34_master_file = "input/ST34_MASTER_FINAL.xlsx"

# =========================================================
# LOAD DATA
# =========================================================

resfinder = pd.read_csv(resfinder_file, sep="\t")
st34_master = pd.read_excel(st34_master_file)

print("ResFinder shape:", resfinder.shape)
print("ST34 master shape:", st34_master.shape)

# =========================================================
# EXTRACT ASSEMBLY ACCESSION
# =========================================================

resfinder["assembly_accession"] = (
    resfinder["#FILE"]
    .str.extract(r"(GCF_\\d+\\.\\d+)")
)

# =========================================================
# FILTER ST34 GENOMES
# =========================================================

st34_ids = set(st34_master["assembly_accession"])

resfinder_st34 = resfinder[
    resfinder["assembly_accession"].isin(st34_ids)
].copy()

print("ST34 filtered shape:", resfinder_st34.shape)

# =========================================================
# REMOVE NON-GENE COLUMNS
# =========================================================

gene_columns = [
    col for col in resfinder_st34.columns
    if col not in ["#FILE", "NUM_FOUND", "assembly_accession"]
]

# Convert:
# "." -> 0
# detected gene -> 1

resfinder_st34[gene_columns] = (
    resfinder_st34[gene_columns]
    .replace(".", 0)
)

resfinder_st34[gene_columns] = (
    resfinder_st34[gene_columns]
    .applymap(lambda x: 1 if str(x) != "0" else 0)
)

# =========================================================
# FINAL RESISTOME MATRIX
# =========================================================

st34_resistome_matrix = resfinder_st34[
    ["assembly_accession"] + gene_columns
]

# =========================================================
# SAVE OUTPUT
# =========================================================

output_path = "output/ST34_Resistome_Matrix.xlsx"

st34_resistome_matrix.to_excel(output_path, index=False)

print("ST34 resistome matrix saved successfully.")
print("Output:", output_path)