from os.path import join

ENT_FORMAT = '.ent'
PDB_FORMAT = '.pdb'

# database root
db_dir = 'data'

# raw data
pdb_db = join(db_dir, 'pdb_db')
alpha_db = join(db_dir, 'AlphaFold_HUMAN')

# structure dir root
structure_db = join(db_dir, 'structure_db')
# residue pair
resPairsByChainPairs_csv = join(structure_db, 'resPairsByChainPairs.csv')
# Chain Res Pairs
ChainResPairs_csv = join(structure_db, 'ChainResPairs_csv.csv')
# PDB length
PDBsingleChain_len_csv = join(structure_db, 'PDBsingleChain_len_csv.csv')
# AlphaFold length
alphaFoldHuman_len_csv = join(structure_db, 'AlphaFoldHuman_len_csv.csv')
# dimer
dimer_csv = join(structure_db, 'dimer.csv')
# not protein
notprotein_csv = join(structure_db, 'notProtein.csv')

# sasa
sasa_db = join(db_dir, 'sasa_db')
# max contact chain pair sasa and buried area 
ChainPair_sasa_bsa_csv = join(sasa_db, 'ChainPair_sasa_bsa_csv.csv')
# dimer sasa
dimer_ChainPair_sasa_bsa_csv = join(sasa_db, 'dimer_ChainPair_sasa_bsa_csv.csv')
# chain pair sasa
ResPairs_sasa_csv = join(sasa_db, 'ResPairs_sasa_csv.csv')
# residues sasa
ChainResPairs_sasa_csv = join(sasa_db, 'ChainResPairs_sasa_csv.csv')
# PDB sasa
PDBsingleChain_sasa_csv = join(sasa_db, 'PDBsingleChain_sasa_csv.csv')
# AlphaFold sasa
alphaFoldHuman_sasa_csv = join(sasa_db, 'AlphaFoldHuman_sasa_csv.csv')

# DSSP
# dssp path
dssp_db = join(db_dir, 'dssp_db')
dssp_path = '/home/ubuntu/anaconda3/bin/mkdssp'
Alpha_NumberHelixLoopsSheet_csv = join(dssp_db, 'Alpha_NumberHelixLoopsSheet.csv')
PDB_NumberHelixLoopsSheet_csv = join(dssp_db, 'PDB_NumberHelixLoopsSheet.csv')
