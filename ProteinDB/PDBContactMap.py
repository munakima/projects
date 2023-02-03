import PDBStructure as pdbStru
import Bio.PDB.NeighborSearch
import pandas as pd
import DB
import itertools
from os.path import join


class PDBContactMap():
    def __init__(self, struc):
        self.struc = struc

    def getContactResOnePairchain(self, chain1, chain2):
        """
            Get a dictionary of structure_id, maximum contact chain pair, number of contact residues, residue pairs

            :param chain1: id of chains e.g., 'A'
            :param chain2: id of chains e.g., 'B'
            :return: a dictionary format as:
            {'structure_id':'169l','num_res':324,'chain_pair':C_D,res_pair: ['C_ILE_3~D_SER_38',
            'C_ILE_3~D_PRO_37',...]}
        """
        cutoff = 5  # set residue distance less than 5A
        model = self.struc[0]
        chain_res_pair = {}
        chain2_atom_list = [at for at in model[chain2].get_atoms() if at.parent.id[0] == ' ']  # all atom of chain2
        check_identifer = []
        res_list = []
        ns = Bio.PDB.NeighborSearch(chain2_atom_list)
        for target_residue in model[chain1]:
            # set chain 2 as search range
            if target_residue.id[0] == ' ':  # chain1 ignore Hetero atom
                for target_atom in target_residue:  # chain1 atom
                    nearby_atoms = ns.search(target_atom.coord, cutoff,
                                             "A")  # Search chain1 in chain2 to get list of chain1's all nearby atoms
                    # which distance less than cutoff, i.e., 5A
                    nearby_residues = ns.search(target_atom.coord, cutoff,
                                                "R")  # Search chain1 in chain2 to get list of chain1's all nearby
                    # residues which distance less than cutoff, i.e., 5A
                    if len(nearby_atoms) != 0:  # has nearby atom
                        for nearby_res in nearby_residues:  # chain2 residues
                            if nearby_res.id[2] != ' ':  # if chain1 residues has insertion code
                                nearby_id = str(nearby_res.id[1]) + nearby_res.id[
                                    2]  # append chain1 insertion code after seq indentifier,i.e., 111A  4XAW
                            else:
                                nearby_id = nearby_res.id[1]  # chain1 seq indentifier,
                            if target_residue.id[2] != ' ':  # if chain1 residues has insertion code
                                target_id = str(target_residue.id[1]) + target_residue.id[
                                    2]  # append chain1 insertion code after seq indentifier,i.e., 111A
                            else:
                                target_id = target_residue.id[1]  # chain1 seq indentifier,
                            key1 = '{0}_{1},{2}_{3}'.format(chain1, target_id, chain2, nearby_id)
                            key2 = '{0}_{1},{2}_{3}'.format(chain2, nearby_id, chain1, target_id)
                            if key1 not in check_identifer and key2 not in check_identifer:  # avoid same residues pairs of chain pairs
                                nearby_residue = nearby_res.get_resname()  # chain2 residue
                                res_list.append(
                                    '{0}_{1}_{2}~{3}_{4}_{5}'.format(chain1, target_residue.get_resname(), target_id,
                                                                     chain2, nearby_res.get_resname(),
                                                                     nearby_id))  # A_SER_14-B_ARG_63
                                check_identifer.append(key1)  # store key
                                check_identifer.append(key2)
                        else:
                            continue
                    else:
                        continue
        chain_res_pair['structure_id'] = self.struc.id  # structure_id,i.e., 167l
        chain_res_pair['num_res'] = len(res_list)  # contact number of residues
        chain_res_pair['chain_pair'] = chain1 + '_' + chain2  # contact chain pairs,i.e., 'A_B'
        chain_res_pair['res_pair'] = res_list
        return chain_res_pair

    def getMaxContactChainPairs(self, file_path, test):
        """
            Get a maximum contact chain pair in formation in a structure
            which including structure_id, maximum contact chain pair, contact number of residues, residue pairs
            and save as csv.

            :param file_path:
            :param test: if pass nothing to test, data will save into csv, otherwise is for test
            :return: a dictionary of structure_id, chain list,max contact chain pairs,residue pairs, format as:
            {'structure_id':'169l','chains':'ABCDE','chain_pair':'C_D',res_pair:['C_ILE_3~D_SER_38', 'C_ILE_3~D_PRO_37'
            ,...]}
        """
        chain_pair_list = []
        max_contact_pair = {}
        max_contact = 0
        chain_list = pdbStru.PDBstructure(self.struc).chainLine()
        for i in itertools.combinations(chain_list,
                                        2):  # all possible combine chains, i.e.,['AB', 'AC', 'AD', 'BC', 'BD', 'CD']
            chain_pair_list.append(''.join(i), )
            chain_res_pair = self.getContactResOnePairchain(i[0], i[1])  # calculate max contact for a chain pair
            contact_num = chain_res_pair['num_res']  # record this chain pair
            if contact_num > max_contact:  # replace max_contact if contact num of this chain pair is greater
                max_contact = contact_num
                max_contact_pair = chain_res_pair  # only record one chain pair for a structure
        max_contact_dict = {'structure_id': max_contact_pair['structure_id'], 'chains': chain_list,
                            'chain_pair': max_contact_pair['chain_pair'], 'res_pair': max_contact_pair['res_pair']}
        df = pd.DataFrame([max_contact_dict], columns=['structure_id', 'chains', 'chain_pair', 'res_pair'])
        pdbStru.saveCsv(DB.structure_db, file_path, df, test)
        return max_contact_dict

    
