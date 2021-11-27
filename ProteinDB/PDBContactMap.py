import PDBStructure as pdbStru
import Bio.PDB.NeighborSearch
import pandas as pd
import DB
import itertools

def getContactResOnePairchain(struc,chain1,chain2):
    cutoff = 5  # set residue distance less than 5A
    model = struc[0]
    chain_res_pair={}
    chain2_atom_list = [at for at in model[chain2].get_atoms() if at.parent.id[0] == ' '] # all atom of chain2
    check_indentifer = []
    res_list=[]
    ns = Bio.PDB.NeighborSearch(chain2_atom_list)
    for target_residue in model[chain1]:
         # set chain 2 as search range
        if (target_residue.id[0] == ' '): # chain1 ignore Hetero atom
            for target_atom in target_residue: # chain1 atom
                nearby_atoms = ns.search(target_atom.coord, cutoff, "A") # Search chain1 in chain2 to get list of chain1's all nearby atoms which distance less than cutoff, i.e., 5A
                nearby_residues = ns.search(target_atom.coord, cutoff, "R") # Search chain1 in chain2 to get list of chain1's all nearby residues which distance less than cutoff, i.e., 5A
                if (len(nearby_atoms) != 0): # has nearby atom
                    for nearby_res in nearby_residues: # chain2 residues
                        if (nearby_res.id[2] != ' '): # if chain1 residues has insertion code
                           nearby_id = str(nearby_res.id[1]) + nearby_res.id[2] # append chain1 insertion code after seq indentifier,i.e., 111A  4XAW
                        else:
                           nearby_id = nearby_res.id[1] # chain1 seq indentifier,
                        if (target_residue.id[2] != ' '): # if chain1 residues has insertion code
                           target_id = str(target_residue.id[1]) + target_residue.id[2] # append chain1 insertion code after seq indentifier,i.e., 111A
                        else:
                           target_id = target_residue.id[1] # chain1 seq indentifier,
                        key1 = '{0}_{1},{2}_{3}'.format(chain1, target_id, chain2, nearby_id)
                        key2 = '{0}_{1},{2}_{3}'.format(chain2, nearby_id, chain1, target_id)
                        if (key1 not in check_indentifer and key2 not in check_indentifer): # avoid same residues pairs of chain pairs
                            nearby_residue = nearby_res.get_resname() # chain2 residue
                            res_list.append('{0}_{1}_{2}~{3}_{4}_{5}'.format(chain1,target_residue.get_resname(), target_id,chain2, nearby_res.get_resname(), nearby_id))#A_SER_14-B_ARG_63
                            check_indentifer.append(key1) # store key
                            check_indentifer.append(key2) 
                    else:
                       continue
                else:
                    continue               
    chain_res_pair['structure_id'] = struc.id # structure_id,i.e., 167l
    chain_res_pair['num_res'] = len(res_list) # contact number of residues
    #chain_res_pair['chains'] = chain1+chain2
    chain_res_pair['chain_pair'] = chain1 + '_' + chain2 # contact chain pairs,i.e., 'A_B'
    chain_res_pair['res_pair'] = res_list
    return chain_res_pair

def getMaxContactChainPairs(struc):
    chain_pairs_lists=[]
    buried_list=[]
    exist_list = []
    chain_pair_list = []
    max_contact_pair = []
    max_contact=0
    model=struc[0]
    chain_list = pdbStru.PDBstructure(struc).chainLine()
    for i in itertools.combinations(chain_list, 2): # all possible combine chains, i.e.,['AB', 'AC', 'AD', 'BC', 'BD', 'CD']
        chain_pair_list.append(''.join(i), )
        chain_res_pair = getContactResOnePairchain(struc,i[0],i[1]) # calculate max contact for a chain pair
        contactnum = chain_res_pair['num_res'] # record this chain pair
        if(contactnum > max_contact): # replace max_contact if contact num of this chain pair is greater
            max_contact = contactnum
            max_contact_pair = chain_res_pair # only record one chain pair for a structure
    print(chain_list)
    df=pd.DataFrame({'structure_id':[max_contact_pair['structure_id']],'chains':[chain_list],'chain_pair':[max_contact_pair['chain_pair']],'res_pair':[max_contact_pair['res_pair']]},columns=['structure_id','chains','chain_pair','res_pair'])
    pdbStru.saveCsv(DB.structure_db,DB.ChainResPairs_csv,df)
    return max_contact_pair

if __name__ == '__main__':

	###general chain pair
	#'''
	# pdb_list=pdbStru.getAllStruc(DB.ENT_FORMAT)
	# for pdb_path in pdb_list:
	# 	structure=pdbStru.getOneStrucByPath(pdb_path)
	# 	print(structure.id)
	# 	struc=pdbStru.cleanStructure(structure)
	# 	chain_list = pdbStru.PDBstructure(struc).allChains()
	# 	print(len(chain_list))
	# 	if(len(chain_list)<=1):
	# 		continue
	# 	else:	
	# 		getMaxContactChainPairs(struc)

	#'''##END general chain pair


	#not protein list
	'''
	pdb_list=pdbStru.getAllStruc(DB.ENT_FORMAT)
	for pdb_path in pdb_list:
		structure=pdbStru.getOneStrucByPath(pdb_path)
		print(structure.id)
		struc=pdbStru.cleanStructure(structure)
		chain_list = pdbStru.PDBstructure(struc).allChains()
		print(len(chain_list))
		if(len(chain_list)<=1):
			df=pd.DataFrame([structure.id],columns=['structure_id'])
			pdbStru.saveCsv(DB.category_db,DB.notprotein_csv,df)
	'''##END not protein list

	pdb_path='F:/1/pdb4xaw.ent'
	# structure=pdbStru.getOneStrucByPath(pdb_path)
	# struc=pdbStru.cleanStructure(structure)
	#y=getContactResOnePairchain(struc,'L','H')
	# pdb_list=['F:/1/pdb12e8.ent']
	#print(getMaxContactChainPairs(struc))
