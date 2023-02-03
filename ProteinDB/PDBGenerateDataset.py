import PDBStructure as pdbStru
import PDBContactMap as pdbMap
import PDBFreesasa as pdbSasa
import PDBdssp as pdbDssp
import DB
from os.path import join


#########################
# Generate dimer dataset#
#########################
# Generate all dimer into CSV file.
# ['structure_id']
def generateDimer(test=None):
    pdbStru.getAllDimerPDB(pdbStru.loadingPDB(),test)


#######################################
# Generate single chain length dataset#
#######################################
# Generate a length of single chain PDB csv
# ['structure_id', 'chain_id', 'length']
def generateLenSingleChainPDB(test=None):
    pdb_list = pdbStru.loadingPDB()
    pdbStru.getListLenByStructure(pdb_list, DB.PDBsingleChain_len_csv, test)


# Generate a length of single chain AlphaFold csv
# ['structure_id', 'chain_id', 'length']
def generateLenSingleChainAlphaFold(test=None):
    pdb_list = pdbStru.loadingAlpha()
    pdbStru.getListLenByStructure(pdb_list, DB.alphaFoldHuman_len_csv, test)


#####################################
# Generate single chain sasa dataset#
#####################################
# Generate sasa of PDB single chain
# ['structure_id', 'chain_id', 'sasa']
def generateSasaPDBSingleChain(test=None):
    pdb_list = pdbStru.loadingPDB()
    pdbSasa.loadListForSasaSingleChain(pdb_list, DB.PDBsingleChain_sasa_csv, test)


# Generate sasa of AlphaFold single chain
# ['structure_id', 'chain_id', 'sasa']
def generateSasaAlphaSingleChain(test=None):
    pdb_list = pdbStru.loadingAlpha()
    pdbSasa.loadListForSasaSingleChain(pdb_list, DB.alphaFoldHuman_sasa_csv, test)


########################
# Generate DSSP dataset#
########################
# For generate dssp of AlphaFold
# ['structure_id', 'loops', 'alpha_helix', 'beta_sheet']
def generateDsspAlphaFold(test=None):
    pdb_list = pdbStru.pdbStru.loadingPDB()
    pdbDssp.loadListForDSSPAlphaFold(pdb_list, DB.Alpha_NumberHelixLoopsSheet_csv, test)


# For generate dssp of PDB
# ['structure_id', 'loops', 'alpha_helix', 'beta_sheet']
def generateDsspPDBSingleChain(test=None):
    pdb_list = pdbStru.loadingAlpha()
    pdbDssp.loadListForDSSPAlphaFold(pdb_list, DB.PDB_NumberHelixLoopsSheet_csv, test)
    
    
###################################
# Generate maximum contact dataset#
###################################
# Get which chains are close to each other in one PDB structure
# and list all residues of those chains which are within a certain threshold distance
# which we set as 5Å. If passing 'test' to function that will not save into csv.
# ['structure_id', 'chains', 'chain_pair', 'res_pair']
def generateAllPDBContact(test=None):
    pdb_list = pdbStru.loadingPDB()
    pdbMap.listAllPDBContact(pdb_list, DB.ChainResPairs_csv, test)


########################################
# Generate maximum contact sasa dataset#
########################################
# NOTE: based on generateAllPDBContact and generateAllResPairSasaBsa
# Generate maximum contact residue pair sasa dataset
# Combined chain pair, residue pair information with sasa of residues together which will like:
# ['structure_id', 'chains', 'chain_pair', 'res_pair']+['structure_id', 'res_sasa']=
# ['structure_id', 'chains', 'chain_pair', 'res_pair', 'res_sasa']
def generateChainResPairSasaBsaCsv():
    try:
        pdbSasa.merging(DB.ChainResPairs_csv, DB.ResPairs_sasa_csv, join(DB.sasa_db, 'chainResPair_sasa_bsa_csv.csv'))
    except OSError as e:
        print(e)
        print('Please run generateAllPDBContact and generateAllResPairSasaBsa first.')


# NOTE: based on generateAllPDBContact
# Generate sasa, bsa of all PDB chain pair
# ['Structure_id','chain_pair','total_sasa','pair_length','bsa']
def generateAllChainPairSasaBsa(test=None):
    mer = None
    try:
        pdbSasa.generateChainPairSasaBsaByChainPairCsv(mer, test)
    except OSError as e:
        print(e)
        print('Please run generateAllPDBContact first.')


# NOTE: based on generateAllPDBContact and generateDimer
# Generate sasa, bsa of dimer chain pair
# ['Structure_id','chain_pair','total_sasa','pair_length','bsa']
def generateDimerChainPairSasaBsa(test=None):
    mer = 'dimer'
    try:
        pdbSasa.generateChainPairSasaBsaByChainPairCsv(mer, test)
    except OSError as e:
        print(e)
        print('Please run generateAllPDBContact and generateDimer first.')


# NOTE: based on generateAllPDBContact
# Generate sasa of residue pair for all PDB
# ['structure_id', 'res_sasa']
def generateAllResPairSasaBsa(test=None):
    try:
        pdbSasa.getResAsaByChainResPairsCsv(test)
    except OSError as e:
        print(e)
        print('Please run generateAllPDBContact first.')


if __name__ == '__main__':
    generateDimer('test')
    # Generate dimer dataset
    # generateDimer()

    # Generate a length of single chain PDB
    # generateLenSingleChainPDB()

    # Generate a length of single chain AlphaFold
    # generateLenSingleChainAlphaFold()

    # Generate sasa of PDB single chain
    # generateSasaPDBSingleChain()

    # Generate sasa of AlphaFold single chain
    # generateSasaAlphaSingleChain()
    
    # Generate dssp of PDB single chain
    # generateDsspPDBSingleChain()

    # Generate dssp of AlphaFold single chain
    # generateDsspAlphaFold()

    # Generate maximum contact chain pair in one structure
    # generateAllPDBContact()

    # Generate maximum contact residue pair sasa
    # generateChainResPairSasaBsaCsv()

    # Generate sasa, bsa of all PDB chain pair
    # generateAllChainPairSasaBsa()

    # Generate sasa, bsa of dimer chain pair
    # generateDimerChainPairSasaBsa()

    # Generate sasa of residue pair for all PDB
    # generateAllResPairSasaBsa()
