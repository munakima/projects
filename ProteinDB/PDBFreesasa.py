import PDBStructure as pdbStru
import freesasa
import DB
import pandas as pd
from os.path import join


def getASAByStruc(struc):
    """
        Get sasa by a Biopython structure.

        :param struc: a Biopython structure.
    """
    freesasa_structure = freesasa.structureFromBioPDB(struc[0])
    result = freesasa.calc(freesasa_structure)
    return '%0.2f' % result.totalArea()


def merging(file1, file2, merge_file):
    """
        Merge two csv file.

        :param file1: csv1 file
        :param file2: csv2 file
        :param merge_file: path of merge file
    """
    csv1 = pd.read_csv(file1)
    csv2 = pd.read_csv(file2)
    df = pd.merge(csv1, csv2)
    df.to_csv(merge_file, index=False, header=True)


def getASABystructure(struc, file, test):
    """
        Get structure_id,chain_id, sasa by a Biopython structure.
        And save as csv file.

        :param struc: a Biopython structure
        :param file: a target file
        :param test: if pass nothing to test, data will save into csv, otherwise is for test
        :return: a sasa dictionary, format as:
        {'structure_id':'101m', 'chain_id': 'A','sasa': 8180.48}
    """
    sasa = getASAByStruc(struc)
    chains = pdbStru.PDBstructure(struc).chainLine()
    sasa_dict = {}
    sasa_dict['structure_id'] = struc.id
    sasa_dict['chain_id'] = chains
    sasa_dict['sasa'] = sasa
    df = pd.DataFrame([sasa_dict], columns=['structure_id', 'chain_id', 'sasa'])
    pdbStru.saveCsv(DB.sasa_db, file, df, test)
    return sasa_dict


##############
# chain pair #
##############
def getGivenChainSasa(struc, target_chains):
    """
        Get SASA by a structure and target chains.

        :param struc: a Biopython structure
        :param target_chains: a list of target chains, e.g., ['A', 'B']
        :return: total area of a structure with giving chains
    """
    all_chains = pdbStru.PDBstructure(struc).allChains()  # all chains of a clean structure
    delChains = [c for c in all_chains if c not in target_chains]  # mark chains except targetChains
    [struc[0].detach_child(c) for c in delChains]  # delete chains except targetChains
    freesasa.setVerbosity(1)  # nowarnings FreeSASA: warning
    result = getASAByStruc(struc)
    return result


def calContactSeperateBuriedArea(path, sel_chains):
    """
        Get SASA by a structure's path and target chains.

        :param struc: a structure's path
        :param sel_chains: select two chains with format e.g., A_B
        :return: a dictionary
        {
            'Structure_id':10gs,'chain_pair':A_B,'total_sasa':17725.83,'pair_length':416,'bsa':1187.60
        }
    """
    structure = pdbStru.getOneStrucByPath(path)
    struc = pdbStru.cleanStructure(structure)
    sasa = {}
    sasa['Structure_id'] = struc.id
    targetChains = sel_chains.split('_')  # ['A', 'B']
    # a clean structure removed Unknown residues and atoms in order to avoid error when doing freesasa calculate
    totalSasa = getGivenChainSasa(struc, targetChains)
    chain_len = 0
    buried_sasa = float(totalSasa)
    sasa['chain_pair'] = sel_chains
    sasa['total_sasa'] = totalSasa
    for chain in struc[0]:
        if chain.id in targetChains:
            for res in chain:
                chain_len += 1
    sasa['pair_length'] = chain_len
    for chain in targetChains:
        stru = pdbStru.getOneStrucByPath(path)  # initialize structure
        clean_struc = pdbStru.cleanStructure(stru)
        chainSasa = getGivenChainSasa(clean_struc, chain)  # get sasa of a single chain
        buried_sasa -= float(chainSasa)
    sasa['bsa'] = '% .2f' % -(buried_sasa / 2)  # formula  buried area= -((totalSasa-chain1 sasa - chain2 sasa)/2)
    return sasa


