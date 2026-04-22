gene_identifiers = {
    "FRAT1": "ENSG00000165879",
    "ADA": "ENSG00000196839",
    "FXN": "ENSG00000165060",
    "RNU6-269P": "ENSG00000206621",
    "MIR633": "ENSG00000207758",
    "TTTY4C": "ENSG00000228670",
    "RBMY2YP": "ENSG00000229352",
    "FGFR3": "ENSG00000068078",
    "KDR": "ENSG00000128052",
    "ANK2": "ENSG00000145362"
}

print(f"Number of genes: {len(gene_identifiers)}")
for gene, ident in gene_identifiers.items():
    print(f'{gene}: -> {ident}')

