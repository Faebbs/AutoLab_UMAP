import requests
from requests import Timeout
from ete3 import NCBITaxa

def update_local_ncbi():
    ncbi = NCBITaxa() # stored in /home/.etetoolkit
    ncbi.update_taxonomy_database()

def ncbi_lineage_local(ncbiID): #TODO Alternative oder weg?
    #TODO weitere Idee: No ranks rausschmeißen
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(ncbiID)
    # names = ncbi.get_taxid_translator(lineage)
    # for taxid in lineage:
    #     print(names[taxid])
    tree = ncbi.get_topology(lineage)
    print(tree.get_ascii(attributes=["sci_name", "rank"]))

# TODO Vielleicht ne Idee: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/reference-docs/data-packages/taxonomy/

def ncbi_lineage(ncbiID): #TODO Scheiße weil online und langsam mit 0.3s pro Aufruf
    # Slices ncbiId so that only number remains
    ncbiID = ncbiID[4:]
    try:
        ncbiID = int(ncbiID)
    except ValueError:
        return ("Invalid ncbiID") #TODO Fehlerbehandlung

    # Make Request to ncbi Taxonomy Database, returns JSON format
    try:
        url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/{ncbiID}/dataset_report?returned_content=METADATA"
        response = requests.get(url, timeout=1)
    except ConnectionError:
        return ("ConnectionError") #TODO Fehlerbehandlung
    except Timeout:
        return ("Timeout") #TODO Fehlerbehandlung
    # Takes lineage from ncbi Response
    response = response.json()
    # Error when ncbiId couldn't be found in database
    if "errors" in response["reports"][0].keys():
        return response["reports"][0]["errors"][0]["reason"]
    # lineage as dict with taxonomic rank and the corresponding name and id
    lineage = response["reports"][0]["taxonomy"]["classification"]
    return lineage

# Testcases
if __name__ == "__main__":
    print(ncbi_lineage_local(9606))
    # print(ncbi_lineage("ncbi9606"))

