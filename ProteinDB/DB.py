from os.path import join

ENT_FORMAT = '.ent'
PDB_FORMAT = '.pdb'

# database root
db_dir='data'

# raw data
pdb_db=join(db_dir,'pdb_db')
alpha_db=join(db_dir,'AlphaFold_HUMAN')

# dimer
category_db=join(db_dir,'category_db')
dimer_csv=join(category_db,'dimer.csv')
notprotein_csv=join(category_db,'notProtein.csv')

# structure dir root
structure_db=join(db_dir,'structure_db')
#residue pair
resPairsByChainPairs_csv=join(structure_db,'resPairsByChainPairs.csv')
# Chain Res Pairs
ChainResPairs_csv=join(structure_db,'ChainResPairs_csv.csv')
# PDB length
PDBsingleChain_len_csv=join(structure_db,'PDBsingleChain_len_csv.csv')
# AlphaFold length
alphaFoldHuman_len_csv=join(structure_db,'AlphaFoldHuman_len_csv.csv')


# sasa 
sasa_db=join(db_dir,'sasa_db')
# chain pair sasa
ResPairs_sasa_csv=join(sasa_db,'ResPairs_sasa_csv.csv')
# residues sasa
ChainResPairs_sasa_csv=join(sasa_db,'ChainResPairs_sasa_csv.csv')
# PDB sasa
PDBsingleChain_sasa_csv=join(sasa_db,'PDBsingleChain_sasa_csv.csv')
# AlphaFold sasa
alphaFoldHuman_sasa_csv=join(sasa_db,'AlphaFoldHuman_sasa_csv.csv')

# DSSP
# dssp path
dssp_db=join(db_dir,'dssp_db')
dssp_path='/home/ubuntu/anaconda3/bin/mkdssp'
Alpha_NumberHelixLoopsSheet_csv=join(dssp_db,'Alpha_NumberHelixLoopsSheet.csv')