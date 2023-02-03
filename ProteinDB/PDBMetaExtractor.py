from Bio.PDB import PDBParser
import requests


class MetaDataExtractor:
    """
    Extract all the metadata from the pdb code
    """
    metadata_dict = None
    structure = None
    pdb_code = None

    def __init__(self, pdb_code):
        """
        initialize the code for extracting metadata
        """
        parser = PDBParser()
        self.pdb_code = pdb_code
        self.structure = parser.get_structure("PHA-L", "data/testdata/{}.pdb".format(pdb_code))
        # print(self.structure.header)
        self.metadata_dict = {
            "id_code": self.structure.header["idcode"],
            "deposition_date": self.structure.header["deposition_date"],
            "head": self.structure.header["head"],
            "organism": self.structure.header.get("source", None).get("1", None).get('organism_scientific',
                                                                                     None).upper(),
            "compound": self.structure.header.get('compound', None),
            "source": self.structure.header.get('source', None),
            "author": self.structure.header.get('author', None),
            "resolution": self.structure.header.get("resolution", None),
            "structure_method": self.structure.header['structure_method'],
            "abstract": self.retrieve_publication_details(self.structure.header["idcode"]),
            "global_stochiometry": self.retrieve_global_stoichiometry_details(self.structure.header['idcode'])
        }

    def get_metadata_dict(self):
        """
        retrieves metadata dictionary
        """
        return self.metadata_dict

    def get_metadata(self, meta_data=None):
        """
        returns the value for a specific metadata key
        """
        metadata_keys = self.structure.header.keys()  # to look at the different meta data headers
        meta_data_value = None

        if meta_data and meta_data in metadata_keys:
            meta_data_value = self.structure.header[meta_data]

        return meta_data_value

    # function to retrieve the publication details about author from Pubmed website
    def retrieve_publication_details(self, pbd_code):
        """
        retrieve publication details from the website
        """
        TOOL_NAME = "ProteinDatabaseSystem"
        rcsb_api_json_response = requests.get("https://data.rcsb.org/rest/v1/core/entry/{}/".format(pbd_code)).json()
        pubmedid = rcsb_api_json_response.get("rcsb_entry_container_identifiers", None).get("pubmed_id")
        pub_med_api_abstract_response = requests.get(
            "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=text&rettype=abstract&id={}".format(
                pubmedid))
        return pub_med_api_abstract_response.content

    # retrieve Global Stoichiometry using api
    def retrieve_global_stoichiometry_details(self, pbd_code):
        """
        retrieve global stoichiometry information from the pdb code
        """
        rcsb_stochiometry_api_json_response = requests.get(
            "https://data.rcsb.org/rest/v1/core/assembly/{}/1/".format(pbd_code)).json()
        oligomeric_state = rcsb_stochiometry_api_json_response.get('rcsb_struct_symmetry', None)[0].get(
            'oligomeric_state')
        stoichiometry = rcsb_stochiometry_api_json_response.get('rcsb_struct_symmetry', None)[0].get('stoichiometry')
        stochio = ''
        for items in stoichiometry:
            stochio += items
        global_stochiometry = oligomeric_state + ' - ' + stochio
        return global_stochiometry
