# =========================================================
# Figure 1: AMR Gene Distribution in ST34
# =========================================================
# Author: Dr. Shaikh Akbarpasha
# Project: ST34 Resistome Analysis
#
# Description:
# This script generates a grouped horizontal bar plot
# showing prevalence of major AMR genes across
# Salmonella enterica ST34 genomes.
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt
import re

# =========================================================
# LOAD PREVALENCE DATA
# =========================================================

prev_file = "output/ST34_Gene_Prevalence.xlsx"

df = pd.read_excel(prev_file)

# Keep genes with prevalence >=10%
df = df[df["Prevalence_percent"] >= 10].copy()

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
# CLEAN GENE NAMES AND ASSIGN CLASSES
# =========================================================

df["Gene_clean"] = df["Gene"].apply(clean_gene)

df["AMR_Class"] = df["Gene"].apply(assign_amr_class)

# =========================================================
# DEFINE CLASS ORDER
# =========================================================

class_order = [
    "Aminoglycoside",
    "β-lactamase",
    "Tetracycline",
    "Sulfonamide / Trimethoprim",
    "Phenicol",
    "Quinolone",
    "Colistin",
    "Efflux / Intrinsic",
    "Other AMR"
]

df["AMR_Class"] = pd.Categorical(
    df["AMR_Class"],
    categories=class_order,
    ordered=True
)

df = df.sort_values(
    ["AMR_Class", "Prevalence_percent"],
    ascending=[True, False]
)

# =========================================================
# BUILD PLOT STRUCTURE
# =========================================================

y_labels = []
y_values = []
class_positions = {}

current_pos = 0

for cls in class_order:

    subset = df[df["AMR_Class"] == cls]

    if subset.empty:
        continue

    start = current_pos

    for _, row in subset.iterrows():

        y_labels.append(row["Gene_clean"])
        y_values.append(row["Prevalence_percent"])

        current_pos += 1

    end = current_pos - 1

    class_positions[cls] = (start + end) / 2

    # Spacer between classes
    y_labels.append("")
    y_values.append(0)

    current_pos += 1

# Remove final spacer
y_labels = y_labels[:-1]
y_values = y_values[:-1]

# =========================================================
# GENERATE FIGURE
# =========================================================

fig, ax = plt.subplots(figsize=(10, 14))

y_positions = range(len(y_values))

ax.barh(y_positions, y_values)

ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels, fontsize=9)

ax.set_xlabel("Prevalence (%)")

ax.set_title(
    "AMR Gene Distribution in Salmonella enterica ST34"
)

# Aminoglycosides at top
ax.invert_yaxis()

# =========================================================
# ADD CLASS LABELS
# =========================================================

x_max = max(y_values) + 5

for cls, midpoint in class_positions.items():

    ax.text(
        x_max,
        midpoint,
        cls,
        va="center",
        ha="left",
        fontsize=10,
        fontweight="bold"
    )

# =========================================================
# SAVE FIGURE
# =========================================================

plt.tight_layout()

output_figure = "figures/Figure1_AMR_Gene_Distribution.png"

plt.savefig(
    output_figure,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Figure 1 saved successfully.")
print("Output:", output_figure)