# Note for PDB, this function need to generate the ChainResPairs_csv.csv
# by the getMaxContactChainPairs function first.
# For dimer, this function need to generate the dimer.csv by
# the generateDimer function first, and the function mentioned before.
def generateChainPairSasaBsaByChainPairCsv(mer, test):
    """
        Get SASA and BSA by chain pairs in exist dataset,
        which is the maximum contact in a structure,
        if structure is dimer passing dimer to mer,
        if structure not specific, pass nothing.

        :param mer: pass string 'dimer' or nothing
        :param test: if pass nothing to test, data will save into csv, otherwise is for test
        :return: a dictionary, format as:
        {
            'Structure_id':10gs,'chain_pair':A_B,'total_sasa':17725.83,'pair_length':416,'bsa':1187.60
        }
    """
    buried_list = []
    #try:
    csv_df = pd.read_csv(DB.ChainResPairs_csv)
    print(csv_df)
    if mer is None:
        for index, row in csv_df.iterrows():
            path = DB.pdb_db + '/pdb' + row['structure_id'] + DB.ENT_FORMAT
            values = row['chain_pair']
            pair = calContactSeperateBuriedArea(path, values)
            df = pd.DataFrame([pair])
            pdbStru.saveCsv(DB.sasa_db, DB.ChainPair_sasa_bsa_csv, df, test)
            buried_list.append(pair)
    elif mer == 'dimer':
        df = pd.read_csv(DB.dimer_csv)
        li = list(df['structure_id'])
        for index, row in csv_df.iterrows():
            if row['structure_id'] in li:
                path = DB.pdb_db + '/pdb' + row['structure_id'] + DB.ENT_FORMAT
                values = row['chain_pair']
                pair = calContactSeperateBuriedArea(path, values)
                df = pd.DataFrame([pair])
                pdbStru.saveCsv(DB.sasa_db, DB.dimer_ChainPair_sasa_bsa_csv, df, test)
                buried_list.append(pair)
    # except OSError as e:
    #     print(e)
    return buried_list


################
# residue pair #
################
def getResSasa(clean, k, v):
    """
        Get SASA by passing a protein structure,

        :param clean: a Biopython protein structure
        :param k: id of chain e.g., A
        :param v: residue name e.g., ALA
        :return: a residue area
    """
    stru_Free = freesasa.structureFromBioPDB(clean)
    result = freesasa.calc(stru_Free)
    dic = result.residueAreas()
    complex_res = dic[k][v]
    complex_sasa = '%.2f' % complex_res.total
    return complex_sasa


def remainTargetRes(struc, target_chain):
    """
        Get a new structure after removing target chains from struc,

        :param struc: a Biopython structure
        :param target_chain: id of chains e.g.,  ['A', 'B']
        :return: a residue area
    """
    model = struc
    all_chains = [c.id for c in model]
    del_chains = [c for c in all_chains if c not in target_chain]  # mark chains except targetChains
    [model.detach_child(c) for c in del_chains]  # delete chains except targetChains
    return struc


# Note this function need to generate the ChainResPairs_csv.csv by
# the getMaxContactChainPairs function first.
def getResAsaByChainResPairsCsv(test):
    """
        Read exist chain residues pairs use it to calculate the combine residues,
        SASA and without combine residues' SASA. Store dict result and save as csv.

        :param struc: .ent or .pdb format
        :param test: if pass nothing to test, data will save into csv, otherwise is for test
        :return: a residue area, format as:
        {'structure_id':169l, res_sasa:'C_93': ['73.50', '25.09'],...}
    """
    df = pd.read_csv(DB.ChainResPairs_csv)
    for index, row in df.iterrows():
        line = row['res_pair'].replace(" ", "").replace("'", "").strip("[").strip("]").split(',')
        print(row['structure_id'])
        list_a = []
        list_b = []
        res_sasa_list = {}
        stru_pair = {}
        for j in line:
            A = j.split('~')[0]
            B = j.split('~')[1]
            list_a.append(A.split('_')[0] + '_' + A.split('_')[2])
            list_b.append(B.split('_')[0] + '_' + B.split('_')[2])
        chain_res = list(set(list_a)) + list(set(list_b))

        pdb_path = DB.pdb_db + '/pdb' + row['structure_id'] + DB.ENT_FORMAT
        for c in chain_res:
            chain_arr = []
            structure = pdbStru.getOneStrucByPath(pdb_path)
            struc = pdbStru.cleanStructure(structure)
            sp = c.split('_')
            comb = getResSasa(struc[0], sp[0], sp[1])
            stru_s = remainTargetRes(struc[0], sp[0])
            single = getResSasa(stru_s, sp[0], sp[1])
            chain_arr.append(single)
            chain_arr.append(comb)
            res_sasa_list[c] = chain_arr
        stru_pair['structure_id'] = row['structure_id']
        new_res = {i: res_sasa_list[i] for i in sorted(res_sasa_list)}
        stru_pair['res_sasa'] = new_res
        df = pd.DataFrame({'structure_id': [stru_pair['structure_id']], 'res_sasa': [stru_pair['res_sasa']]},
                          columns=['structure_id', 'res_sasa'])
        pdbStru.saveCsv(DB.sasa_db, DB.ResPairs_sasa_csv, df, test)
        print(stru_pair)
    return stru_pair