# Caculate minimum distance between atoms of two residues of distances 
def minDis(res1,res2):
    min_dis=999999
    aa1,aa2='',''
    for a1 in res1:
        for a2 in res2:
            if a1 != a2:
                dist_matrix=a1-a2
                if(dist_matrix<min_dis):
                    min_dis=dist_matrix
                    aa1=a1.get_name()
                    aa2=a2.get_name()
    return min_dis,aa1,aa2


# Caculate maximum distance between atoms of two residues of distances 
def maxDis(res1,res2):
    max_dis=-1   
    for a1 in res1:
        for a2 in res2:
            if a1 != a2:
                dist_matrix=a1-a2
                if(dist_matrix>max_dis):
                    max_dis=dist_matrix 
                    aa1=a1.get_name()
                    aa2=a2.get_name()                        
    return max_dis,aa1,aa2


# Return atom and residue 
def returnResidueObj(atom,residue):
    atom_type=atom.get_name()
    coordinates=atom.get_coord()
    bfactor=atom.get_bfactor()
    at=Atom(atom_type,coordinates,bfactor,'')
    resname=residue.get_resname()
    whichchain=residue.get_parent().id
    reid='{0}{1}'.format(residue.id[1],residue.id[2]).strip()
    res = Residue(at,resname,whichchain,reid,is_hetatom=False)
    return res


