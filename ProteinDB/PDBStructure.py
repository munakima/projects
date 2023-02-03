# coding: utf-8

# In[52]:


import json
from os.path import join,isfile
import os, shutil, glob,math
import random
from Bio.PDB.PDBParser import PDBParser
from Bio import SeqIO
from Bio.PDB import *
import numpy as np
from Bio.PDB import PDBList
from urllib.request import urlretrieve
import re
import DB
from os.path import join
from Bio.PDB import PDBParser
import requests
import pandas as pd
from pathlib import Path
import warnings
from Bio.PDB.PDBExceptions import PDBConstructionWarning


ALL_PDB_URL = 'https://files.rcsb.org/download/'
_hydrogen = re.compile("[123 ]*H.*")
d = re.compile("[123 ]*D.*")

# A standard residues list
residue_list = ['ASX', 'GLX', 'ALA', 'ARG', 'ASP', 'ASN', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU'
    , 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL', 'SEC', 'PYL']

# A list of atoms (excluding hydrogen) for each AA type. PDB naming convention.
residue_atoms = {
    'ALA': ['C', 'CA', 'CB', 'N', 'O'],
    'ARG': ['C', 'CA', 'CB', 'CG', 'CD', 'CZ', 'N', 'NE', 'O', 'NH1', 'NH2'],
    'ASP': ['C', 'CA', 'CB', 'CG', 'N', 'O', 'OD1', 'OD2'],
    'ASN': ['C', 'CA', 'CB', 'CG', 'N', 'ND2', 'O', 'OD1'],
    'CYS': ['C', 'CA', 'CB', 'N', 'O', 'SG'],
    'GLU': ['C', 'CA', 'CB', 'CG', 'CD', 'N', 'O', 'OE1', 'OE2'],
    'GLN': ['C', 'CA', 'CB', 'CG', 'CD', 'N', 'NE2', 'O', 'OE1'],
    'GLY': ['C', 'CA', 'N', 'O'],
    'HIS': ['C', 'CA', 'CB', 'CG', 'CD2', 'CE1', 'N', 'ND1', 'NE2', 'O'],
    'ILE': ['C', 'CA', 'CB', 'CG1', 'CG2', 'CD1', 'N', 'O'],
    'LEU': ['C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'N', 'O'],
    'LYS': ['C', 'CA', 'CB', 'CG', 'CD', 'CE', 'N', 'NZ', 'O'],
    'MET': ['C', 'CA', 'CB', 'CG', 'CE', 'N', 'O', 'SD'],
    'PHE': ['C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'N', 'O'],
    'PRO': ['C', 'CA', 'CB', 'CG', 'CD', 'N', 'O'],
    'SER': ['C', 'CA', 'CB', 'N', 'O', 'OG'],
    'THR': ['C', 'CA', 'CB', 'CG2', 'N', 'O', 'OG1'],
    'TRP': ['C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE2', 'CE3', 'CZ2', 'CZ3',
            'CH2', 'N', 'NE1', 'O'],
    'TYR': ['C', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'N', 'O',
            'OH'],
    'VAL': ['C', 'CA', 'CB', 'CG1', 'CG2', 'N', 'O']
}


#########################
# download all pdb file #
#########################
# Ubuntu download PDB structure as ent format command
# wget ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/*

# Windows download PDB structure
def downloadPDBWindows():
    pdbl = PDBList()
    PDB_list = pdbl.get_all_entries()
    for i in PDB_list:
        filename = '%s.pdb' % i[:4]
        # url='https://files.rcsb.org/download/%s' % filename
        url = ALL_PDB_URL + '%s' % filename
        dest_file = os.path.join(DB.pdb_db, filename)
        try:
            os.makedirs(DB.pdb_db)
        except OSError as e:
            pass
        urlretrieve(url, dest_file)


# Download AlphaFold human database
# https://ftp.ebi.ac.uk/pub/databases/alphafold/latest/UP000005640_9606_HUMAN_v2.tar


########################
# Loading data dataset #
########################
# Get a list of all PDB local path
def loadingPDB():
    all_files = os.listdir(DB.pdb_db)
    lists = []
    for i in all_files:
        full_filename = join(DB.pdb_db, i)
        lists.append(full_filename)
    return lists


# Get a list of all alphaFold human local path which only keep one model
def loadingAlpha():
    all_names = os.listdir(DB.alpha_db)
    alphaFold_DB_names = [(i.split('.'))[0] for i in all_names]
    name_list = []
    for i in alphaFold_DB_names:
        if i.split('-')[2] == 'F1':
            full_filename = join(DB.alpha_db, i)
            name_list.append(full_filename + DB.PDB_FORMAT)
    return name_list

# Get a full pdb file path by a given structure id
# structure_id: name of pdb dataset, e.g., 1ahw.pdb
def loading(filename):#data\testdata\1ahw.pd  
    #Common locations
    # __file__: current file path, i.o: E:\ProteinDB\ProteinDB\pdb.py
    where_i_am = os.path.dirname(os.path.abspath(__file__))  # current folder, e.g., E:\ProteinDB\ProteinDB
    
    full_filename = join(where_i_am,filename) # Database path  e.g., E:\ProteinDB\version format\data\testdata\1ahw.pdb
    return filename
#####################
# store to csv file #
#####################
def saveCsv(file_dir, file_path, pd_file, test=None):
    """
        saved as a csv.
        Create a folder, if the file_dir not exist.
        Add a header to csv file if file_path not exist,
        o.w don't add header.

        :param file_dir: directory of csv file
        :param file_path: path of csv file
        :param pd_file: target file
        :param test: if pass nothing to test, data will save into csv, otherwise is for test
    """
    if test == 'test':
        print('test, will not save into csv.')
    else:
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file = Path(file_path)
        if file.is_file():
            pd_file.to_csv(file_path, mode='a', index=False, header=False)
        else:
            pd_file.to_csv(file_path, mode='a', index=False, header=True)   

            
#################
# PDB structure #
#################
# Return a structure according to filepath
# filename: full path of pdb dataset
def getSloppyParser(filename):
    sloppyparser = PDBParser(PERMISSIVE=True, structure_builder=xpdb.SloppyStructureBuilder())
    structure_id=filename.split('\\')[-1].split('.')[0] # file name, e.g., 1ahw
    structure = sloppyparser.get_structure(structure_id, filename)
    return structure


# Get chain ids for a given structure.
# The input needs to be a PDB structure in .pdb format
def get_chain_ids(pdb_structure):
	# TODO qianhua
	return pdbStru.getChainIds(pdb_structure)


# Get structure id of pdb format for PDB
def getStrucIdByPDBPdb(pdb_path):
    pdb_path = pdb_path.replace("\\", "/")
    return pdb_path.split('/')[-1].strip('.pdb').lower()


# Get structure id of pdb format for AlphaFold
def getStrucIdByAlphaPdb(pdb_path):
    pdb_path = pdb_path.replace("\\", "/")
    return pdb_path.split('-')[1]


# Get structure id of ent format for PDB
def getStrucIdByPDBEnt(pdb_path):
    pdb_path = pdb_path.replace("\\", "/")
    return pdb_path.split('/')[-1].strip('pdb').strip('.ent').lower()


# Lookup dictionary for different PDB format and database
PDB_code_dict = {DB.PDB_FORMAT: getStrucIdByPDBPdb, DB.PDB_FORMAT + 'A': getStrucIdByAlphaPdb,
                 DB.ENT_FORMAT: getStrucIdByPDBEnt}


def getOneStrucByPath(pdb_path):
    """
        Get one structure by pass a path of structure.

        :param pdb_path: path of structure
        :return: a structure
    """
    warnings.simplefilter('ignore', PDBConstructionWarning)
    p = PDBParser(PERMISSIVE=True, QUIET=True)
    pdb_format = '.' + pdb_path.split('.')[1][-4:]
    if 'model' in pdb_path:
        pdb_format = DB.PDB_FORMAT + 'A'
    structure_id = PDB_code_dict[pdb_format](pdb_path)
    structure = p.get_structure(structure_id, pdb_path)
    return structure


# Get protein structure by structure
def cleanStructure(struc):
    """
        Get protein structure by pass a structure.

        :param struc: a biopython structure
        :return: a protein structure
    """
    model = struc[0]
    chain_to_remove = []
    res_to_remove = []
    atom_to_remove = []
    for chain in model:
        for residue in chain:
            if residue.get_resname() not in residue_list:
                res_to_remove.append(residue)
                continue
            new = str(residue.id).split(',')
            if 'H_' in new[0]:
                res_to_remove.append(residue)
            if (residue.get_resname() not in residue_list or residue.id[
                0] != ' '):  # mark not amino acid or Unknown residues #or  'H_' in (str(residue.id).split(','))[0]
                res_to_remove.append(residue)
            for atom in residue:
                if _hydrogen.match(atom.name) or d.match(atom.name):  # atom.altloc == "B"
                    atom_to_remove.append(atom)
                if (residue.get_resname() in residue_atoms.keys() and atom.name not in residue_atoms[
                    residue.get_resname()]):
                    if not atom.is_disordered():
                        atom_to_remove.append(atom)
    # remove hydrogens atoms
    for atom in atom_to_remove:
        if str(atom.get_parent()) != 'None':
            atom.get_parent().detach_child(atom.get_id())
    # mark residue that atoms are empty
    for res in model.get_residues():
        atoms = [a for a in res]
        if not atoms:
            res_to_remove.append(res)
    # remove residues
    for res in res_to_remove:
        if str(res.get_parent()) != 'None':
            res.get_parent().detach_child(res.id)

    for chains in model.get_chains():
        res = [r for r in chains]
        if not res:
            chain_to_remove.append(chains)

    for chain in chain_to_remove:
        chain.get_parent().detach_child(chain.id)
    return struc


# get protein structure by path
def loadingCleanStruc(path):
    return cleanStructure(getOneStrucByPath(path))


def global_stoichiometry(pbd_id):
    """
        Return a oligomeric state from API.

        :param pdb_id: id of pdb
        :return: a oligomeric state
    """
    rcsb_stoichiometry_api_json_response = requests.get(
        "https://data.rcsb.org/rest/v1/core/assembly/{}/1/".format(pbd_id)).json()
    if 'rcsb_struct_symmetry' in rcsb_stoichiometry_api_json_response:
        repository = rcsb_stoichiometry_api_json_response['rcsb_struct_symmetry']
        for i in repository:
            if i['kind'] == 'Global Symmetry':
                return i['oligomeric_state']


def getAllDimerPDB(pdb_list, test):
    """
        Return a dimer list for all PDB structures.

        :param pdb_list: a list of all pdb path
        :return: a dimer list
    """
    dimer_list = []
    for pdb in pdb_list:
        pbd_id = pdb.split('.')[0][-4:]
        stoichiometry = global_stoichiometry(pbd_id)
        if stoichiometry == 'Hetero 2-mer':
            dimer_list.append(pbd_id)
            dimer_df = pd.DataFrame({'structure_id': [pbd_id]}, columns=['structure_id'])
            saveCsv(DB.structure_db, DB.dimer_csv, dimer_df, test)
    return dimer_list


def getSingleChainStructure(pdb_list):
    """
        Return a single-chain list for all PDB structures.

        :param pdb_list: a list of all pdb path
        :return: a single-chain list
    """
    singleChain_list = []
    for pdb_path in pdb_list:
        structure = getOneStrucByPath(pdb_path)
        struc = cleanStructure(structure)
        chains = [c for c in struc[0].get_chains()]
        if len(chains) == 1:
            singleChain_list.append(pdb_path)
    return singleChain_list

standard_aa_names = [
    "ALA",
    "CYS",
    "ASP",
    "GLU",
    "PHE",
    "GLY",
    "HIS",
    "ILE",
    "LYS",
    "LEU",
    "MET",
    "ASN",
    "PRO",
    "GLN",
    "ARG",
    "SER",
    "THR",
    "VAL",
    "TRP",
    "TYR",
    "SEC",
    "PYL",
]
aa1 = "ACDEFGHIKLMNPQRSTVWYUO"
aa3 = standard_aa_names
d1_to_index = {}
dindex_to_1 = {}
d3_to_index = {}
dindex_to_3 = {}

# Create some lookup tables
for i in range(0, 22):
    n1 = aa1[i]
    n3 = aa3[i]
    d1_to_index[n1] = i
    dindex_to_1[i] = n1
    d3_to_index[n3] = i
    dindex_to_3[i] = n3


def three_to_index(s):
    return d3_to_index[s]


def three_to_one(s):
    i = d3_to_index[s]
    return dindex_to_1[i]


def is_aa_22(residue):
    if not isinstance(residue, str):
        residue = residue.get_resname()
    residue = residue.upper()
    return residue in d3_to_index


def getStructureSequenceByChain(struc, which_chain):
    """
        Return a single-chain list for all PDB structures.

        :param struc: a structure
        :param which_chain: a specific chain
        :return: a full sequence
    """
    model = struc[0]
    seq = []
    name = struc.id
    for residue in model[which_chain]:
        if residue.get_resname() in standard_aa_names:
            seq.append(three_to_one(residue.get_resname()))
    full_seq = ''.join(seq)
    return name, full_seq


class PDBstructure:
    struc_id = None
    struc = None

    def __init__(self, struc):
        self.struc = struc
        self.struc_id = struc.id
        self.model = self.struc[0]

    def chainLine(self):
        chains = [c.id for c in self.model.get_chains()]
        lines = (''.join(str(c) for c in chains))
        return lines

    def allChains(self):
        chains = [c.id for c in self.model.get_chains()]
        return chains


class PDBchain:
    chain_id = None
    struc = None

    def __init__(self, struc, whichchain):
        self.chain = whichchain
        self.struc = struc
        self.model = self.struc[0]
        self.chains_dict = {}
        self.list = []

    def getResByChainId(self):
        for r in self.model[self.chain]:
            self.list.append('{0}_{1}'.format(r.id[1], r.get_resname()))
        self.chains_dict[self.chain] = self.list
        return self.chains_dict

    def getResNum(self):
        residues = [l for l in self.chains_dict[self.chain]]
        return len(residues)


def getAlphaName(path):
    """
        Return alphaFold structure name by path of it

        :param path: a structure
        :return: a string name
    """
    path = path.split('/')[-1]
    alphaFold_DB_names = path.split('-')[1]
    return alphaFold_DB_names


#######################
# Generate CSV dataset#
#######################


def generateLenByStructure(struc, file_path, test):
    """
        Get length by one structure, and save as csv.

        :param struc: a structure
        :param file_path: target file
        :param test: for test or not
        :param return: a dictionary of length for PDB or AlphaFold, Format as:
        {'structure_id':169l, chain_id:'ABCDE', length:324}
    """
    res_num = [r for r in struc[0].get_residues()]
    chains = PDBstructure(struc).chainLine()
    len_dict = {'structure_id': struc.id, 'chain_id': chains, 'length': len(res_num)}
    df = pd.DataFrame([len_dict], columns=['structure_id', 'chain_id', 'length'])
    saveCsv(DB.structure_db, file_path, df, test)
    return len_dict


def getListLenByStructure(pdb_list, file_path, test):
    """
        Generate a csv to store length of structures by a dataset.

        :param pdb_list: a PDB or AlphaFold dataset
        :param file_path: target directory
        :param test: for test or not
    """
    for pdb in pdb_list:
        structure = getOneStrucByPath(pdb)
        struc = cleanStructure(structure)
        if len(PDBstructure(struc).allChains()) == 1:
            generateLenByStructure(struc, file_path, test)
        else:
            continue
            
            
###########################
# sequence from structure #
###########################
# Get full seq from a structure by filename
# filename: full path of pdb dataset
def WriteSeqFromStructure(filename):
    full_seq=[]
    i=0
    struc=getSloppyParser(filename)
    for model in struc:       
        seqs = [] 
        for chain in model:
            seq = []
            i+=1
            full_seq.append(struc.id+'_'+chain.id)# structure id and chain id of seq, e.g., '1ahw_A','1ahw_B',...,'1ahw_F'
            for residue in chain:
                if(residue.get_resname() in standard_aa_names):
                    seq.append(polypep.three_to_one(residue.get_resname())) # transfer residues name to one letter by standard_aa_names
            seqs=(''.join(seq)) # make the seq to one line, e.g., 'DIKM...NEC'
            full_seq.append(seqs) # add seqs into full_seq
    return full_seq


# Get seq from structure by full path and a specific chain
# filename: directory of pdb data + pdb name, e.g., 'data\\testdata\\1ahw.pdb'
# whichchain: a given chain, e.g., 'A'
def getStructureSequence(filename,whichchain):
    full_filename=loading(filename)
    struc=getSloppyParser(full_filename)
    full_seq=[]
    for model in struc:       
        seq = []
        full_seq.append(struc.id+'_'+model[whichchain].id)#struc.id+'_'+str(i)+' | Chain '+chain.id
        for residue in model[whichchain]:
            if(residue.get_resname() in standard_aa_names):
                seq.append(polypep.three_to_one(residue.get_resname()))
        full_seq.append((''.join(seq)))
    return full_seq


# The main function will parse options via the parser variable.
# These options will be defined by the user on the console.
if __name__ == '__main__':
    from optparse import OptionParser

    # Use for optionParser
    test_directory = join('data', 'test_db')

    parser = OptionParser()

    parser.add_option("--structurePDB", dest="structurePDB", action="store_true",
                      help="get structurePDB", metavar="Structure")
    parser.add_option("--structureAlpha", dest="structureAlpha", action="store_true",
                      help="get structureAlpha", metavar="Structure")
    parser.add_option("--dimer", dest="dimer", action="store_true",
                      help="get dimer", metavar="Structure")
    parser.add_option("--singlechain", dest="singlechain", action="store_true",
                      help="get singlechain", metavar="Structure")
    parser.add_option("--seq", dest="seq", action="store_true",
                      help="get seq", metavar="Structure")
    parser.add_option("--alphaname", dest="alphaname", action="store_true",
                      help="get alpha name", metavar="Structure")
    parser.add_option("--loadingAlpha", dest="loadingAlpha", action="store_true",
                      help="get loadingAlpha", metavar="Structure")
    parser.add_option("--loadingPDB", dest="loadingPDB", action="store_true",
                      help="get loading PDB", metavar="Structure")
    parser.add_option("--pdb_code", dest="pdb_code",
                      help="Holds the pdb code", metavar="PDBCODE")
    (options, args) = parser.parse_args()

    # test getOneStrucByPath PDB
    if options.structurePDB:
        # python PDBStructure.py --structurePDB --pdb_code 1ahw
        pdb_code = '1ahw'
        chain = 'A'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        struc = getOneStrucByPath(path)
        if struc.id != pdb_code:
            print('Fail')

    # test getOneStrucByPath AlphaFold
    if options.structureAlpha:
        # python PDBStructure.py --structureAlpha --pdb_code A0A0A0MS05
        pdb_code = 'A0A0A0MS05'
        chain = 'A'
        path = test_directory + '/' + 'AF-A0A0A0MS05-F1-model_v1' + DB.PDB_FORMAT
        struc = getOneStrucByPath(path)
        if struc.id != pdb_code:
            print('Fail')

    # test global_stoichiometry
    if options.dimer:
        # python PDBStructure.py --dimer --pdb_code 1igm
        pdb_code = '1igm'
        chain = 'A'
        hetero = global_stoichiometry(pdb_code)
        if hetero != 'Hetero 2-mer':
            print('Fail')

    # test getSingleChainStructure
    if options.singlechain:
        # python PDBStructure.py --singlechain --pdb_code 1a8o
        pdb_code = '1a8o'
        path = test_directory + '/' + pdb_code + DB.PDB_FORMAT
        single_chain_path = getSingleChainStructure([path])
        structure = getOneStrucByPath(single_chain_path[0])
        struc = cleanStructure(structure)
        chains = [c for c in struc[0].get_chains()]
        if len(chains) != 1:
            print('Fail')

    # test getStructureSequenceByChain
    if options.seq:
        # python PDBStructure.py --seq --pdb_code sample
        pdb_code = 'sample'
        chain = 'F'
        path = test_directory + '/' + pdb_code + DB.PDB_FORMAT
        structure = getOneStrucByPath(path)
        struc = cleanStructure(structure)
        name, seqs = getStructureSequenceByChain(struc, chain)
        if seqs != 'TDSPVECMG':
            print('Fail')

    # test loadingAlpha
    if options.loadingAlpha:
        # python PDBStructure.py --loadingAlpha
        target_list = loadingAlpha()
        if len(target_list) != 3:
            print('Fail')

    # test loadingPDB
    if options.loadingPDB:
        # python PDBStructure.py --loadingPDB
        target_list = loadingPDB()
        if len(target_list) != 4:
            print('Fail')

    # test getAlphaName
    if options.alphaname:
        # python PDBStructure.py --alphaname --pdb_code A0A0A0MS05
        pdb_code = 'sample'
        chain = 'F'
        path = join(test_directory, 'AF-A0A0A0MS05-F1-model_v1.pdb')
        seqs = getAlphaName(path)
        if seqs != 'A0A0A0MS05':
            print('Fail')
