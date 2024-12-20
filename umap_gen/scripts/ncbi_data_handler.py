from ete3 import NCBITaxa
import requests
from requests import Timeout


def update_local_ncbi():
    """
    Updates local NCBI copy
    :return:
    """
    ncbi = NCBITaxa() # stored in /home/.etetoolkit
    ncbi.update_taxonomy_database()
    print("Local Database has been created at ~/.etetoolkit")

def ncbi_lineage(ncbiID):
    """
    Fetches Information of local NCBI Taxonomy via ete3
    :param ncbiID: ID of organism as String or Integer
    :return: Dict with the rank and name of given organism
    """
    # turning given ncbi ID to number
    try:
        ncbiID = int(ncbiID)
    except(ValueError):
        # tries to delete letters from given ID
        processed_ncbiId = ""
        for el in ncbiID:
            if el.isdigit() is True:
                processed_ncbiId = processed_ncbiId + el
        try:
            ncbiID = int(processed_ncbiId)
        except(ValueError):
            return "Parse Error"
    # gets lineage from local NCBI Taxonomy copy
    ncbi = NCBITaxa()
    try:
        lineage = ncbi.get_lineage(ncbiID)
    except (ValueError): # TODO Fehlerbehandlung wenn ID nicht vorhanden
        return "Database Error"
    # translates IDs to ranks
    names = ncbi.get_taxid_translator(lineage)
    # list with wanted ranks
    wanted_ranks = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
    # creates dict with relevant ranks of organism
    lineage_dic = {} # Dict with rank and name
    for taxid in lineage:
        rank_raw = ncbi.get_rank([taxid])
        values = list(rank_raw.values())
        rank = values[0]
        # filters out the unwanted ranks
        if rank in wanted_ranks:
            name = names[taxid]
            new_dict = {rank: name}
            lineage_dic.update(new_dict)
    return lineage_dic



def ncbi_lineage_deprecated(ncbiID):
    """
    Fetches information of NCBI taxonomy via URL Request. Deprecated cause other approach was used.
    :param ncbiID: String like "ncbi9606"
    :return: Dict with the taxonomic rank and the specific taxa of the searched organism
    """
    # Slices ncbiId so that only number remains
    ncbiID = ncbiID[4:]
    try:
        ncbiID = int(ncbiID)
    except ValueError:
        return ("Invalid ncbiID")
    # Make Request to ncbi Taxonomy Database, returns JSON format
    try:
        url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/taxonomy/taxon/{ncbiID}/dataset_report?returned_content=METADATA"
        response = requests.get(url, timeout=1)
    except ConnectionError:
        return ("ConnectionError")
    except Timeout:
        return ("Timeout")
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
    # update_local_ncbi()

    print(ncbi_lineage(9606))
    # print(ncbi_lineage_deprecated("ncbi9606"))