# Calculate the minimum distance of atoms among residues in a PDB file according to a specific chain.
# filename: full path of pdb dataset
# chain_1: the first given chain
# chain_2: the second given chain
def contact_map(filename,chain_1,chain_2):
    full_filename=loading(filename)
    struc=getSloppyParser(full_filename)    
    model = struc[0]
    chains1 = model[chain_1]
    chains2 = model[chain_2]
    mapping = dict()

    global_cutoff =100 #8.0
    dis_residues = dict()
    dis_chain= dict()
    res_dis_dic=dict()

    jsonified = {}
    for residue1 in  sorted(aa_residues(chains1)):
        re1='{0}{1}'.format(residue1.id[1],residue1.id[2]).strip()
        index_id_1='{0}{1}{2}'.format(residue1.get_parent().id,re1,residue1.get_resname()) #F203THR
        if index_id_1 not in mapping:
            mapping[index_id_1] = dict()
        for residue2 in sorted(aa_residues(chains2)):
            if residue1 != residue2:
                try:
                    re2='{0}{1}'.format(residue2.id[1],residue2.id[2]).strip()
                    str2='{0}{1}{2}'.format(residue2.get_parent().id,re2,residue2.get_resname())
                    if(str2 not in mapping):
                        index_id_2 = str2
                        #print('2: '+index_id_2)
                        if index_id_1 == index_id_2:
                            print('index_id_1 == index_id_2')
                            continue
                        #print(residue1.id)
                        min_dis,min_a1,min_a2=minDis(residue1,residue2)

                        #print('{0}'.format(min_dis))
                        if (min_dis < global_cutoff):
                            min_res1 = returnResidueObj(residue1[min_a1],residue1)
                            min_res2 = returnResidueObj(residue2[min_a2],residue2)

                            min_chain_resid_atom_format='{0}/{1}/{2},{3}/{4}/{5}'.format(chain_1,min_res1.id,min_a1,chain_2,min_res2.id,min_a2)
                            res_dis_dic_key='{0}_{1},{2}_{3}'.format(chain_1,min_res1.id,chain_2,min_res2.id)
                            res_dis_dic[res_dis_dic_key]=('%.2f' % min_dis)

                            res={'res1':min_res1.res_type,'res2':min_res2.res_type,
                            'min_distance':('%.2f' % min_dis),
                            'atoms':min_chain_resid_atom_format,
                            }
                            chain_resid_key='{0}_{1},{2}_{3}'.format(chain_1,min_res1.id,chain_2,min_res2.id)
                            dis_residues[chain_resid_key]=res  
                except KeyError:
                    ## no CA atom, e.g. for H_NAG
                    continue
    dis_chain['contacts']=dis_residues
    #print(dis_chain)
    return dis_chain,res_dis_dic
#######################
# Generate CSV dataset#
#######################
# Get which chains are close to each other in one PDB structure
# and list all residues of those chains which are within a certain threshold distance
# which we set as 5Å. If passing 'test' to function that will not save into csv.
# ['structure_id', 'chains', 'chain_pair', 'res_pair']
def listAllPDBContact(pdb_list, file_path, test):
    for pdb in pdb_list:
        structure = pdbStru.getOneStrucByPath(pdb)
        struc = pdbStru.cleanStructure(structure)
        if len(pdbStru.PDBstructure(struc).allChains()) > 1:
            PDBContactMap(struc).getMaxContactChainPairs(file_path, test)
        else:
            continue


if __name__ == '__main__':
    test_directory = join('data', 'test_db')

    from optparse import OptionParser

    # Use for optionParser
    test_directory = join('data', 'test_db')

    parser = OptionParser()

    parser.add_option("--pairchain", dest="pairchain", action="store_true",
                      help="get pairchain", metavar="Contact")
    parser.add_option("--maxpairchain", dest="maxpairchain", action="store_true",
                      help="get maxpairchain", metavar="Contact")
    parser.add_option("--pdb_code", dest="pdb_code",
                      help="Holds the pdb code", metavar="PDBCODE")
    (options, args) = parser.parse_args()

    # test getContactResOnePairchain
    if options.pairchain:
        # python PDBContactMap.py --pairchain --pdb_code 1ahw
        pdb_code = '1ahw'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        contact_dict = PDBContactMap(struc).getContactResOnePairchain('A', 'B')
        target_keys = list(contact_dict.keys())
        if struc.id != pdb_code or contact_dict['num_res'] != 120 or contact_dict['chain_pair'] != 'A_B':
            print('Fail')
        elif target_keys != ['structure_id', 'num_res', 'chain_pair', 'res_pair']:
            print('Fail')

    # test getMaxContactChainPairs
    if options.maxpairchain:
        # python PDBContactMap.py --maxpairchain --pdb_code 1ahw
        pdb_code = '1ahw'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        max_contact_dict = PDBContactMap(struc).getMaxContactChainPairs('test.csv', 'test')
        target_keys = list(max_contact_dict.keys())
        if struc.id != pdb_code or max_contact_dict['chains'] != 'ABCDEF' or max_contact_dict['chain_pair'] != 'D_E':
            print('Fail')
        elif target_keys != ['structure_id', 'chains', 'chain_pair', 'res_pair']:
            print('Fail')
