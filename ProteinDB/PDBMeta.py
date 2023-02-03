"""
This file is used to extract metadata for a specific PDB.
#Metadata can be mostly grabbed from the ftp: https://www.rcsb.org/docs/file-downloads/ftp-services#summaries-of-pdb
- You can get it from the
https://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt
 """
import sys
import Bio.PDB
import Bio.PDB.StructureBuilder
from PDBMetaExtractor import MetaDataExtractor

from Bio.PDB import PDBParser
from Bio.PDB.Residue import Residue

print("The script has the name %s" % (sys.argv))
# pass the name of the pdb code like 1ahw
# pass any of the metadata like resolution, idcode, deposition_date, author, head
pdb_code = sys.argv[1]
meta_data = sys.argv[2]

extractor = MetaDataExtractor(pdb_code)
data = extractor.get_metadata(meta_data)
print("METADATA: {}".format(data))