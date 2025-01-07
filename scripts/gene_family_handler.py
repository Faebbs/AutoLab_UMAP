import pandas as pd

def gene_annotation(data):
    genes = data.loc[:, "geneID"].unique()
    geneID = []
    family = []
    subfamily = []
    gene_name = []
    for gen in genes:
        has_subfamily = True
        parts = gen.split("_", 2)
        # sets geneID
        geneID.append(gen)
        # sets family
        family.append(parts[0])
        # checks if gene has a subclass, then sets subclass
        try:
            test_subfamily = int(parts[1])
            subfamily_concat = parts[0] + "_" + parts[1]
            subfamily.append(subfamily_concat)
        except(ValueError, TypeError):
            has_subfamily = False
            subfamily.append(parts[0])
        # sets gene
        if has_subfamily is True:
            i = 2
        else:
            i = 1
        gene_concat = ""
        while i < len(parts):
            gene_concat = gene_concat + "_" + parts[i]
            i = i + 1
        gene_concat = gene_concat[1:]
        gene_name.append(gene_concat)
    matrix_dict = {"geneID":geneID, "family":family, "subfamily":subfamily, "gene_name":gene_name}
    gene_matrix = pd.DataFrame(matrix_dict)
    return gene_matrix

if __name__ == "__main__":
    data_read = pd.read_csv("/home/fabian/Documents/data/eukaryots.phyloprofile", sep="\t")
    gene_annotation(data_read)