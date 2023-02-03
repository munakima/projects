#Fetch the latest metadata.
cd data/metadata
#Clean previous data
rm *.txt .*ids
#Fetch entry types
wget http://ftp.rcsb.org/pub/pdb/derived_data/pdb_entry_type.txt
#Fetch sequences
wget http://ftp.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt
#Fetch entries
wget http://ftp.rcsb.org/pub/pdb/derived_data/index/entries.idx 
#Fetch all PDB structure file
wget ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/*
# fetch alphafold human ids
wget https://ftp.ebi.ac.uk/pub/databases/alphafold/latest/UP000005640_9606_HUMAN_v2.tar
