# ST34 Resistome Analysis

Computational analysis of antimicrobial resistance gene diversity and multidrug resistance patterns in *Salmonella enterica* Sequence Type 34 (ST34).

---

## Project Overview

This project investigates the resistome architecture of 937 publicly available *Salmonella enterica* ST34 genomes using computational genomics and bioinformatics approaches.

The study focuses on:

- Antimicrobial resistance gene prevalence
- Resistance class distribution
- Multidrug resistance (MDR) analysis
- AMR gene burden variation
- Gene co-occurrence patterns

The project was developed as part of the JIGNASA 2026 State Level Student Study Project Competition.

---

## Workflow Summary

The computational workflow included:

1. Retrieval of publicly available *Salmonella enterica* genomes from NCBI RefSeq
2. Genome quality assessment using QUAST
3. Sequence typing using MLST
4. Serovar confirmation using SISTR
5. Selection of Sequence Type 34 (ST34) genomes
6. Detection of antimicrobial resistance genes using ResFinder
7. Computational resistome analysis using Python

---

## Bioinformatics Tools Used

- QUAST
- MLST
- SISTR
- ResFinder
- Python
- pandas
- NumPy
- matplotlib

---

## Repository Structure

```text
ST34-Resistome-Analysis/
│
├── figures/
│   ├── Figure1_AMR_Gene_Distribution.png
│   ├── Figure2_AMR_Class_Distribution.png
│   ├── Figure3_MDR_PieChart.png
│   ├── Figure4_AMR_Gene_Burden_Violin_Boxplot.png
│   ├── Figure5_AMR_Gene_Cooccurrence_Heatmap.png
│   └── Workflow_Diagram.png
│
└── scripts/
    ├── 01_build_resistome_matrix.py
    ├── 02_gene_prevalence_analysis.py
    ├── 03_figure1_amr_gene_distribution.py
    ├── 04_amr_class_distribution.py
    ├── 05_mdr_analysis.py
    ├── 06_amr_gene_burden_analysis.py
    └── 07_gene_cooccurrence_heatmap.py
```

---

## Major Findings

- 90.5% of analyzed genomes were multidrug resistant
- Aminoglycoside resistance genes were present in 100% of genomes
- Major resistance genes included:
  - tet(B)
  - blaTEM-1B
  - aph(6)-Id
  - aph(3'')-Ib
  - sul2
- Strong co-occurrence patterns were observed among major resistance determinants

---

## Author

**Dr. Shaikh Akbarpasha**  
Assistant Professor & Head  
Department of Microbiology  
SRNK Government College (Autonomous), Banswada  
Telangana, India

---

## Student Project Contributors

- ISHRATH FATHIMA
- KOTARI VAISHNAVI
- AYESHA SIDDIQA
- LINGALA SIRI REDDY
- THAVTHI SATHVIKA

---

## Project Link

Repository:
https://github.com/pryp88/ST34-Resistome-Analysis
