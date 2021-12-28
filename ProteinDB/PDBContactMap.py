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