#######################
# Generate CSV dataset#
#######################

# For generate sasa of PDB single chain and AlphaFold function
# ['structure_id', 'chain_id', 'sasa']
def loadListForSasaSingleChain(pdb_list, path, test):
    for pdb in pdb_list:
        structure = pdbStru.getOneStrucByPath(pdb)
        struc = pdbStru.cleanStructure(structure)
        if len(pdbStru.PDBstructure(struc).allChains()) == 1:
            getASABystructure(struc, path, test)
        else:
            continue


if __name__ == '__main__':
    test_directory = join('data', 'test_db')

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("--getchainssasa", dest="getchainssasa", action="store_true",
                      help="get get chains sasa", metavar="Freesasa")
    parser.add_option("--sasa", dest="sasa", action="store_true",
                      help="get sasa by chain list", metavar="Freesasa")
    parser.add_option("--totalsasa", dest="totalsasa", action="store_true",
                      help="get dimer", metavar="Freesasa")
    parser.add_option("--bsa", dest="bsa", action="store_true",
                      help="get dimer", metavar="Freesasa")
    parser.add_option("--keep_onechain_struc", dest="keep_onechain_struc", action="store_true",
                      help="get keep_onechain_struc", metavar="Freesasa")
    parser.add_option("--pdb_code", dest="pdb_code",
                      help="Holds the pdb code", metavar="PDBCODE")

    (options, args) = parser.parse_args()

    # test getGivenChainSasa
    if options.sasa:
        # python PDBFreesasa.py --sasa --pdb_code 1ahw
        pdb_code = '1ahw'
        chains = ['A', 'B']
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        sasa = getGivenChainSasa(struc, chains)
        if (sasa != '18773.39'):
            print('Fail')

    # test totalsasa
    if options.totalsasa:
        # python PDBFreesasa.py --totalsasa --pdb_code 1ahw
        pdb_code = '1ahw'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        sasa = getASAByStruc(struc)
        if sasa != '54779.16':
            print('Fail')

    # test remainTargetRes
    if options.keep_onechain_struc:
        # python PDBFreesasa.py --keep_onechain_struc --pdb_code 1ahw
        pdb_code = '1ahw'
        chain = 'A'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        new_struc = remainTargetRes(struc[0], chain)
        chains = [c for c in new_struc.get_chains()]
        if len(chains) > 1 or chains[0].id != chain:
            print('Fail')

    # test calContactSeperateBuriedArea
    if options.bsa:
        # python PDBFreesasa.py --bsa --pdb_code 1ahw
        pdb_code = '1ahw'
        chains = 'A_B'
        path = test_directory + '/pdb' + pdb_code + DB.ENT_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        sasa = calContactSeperateBuriedArea(path, chains)
        if sasa['bsa'].strip() != '1815.48':
            print('Fail')

    # test calContactSeperateBuriedArea
    if options.getchainssasa:
        # python PDBFreesasa.py --getchainssasa --pdb_code sample
        pdb_code = 'sample'
        path = test_directory + '/' + pdb_code + DB.PDB_FORMAT
        structure = pdbStru.getOneStrucByPath(path)
        struc = pdbStru.cleanStructure(structure)
        sasa = getASABystructure(struc, 'test', test=None)
        if (sasa['sasa'].strip() != '1276.65' or sasa['structure_id'] != 'sample'
                or sasa['chain_id'] != 'F'):
            print('Fail')
