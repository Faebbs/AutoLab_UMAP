from ete3 import NCBITaxa
import time


def update_local_ncbi():
    ncbi = NCBITaxa() # stored in /home/.etetoolkit
    ncbi.update_taxonomy_database()

def ncbi_lineage(ncbiID): #TODO Alternative oder weg?
    #TODO weitere Idee: No ranks rausschmeißen
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(ncbiID)
    names = ncbi.get_taxid_translator(lineage)
    for taxid in lineage:
        print(names[taxid])
    tree = ncbi.get_topology(lineage)
    x = tree.get_ascii(attributes=["sci_name","rank"])
    return x


# Testcases
if __name__ == "__main__":
    # update_local_ncbi()
    start = time.time()
    print(ncbi_lineage(9606))
    end = time.time()
    print(f"Runtime: {end - start}s")
