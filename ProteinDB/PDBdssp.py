from Bio.PDB.DSSP import DSSP
import PDBStructure as pdbStru
import DB
import pandas as pd


def getNumberHelixLoopsSheet(structure, path, test):
    model = structure[0]
    dssp = DSSP(model, path, dssp=DB.dssp_path)
    dict_HelixLoopsSheet = {}
    line = ''
    for i in dssp.keys():
        # print(dssp[i])
        if dssp[i][3] != 'NA':
            if dssp[i][2] == 'H':
                line += 'H'
            elif dssp[i][2] == 'E':
                line += 'E'
            else:
                line += 'C'
    print(line)
    newline = ''
    count_c = 0
    count_C = 0
    count_H = 0
    count_E = 0
    for i in range(0, len(line)):
        if line[i] == 'C':
            count_c += 1
        elif line[i] != 'C' and i != 0 and count_c > 3:
            newline += 'C'
            count_C += 1
            count_c = 0
        if line[i] == 'H' and line[i - 1] != line[i]:
            newline += 'H'
            count_H += 1
        elif line[i] == 'E' and line[i - 1] != line[i]:
            newline += 'E'
            count_E += 1
        elif line[i] != 'C':
            count_c = 0
        elif line[i] == 'C' and i == (len(line) - 1) and count_c > 3:
            newline += 'C'
            count_C += 1
            count_c = 0
    print(newline)
    # new = [[i, newline.count(i)] for i in (newline)]
    key = 'structure_id'
    dict_HelixLoopsSheet[key] = structure.id  # structure.id[-4:len(structure.id)]
    dict_HelixLoopsSheet['loops'] = count_C
    dict_HelixLoopsSheet['alpha_helix'] = count_H
    dict_HelixLoopsSheet['beta_sheet'] = count_E
    # for k in new:
    #     key=k[0]
    #     dict_HelixLoopsSheet[key]=k[1]
    print(dict_HelixLoopsSheet)
    df = pd.DataFrame(
        {'structure_id': [structure.id], 'loops': [count_C], 'alpha_helix': [count_H], 'beta_sheet': [count_E]},
        columns=['structure_id', 'loops', 'alpha_helix', 'beta_sheet'])
    pdbStru.saveCsv(DB.dssp_db, path, df, test)


# For generate dssp for database
# ['structure_id', 'loops', 'alpha_helix', 'beta_sheet']
def loadListForDSSPAlphaFold(pdb_list,path, test):
    for pdb in pdb_list:
        structure = pdbStru.getOneStrucByPath(pdb)
        struc = pdbStru.cleanStructure(structure)
        if len(pdbStru.PDBstructure(struc).allChains()) == 1:
            getNumberHelixLoopsSheet(struc, path, test)
        else:
            continue
